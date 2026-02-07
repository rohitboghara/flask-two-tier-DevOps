pipeline {
    agent { label 'agent2' }
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
       stage('Deploy Kube'){
           steps {
               sh '''
               
               kubectl apply -f kubernetes/namespace.yml -f kubenetes/postgres-deployment.yml
               kubectl apply -f kubernetes/flask-web-deployment.yml
               echo "Waiting for flask-web deployment..."
               kubectl rollout status deployment/flask-web -n flask-app
               echo "Starting port forward..."
 
               nohup kubectl port-forward -n flask-app svc/flask-service 5000:5000 --address=0.0.0.0 > port-forward.log 2>&1 &
               
               '''
           }
       }
    }
}
