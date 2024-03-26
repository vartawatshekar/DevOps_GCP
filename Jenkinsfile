pipeline {
    agent any

    environment {
        // Define the GCP project ID, Artifact Registry location, and repository name
        GCP_PROJECT_ID = 'fabhotels-development'
        ARTIFACT_REGISTRY_LOCATION = 'asia-south1'
        ARTIFACT_REGISTRY_REPOSITORY = 'webpage'
        IMAGE_NAME = 'webapp'
        IMAGE_TAG = 'latest' // or dynamically set based on your versioning scheme
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
                    sh "gcloud auth configure-docker ${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image with the appropriate tag
                    def imageName = "${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    docker.build(imageName)
                }
            }
        }

        stage('Push Image to Artifact Registry') {
            steps {
                script {
                    // Push the image to GCP Artifact Registry
                    def imageName = "${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    docker.image(imageName).push()
                }
            }
        }
        stage('Update Kustomization and Push') {
            steps {
                script {
                    // CD, run kustomize, commit, and push changes
                    sh """
                    cd /jenkins/argocd/webpage && \\
                    kustomize edit set image ${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER} && \\
                    git add . && \\
                    git commit -am "Update image tag to ${BUILD_NUMBER}" && \\
                    git push origin HEAD:master
                    """
                }
            }
        }
    }
}
