pipeline {
    agent any

    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/MuhseN-02/lab_DSO_2.git']]
                ])
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
                    sh './venv/bin/pytest -v --maxfail=1 --disable-warnings'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    sh '''
                        ./venv/bin/python -m bandit -r . -x ./venv -f html -o bandit_report.html || true
                    '''
                    echo "Bandit analysis finished (see bandit_report.html)."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Use sudo to avoid permission issues
                    sh "sudo docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh "sudo docker run -d -p 5000:5000 ${IMAGE_NAME}"
                }
            }
        }

        stage('Push Docker Image (Optional)') {
            steps {
                script {
                    echo "Optional stage: Docker push can be added here"
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
