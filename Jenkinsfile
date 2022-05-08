pipeline {
    agent { docker { image 'python:3.10.1-alpine' } }
    stages {
        stage('Build') { 
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('Deploy') { 
            steps {
                sh "pip freeze"
            }
        }
    }
}