pipeline {
    agent any
    parameters {
        string(defaultValue: '', description: 'What is my Project ID?', name: 'GCP_PROJECT_ID', trim: false)
        string(defaultValue: '', description: 'What is my Artifact Repository Name?', name: 'ARTIFACT_REGISTRY_REPOSITORY', trim: false)
        string(defaultValue: '', description: 'What is my Image Name?', name: 'IMAGE_NAME', trim: false)
        string(defaultValue: '', description: 'What is my Environment?', name: 'ENV_NAME', trim: false)

    }

    environment {
        // Define the GCP project ID, Artifact Registry location, and repository name
        APPLICATION_NAME = ${ARTIFACT_REGISTRY_REPOSITORY}
        DEPLOYMENT_IMAGE = 'asia-south1-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER}'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Check out code from source control
                checkout scm
            }
        }
        
        stage('Authorize gcloud') {
            steps {
                script {
                    // Authenticate to GCP
                    // Make sure Jenkins has configured gcloud CLI and has appropriate permissions
                    sh "gcloud auth configure-docker asia-south1-docker.pkg.dev"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image with the appropriate tag
                    def imageName = "asia-south1-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    docker.build(imageName)
                }
            }
        }

        stage('Push Image to Artifact Registry') {
            steps {
                script {
                    // Push the image to GCP Artifact Registry
                    def imageName = "asia-south1-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    docker.image(imageName).push()
                }
            }
        }
        stage('Update Kustomization and Push') {
            steps {
                script {
                    // CD, run kustomize, commit, and push changes
                    sh """
                    cd /jenkins/argo-cd-configs/patch && \\
                    git pull && \\
                    sed "s/\${APPLICATION_NAME}/$APPLICATION_NAME/g; s/\${DEPLOYMENT_IMAGE}/$DEPLOYMENT_IMAGE/g; s/\${ENV_NAME}/$ENV_NAME/g" vars.txt > ${APPLICATION_NAM}_vars.txt && \\
                    ./update_patch.sh /jenkins/argo-cd-configs/${APPLICATION_NAME}/overlays/${ENV_NAME} kustomization.yaml deployment_patch.json hpa_patch.json service_patch.json ${APPLICATION_NAM}_vars.txt && \\
                    git add . && \\
                    git commit -am "Update image tag to ${BUILD_NUMBER}" && \\
                    git push origin HEAD:main
                    """
                }
            }
        }
    }
}
