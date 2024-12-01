pipeline {
    agent any

    parameters {
        string(name: 'INSTANCE_COUNT', defaultValue: '3', description: 'Number of EC2 instances to deploy')
        string(name: 'REPO_URL', defaultValue: 'https://github.com/your/repo.git', description: 'Git repository URL')
        string(name: 'SCRIPT_NAME', defaultValue: 'script.py', description: 'Python script to execute')
        string(name: 'INSTANCE_TYPE', defaultValue: 't2.micro', description: 'EC2 Instance Type')
        string(name: 'INSTANCE_SECURITY_GROUP', defaultValue: 'sg-02ca8252d2971d420', description: 'EC2 Security Group')
        string(name: 'AMI_ID', defaultValue: 'ami-0866a3c8686eaeeba', description: 'Amazon Machine Image (AMI) ID')
        string(name: 'KEY_NAME', defaultValue: 'jenkins-test', description: 'Key pair for SSH access')
        string(name: 'PEM_FILE_PATH', defaultValue: '/jenkins.pem', description: 'Path to the PEM file for SSH access')
    }

    stages {
        // stage('Launch EC2 Instances') {
        //     steps {
        //         script {
        //             def stdOutput = sh(
        //                 script: """
        //                 aws ec2 run-instances \
        //                     --image-id ${params.AMI_ID} \
        //                     --instance-type ${params.INSTANCE_TYPE} \
        //                     --key-name ${params.KEY_NAME} \
        //                     --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-021176b1e05cb6895","VolumeSize":8,"VolumeType":"gp3","Throughput":125}}' \
        //                     --network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["${params.INSTANCE_SECURITY_GROUP}"]}' \
        //                     --credit-specification '{"CpuCredits":"standard"}' \
        //                     --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"WorldScraper"}]}' \
        //                     --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
        //                     --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
        //                     --count ${params.INSTANCE_COUNT} \
        //                     --query "Instances[*].InstanceId" \
        //                     --output text
        //                 """,
        //                 returnStdout: true
        //             ).trim()
        //             def instanceIds = stdOutput.split().join(' ')
        //             env.INSTANCE_IDS = instanceIds
        //             echo "Launched instance IDs: ${instanceIds}"
        //         }
        //     }
        // }
        stage('SSH into ec2 instances') {
            steps {
                script {
                    env.INSTANCE_IDS = "i-0c260cc6049e0816d i-0c55d0c672d4297cf i-04c3a69fd6fdfb03a"
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
                    
                    sshagent(credentials: ['jenkins-world-scraper-ec2-key']) {
                    publicDnsNames.each { publicDnsName ->
                        echo "SSHing into: ${publicDnsName}"

                        // SSH into the instance and check Python version
                        //! run src/main.py
                        //! Add a new stage for terminating all instance IDs
                        def sshStdOutput = sh(
                            script:"""
                            scp -o StrictHostKeyChecking=no -r ~/world-scraper ubuntu@${publicDnsName}:~/
                            ssh -o StrictHostKeyChecking=no ubuntu@${publicDnsName} "sh ~/world-scraper/start.sh"
                            """,
                            returnStdout: true
                        )
                        echo "Result: ${sshStdOutput}"
                    }
                    }
                }
            }
        }
    }
}
