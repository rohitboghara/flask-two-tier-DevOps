pipeline {
    agent any

    environment {
        DOCKERAPP_NAME = "root938/flask-two-tier-web"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/rohitboghara/flask-two-tier-DevOps.git'
            }
        }

        stage('Build Code') {
            steps {
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

        stage('Docker Push') {
            steps {
                sh '''
                docker tag flask-test:latest ${DOCKERAPP_NAME}:1.1
                docker push ${DOCKERAPP_NAME}:1.1
                '''
            }
        }

        stage('Deploy Web') {
            steps {
                sh '''
                docker compose down -v
                docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            emailext(
                subject: "Jenkins SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
                body: """
                <h2>Build Successful</h2>
                <p><b>Job:</b> ${JOB_NAME}</p>
                <p><b>Build Number:</b> ${BUILD_NUMBER}</p>
                <p><b>Status:</b> SUCCESS</p>
                <p><b>Docker Image:</b> ${DOCKERAPP_NAME}:1.1</p>
                <p><a href="${BUILD_URL}">View Build Logs</a></p>
                """,
                mimeType: 'text/html',
                to: "gitlabtest321@gmail.com"
            )
        }

        failure {
            emailext(
                subject: "Jenkins FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
                body: """
                <h2>Build Failed </h2>
                <p><b>Job:</b> ${JOB_NAME}</p>
                <p><b>Build Number:</b> ${BUILD_NUMBER}</p>
                <p><b>Status:</b> FAILED</p>
                <p>Please check logs:</p>
                <p><a href="${BUILD_URL}">View Build Logs</a></p>
                """,
                mimeType: 'text/html',
                to: "gitlabtest321@gmail.com"
            )
        }
    }
}

