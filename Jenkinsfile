pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main',
                url: 'https://github.com/mlibinanto/jenk.git'
            }
        }

        stage('Create Virtualenv') {
            steps {
                bat '''
                python -m venv %VENV%
                %VENV%\\Scripts\\pip install --upgrade pip
                %VENV%\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Migrate') {
            steps {
                bat '''
                %VENV%\\Scripts\\python manage.py migrate
                '''
            }
        }

        stage('Collect Static') {
            steps {
                bat '''
                %VENV%\\Scripts\\python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Run Server (Test)') {
            steps {
                bat '''
                echo Django build successful
                '''
            }
        }
    }
}
