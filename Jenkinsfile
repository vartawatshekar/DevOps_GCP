pipeline {
    agent any
    parameters {
        string(defaultValue: '', description: 'What is my Project ID?', name: 'GCP_PROJECT_ID', trim: false)
        string(defaultValue: '', description: 'What is my Artifact Repository Name?', name: 'ARTIFACT_REGISTRY_REPOSITORY', trim: false)
        string(defaultValue: '', description: 'What is my Image Name?', name: 'IMAGE_NAME', trim: false)

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
                    echo ${ARTIFACT_REGISTRY_REPOSITORY}
                    cd /jenkins/argocd/webpage && \\
                    git pull && \\
                    kustomize edit set image asia-south1-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPOSITORY}/${IMAGE_NAME}:${BUILD_NUMBER} && \\
                    git add . && \\
                    git commit -am "Update image tag to ${BUILD_NUMBER}" && \\
                    git push origin HEAD:main
                    """
                }
            }
        }
    }
}
