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

        stage('Verify Python') {
            steps {
                bat 'python --version'
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

        stage('Verify DRF') {
            steps {
                bat '%VENV%\\Scripts\\pip show djangorestframework'
            }
        }

        // add stages for mysql client
        stage('Database Setup') {
            steps {
                bat '''
                %VENV%\\Scripts\\pip show mysqlclient || %VENV%\\Scripts\\pip install mysqlclient
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

        // stage to check simple jwt and argon2
        stage('Verify JWT and Argon2') {
            steps {
                bat '''
                %VENV%\\Scripts\\pip show djangorestframework-simplejwt || %VENV%\\Scripts\\pip install djangorestframework-simplejwt
                %VENV%\\Scripts\\pip show argon2-cffi || %VENV%\\Scripts\\pip install argon2-cffi
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
