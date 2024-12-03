Assuming:
- Your terminal location is `~`
- The `.pem` file is called `jenkins-test.pem` and is saved in the Downloads folder

## Copy the source files to Jenkins:
```
scp -i "Downloads/jenkins-test.pem" ~/Documents/Projects/world-scraper ubuntu@ec2-3-82-112-24.compute-1.amazonaws.com:~
```

## SSH into Jenkins:
```
ssh -i "Downloads/jenkins-test.pem" ubuntu@ec2-3-82-112-24.compute-1.amazonaws.com
```

## Other:
#### When inside the Jenkins server, remove the `.git` subfolder
```
rm -rf world-scraper/.git
```
#### Then copy it to the Jenkins folder
```
sudo cp world-scraper /var/lib/jenkins
```