pipeline {
    agent any

    parameters {
        string(name: 'INSTANCE_COUNT', defaultValue: '6', description: 'Number of EC2 instances to deploy')
        string(name: 'AMOUNT_OF_HEXAGONS', defaultValue: '5', description: 'Number of hexagons to scrape')
        string(name: 'REPO_URL', defaultValue: 'https://github.com/your/repo.git', description: 'Git repository URL')
        string(name: 'SCRIPT_NAME', defaultValue: 'start.sh', description: 'Bash script to install all dependencies and run the scraper')
        string(name: 'INSTANCE_TYPE', defaultValue: 't2.medium', description: 'EC2 Instance Type')
        string(name: 'INSTANCE_SECURITY_GROUP', defaultValue: 'sg-02ca8252d2971d420', description: 'EC2 Security Group')
        string(name: 'AMI_ID', defaultValue: 'ami-0866a3c8686eaeeba', description: 'Amazon Machine Image (AMI) ID')
        string(name: 'KEY_NAME', defaultValue: 'jenkins-test', description: 'Key pair for SSH access')
    }

    stages {
        stage('Launch EC2 Instances') {
            steps {
                script {
                    def stdOutput = sh(
                        script: """
                        aws ec2 run-instances \
                            --image-id ${params.AMI_ID} \
                            --instance-type ${params.INSTANCE_TYPE} \
                            --key-name ${params.KEY_NAME} \
                            --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-021176b1e05cb6895","VolumeSize":8,"VolumeType":"gp3","Throughput":125}}' \
                            --network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["${params.INSTANCE_SECURITY_GROUP}"]}' \
                            --credit-specification '{"CpuCredits":"standard"}' \
                            --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"WorldScraper"}]}' \
                            --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
                            --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
                            --count ${params.INSTANCE_COUNT} \
                            --query "Instances[*].InstanceId" \
                            --output text
                        """,
                        returnStdout: true
                    ).trim()
                    def instanceIds = stdOutput.split().join(' ')
                    env.INSTANCE_IDS = instanceIds
                    echo "Launched instance IDs: ${instanceIds}"

                    // Wait for instances to be running
                    sh """
                    aws ec2 wait instance-running --instance-ids ${env.INSTANCE_IDS}
                    """
                    
                    // Additional wait for system status checks
                    sh """
                    aws ec2 wait instance-status-ok --instance-ids ${env.INSTANCE_IDS}
                    """
                }
            }
        }
        stage('Copy project folder into instances') {
            steps {
                script {
                    // env.INSTANCE_IDS = "i-0963d24e25e21615c"
                    echo "Fetching public IP for instance IDs: ${env.INSTANCE_IDS}"

                    // Get the public IP of the instance
                    def stdOutput = sh(
                        script: """
                        aws ec2 describe-instances \
                            --instance-ids ${env.INSTANCE_IDS} \
                            --query "Reservations[*].Instances[*].PublicDnsName" \
                            --output text
                        """,
                        returnStdout: true
                    ).trim()
                    def publicDnsNames = stdOutput.split()
                    env.PUBLIC_DNS_NAMES = publicDnsNames.join(' ')
                    def futures = [:]

                    echo "publicDnsNames: ${publicDnsNames}"
                    
                    sshagent(credentials: ['jenkins-world-scraper-ec2-key']) {
                        publicDnsNames.each { publicDnsName ->
                            futures[publicDnsName] = {
                                echo "SCPing into: ${publicDnsName}"
                                def sshStdOutput = sh(
                                    script:"""
                                    ssh -o StrictHostKeyChecking=no ubuntu@${publicDnsName} "sudo rm -rf ~/world-scraper"
                                    scp -o StrictHostKeyChecking=no -r ~/world-scraper ubuntu@${publicDnsName}:~/
                                    ssh -o StrictHostKeyChecking=no ubuntu@${publicDnsName} "sudo sh ~/world-scraper/${params.SCRIPT_NAME}"
                                    """,
                                    returnStdout: true
                                )
                                echo "Result: ${sshStdOutput}"    
                            }
                        }
                        parallel futures
                    }
                }
            }
        }
        stage('SSH into each instance and run the project N times') {
            steps {
                script {
                    def publicDnsNames = env.PUBLIC_DNS_NAMES.split()
                    int amountOfHexagons = params.AMOUNT_OF_HEXAGONS as Integer
                    echo "amountOfHexagons: ${params.AMOUNT_OF_HEXAGONS} $amountOfHexagons"
                    def futures = [:]
                    sshagent(credentials: ['jenkins-world-scraper-ec2-key']) {
                        publicDnsNames.each { publicDnsName ->
                            for(int i = 1; i <= amountOfHexagons; i++) {
                                echo "$publicDnsName-$i"
                                futures["$publicDnsName-$i"] = {
                                    echo "SSHing into: ${publicDnsName}"
                                    def sshStdOutput = sh(
                                        script:"""
                                        ssh -o StrictHostKeyChecking=no ubuntu@${publicDnsName} "cd world-scraper && sudo poetry run python3 src/main.py"
                                        """,
                                        returnStdout: true
                                    )
                                    echo "Result: ${sshStdOutput}"    
                                }
                            }
                        }
                        parallel futures
                    }
                }
            }
        }
        stage('Terminate EC2 Instances') {
            steps {
                script {
                    sh """
                    aws ec2 terminate-instances --instance-ids ${env.INSTANCE_IDS} --query 'TerminatingInstances[*].InstanceId'
                    """
                    echo "Terminated all EC2 instances: ${env.INSTANCE_IDS}"
                }
            }
        }
    }
}
