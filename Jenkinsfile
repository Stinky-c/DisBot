pipeline {
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