pipeline {
    agent any
    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'lab2-devsecops-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh './venv/bin/pip install -r requirements.txt'
                    // Ensure Bandit and its dependencies are installed
                    sh './venv/bin/pip install bandit pbr'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh './venv/bin/pytest'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    sh './venv/bin/python -m bandit -r .'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh 'docker-compose up -d'
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
            echo '✅ Lab2 build completed successfully!'
        }
        failure {
            echo '❌ Lab2 build failed!'
        }
    }
}
