pipeline {

	agent any 

	environment {
	    APP_NAME="e-ecom"
	    IMAGE_NAME="ohadd306/e-ecom"
	    IMAGE_TAG="${BUILD_NUMBER}"
	    APP_PORT="8000"
	}

	stages {

		stage("checkout") {
		    steps {
                     checkout scm 
		    }
		}
		stage("unit tests") {
		   steps {
                      echo "starting unit tests"
                      sh '''
                      python3 -m pytest -v 
		      '''
                   }
		}
		stage("code quality") {
                   steps {
                           echo "run code quality check"
                   sh '''
                   set -eu
                   python3.11 -m pip install -r requirements.txt
                   python3.11 -m pip install ruff pip-audit pytest-cov
                   ruff check app tests
                   ''' 
		   }
		   
		}
                stage("build docker image") {
		    steps {
                         echo "build docker image"
                         sh '''
                         docker build -t ${IMAGE_NAME}:${IMAGE_TAG}   .  
			 '''
		    }
		}
		stage("test docker image") {
		    steps {
                        echo "test docker image"
		        sh '''
			docker run -d --name ${APP_NAME}-test -p 8002:${APP_PORT} ${IMAGE_NAME}:${IMAGE_TAG}
			'''
			echo "wait for app to start"
			sleep 5 
			sh '''
			curl -f http://localhost:8002/health
                        curl -f  -X POST  -H "Content-Type: application/json" -d '{"product_id":1,"quantity":3}' http://localhost:8002/orders/
                        curl -f http://localhost:8002/products/1
			'''
		    }
                   post {
                       always {
			echo "remove test image docker container "
			sh '''
                        docker stop ${APP_NAME}-test || true
			docker rm -f ${APP_NAME}-test  || true 
			'''
                       } 
		   }
		}

// push docker image

               stage('Push to Docker Hub') {

                   steps {

                       echo "Logging into Docker Hub..."

                       withCredentials([
                            usernamePassword(
                                credentialsId: 'dockerhub-creds',
                                usernameVariable: 'DOCKER_USERNAME',
                                passwordVariable: 'DOCKER_PASSWORD'
                            )
                        ]) {

                            sh '''
                                echo "$DOCKER_PASSWORD" | \
                                docker login \
                                -u "$DOCKER_USERNAME" \
                                --password-stdin

                                docker push \
                                   ${IMAGE_NAME}:${IMAGE_TAG}

                                docker logout
                           '''
                        } 
                    }
                }
		stage("deploy on stg") {
			steps {
                           echo "deploy app on stg"
                           sh '''
			   docker stop ${APP_NAME}-stg || true
			   docker rm -f ${APP_NAME}-stg || true 
			   docker pull ${IMAGE_NAME}:${IMAGE_TAG}
			   docker run -d --name ${APP_NAME}-stg -p 8001:8000 ${IMAGE_NAME}:${IMAGE_TAG}  
			   '''
			}
		}
		stage("test stg") {
			steps {
				echo "wait for app to start"
				sleep 5
				echo "stg health-check"
				sh '''
				curl -f http://localhost:8001/health
				curl -f http://localhost:8001/products/1
				curl -f  -X POST  -H "Content-Type: application/json" -d '{"product_id":1,"quantity":3}' http://localhost:8001/orders/
				'''
			}
		}
		stage("deploy on PRD")  {
			steps {
			   echo "deploy app on prd"
			   sh '''
			   docker stop ${APP_NAME} || true
			   docker rm -f ${APP_NAME}  || true
			   docker run -d --name ${APP_NAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE_NAME}:${IMAGE_TAG}   
			   '''
			}
		}
		stage("test PRD health check")


			





	}



}
