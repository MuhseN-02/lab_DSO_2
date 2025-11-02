pipeline {
    agent any

    environment {
        PYTHON_IMAGE = 'python:3.12-slim'
        IMAGE_NAME = 'arithmetic-api'
        DOCKERHUB_USER = 'muhsen02'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh './venv/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'source ./venv/bin/activate && pytest -v --maxfail=1 --disable-warnings'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    sh 'source ./venv/bin/activate && python -m bandit -r . -x ./venv -f html -o bandit_report.html'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh '''
                        CONTAINER_ID=$(docker ps -q --filter ancestor=${IMAGE_NAME})
                        if [ ! -z "$CONTAINER_ID" ]; then
                            docker stop $CONTAINER_ID
                            docker rm $CONTAINER_ID
                        fi
                        docker run -d -p 5000:5000 ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Push Docker Image (Optional)') {
            steps {
                script {
                    sh """
                        docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
        success {
            echo '✅ Lab2 DevSecOps pipeline completed successfully!'
        }
        failure {
            echo '❌ Lab2 DevSecOps pipeline failed!'
        }
    }
}
