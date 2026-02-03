pipeline {
    agent any
    environment{
        DOCKERAPP_NAME = "root938/flask-two-tier-web"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                  url: 'https://github.com/rohitboghara/flask-two-tier-DevOps.git'
            }
        }
       stage('Build Code'){
           steps{
           sh 'docker build -t flask-test:latest .'

       }
       }
       stage('Docker Login') {
         steps {
             withCredentials([usernamePassword(
                credentialsId: 'dockerhub-creds',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )]) {
                sh '''
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                '''
            }
         }
    }
       stage('Docker Push'){
           steps {
               sh '''
               docker tag flask-test:latest ${DOCKERAPP_NAME}:1.1
               docker push ${DOCKERAPP_NAME}:1.1
               '''
           }
       }
       stage('Deploy Web'){
           steps {
               sh '''
               docker compose down -v
               docker compose up -d
               '''
           }
       }
    }
}
