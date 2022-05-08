pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                pip "install -r requirements.txt"
            }
        }
        stage('Deploy') { 
            steps {
                echo "Deployed"
            }
        }
    }
}