pipeline {
    agent any

    environment {
        APP_NAME = 'lab2-python-app'
        DOCKER_IMAGE = 'python:3.9-slim'
        VENV_PATH = 'venv'
    }

    stages {

        stage('Checkout Repository') {
            steps {
                echo ' Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Set Up Environment') {
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
                echo ' Running tests...'
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
                echo 'Bandit scan completed (report saved as bandit_report.html)'
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
                        sudo docker build -t ${APP_NAME}:latest .
                    fi
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo ' Deploying container...'
                sh '''
                    if command -v docker &> /dev/null
                    then
                        sudo docker run -d -p 5000:5000 --name ${APP_NAME} ${APP_NAME}:latest || true
                    else
                        echo " Docker not available, skipping deployment."
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo ' Pipeline completed successfully!'
        }
        failure {
            echo ' Pipeline failed. Check the logs above.'
        }
        always {
            echo ' Cleaning workspace...'
            cleanWs()
        }
    }
}
