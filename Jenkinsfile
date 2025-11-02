pipeline {
    agent any

    environment {
        APP_NAME = 'lab2-python-app'
        DOCKER_IMAGE = 'python:3.9-slim'
        VENV_PATH = 'venv'
        IMAGE_TAG = 'latest'
    }

    stages {

        stage('Checkout Repository') {
            steps {
                echo ' Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                echo ' Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo ' Running unit tests...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Static Analysis (Bandit)') {
            steps {
                echo ' Running Bandit security scan...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    bandit -r . -x ${VENV_PATH} -f html -o bandit_report.html || true
                '''
                echo ' Bandit report saved as bandit_report.html'
            }
        }

        stage('Dependency Vulnerability Scan (Safety)') {
            steps {
                echo ' Checking Python dependencies for vulnerabilities using Safety...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    safety check || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo ' Building Docker image...'
                sh '''
                    if ! command -v docker &> /dev/null
                    then
                        echo " Docker not found on this agent. Skipping build."
                    else
                        sudo docker build -t ${APP_NAME}:${IMAGE_TAG} .
                    fi
                '''
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                echo 'Scanning Docker image with Trivy...'
                sh '''
                    if command -v trivy &> /dev/null
                    then
                        trivy image --severity HIGH,CRITICAL ${APP_NAME}:${IMAGE_TAG} || true
                    else
                        echo " Trivy not installed. Skipping vulnerability scan."
                    fi
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo ' Deploying Docker container...'
                sh '''
                    if command -v docker &> /dev/null
                    then
                        sudo docker rm -f ${APP_NAME} || true
                        sudo docker run -d -p 5000:5000 --name ${APP_NAME} ${APP_NAME}:${IMAGE_TAG}
                    else
                        echo " Docker not available, skipping deployment."
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo ' Pipeline completed successfully! '
        }
        failure {
            echo ' Pipeline failed. Please check the logs above.'
        }
        always {
            echo ' Cleaning workspace...'
            cleanWs()
        }
    }
}
