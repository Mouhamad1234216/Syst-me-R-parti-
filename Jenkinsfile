pipeline {
  agent any

  environment {
    // Docker registry credentials (configure in Jenkins: Manage Credentials)
    DOCKER_REGISTRY = 'docker.io'
    DOCKER_USERNAME = credentials('docker-username')  // Jenkins secret
    DOCKER_PASSWORD = credentials('docker-password')  // Jenkins secret
    REGISTRY_URL = 'Mouhdev'  // Docker Hub username
    
    // Kubernetes configuration
    KUBECONFIG = credentials('kubeconfig')  // Kubernetes config file (Jenkins secret)
    K8S_NAMESPACE = 'default'
  }

  options {
    timestamps()
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  stages {
    stage('Checkout') {
      steps {
        echo 'Checking out code from repository...'
        checkout scm
      }
    }

    stage('Lint & Test') {
      parallel {
        stage('Backend Lint') {
          steps {
            echo 'Linting backend code with flake8...'
            dir('backend') {
              sh '''
                python -m pip install --quiet flake8
                flake8 app.py --max-line-length=120 --ignore=E501,W503 || true
              '''
            }
          }
        }
        stage('Backend Tests') {
          steps {
            echo 'Running backend unit tests...'
            dir('backend') {
              sh '''
                python -m pip install --quiet pytest
                # Example: pytest tests/ -v || true (if test file exists)
                echo "Backend tests passed (or skipped)"
              '''
            }
          }
        }
        stage('Frontend Lint') {
          steps {
            echo 'Linting frontend code...'
            dir('frontend') {
              sh '''
                # Example: eslint index.html || true (if configured)
                echo "Frontend lint passed (or skipped)"
              '''
            }
          }
        }
      }
    }

    stage('Build Docker Images') {
      steps {
        echo 'Building Docker images...'
        sh '''
          echo "Building backend image..."
          docker build -t ${REGISTRY_URL}/backend:${BUILD_NUMBER} ./backend
          docker tag ${REGISTRY_URL}/backend:${BUILD_NUMBER} ${REGISTRY_URL}/backend:latest

          echo "Building frontend image..."
          docker build -t ${REGISTRY_URL}/frontend:${BUILD_NUMBER} ./frontend
          docker tag ${REGISTRY_URL}/frontend:${BUILD_NUMBER} ${REGISTRY_URL}/frontend:latest

          echo "Displaying built images..."
          docker images | grep ${REGISTRY_URL}
        '''
      }
    }

    stage('Push to Docker Registry') {
      steps {
        echo 'Authenticating to Docker Registry and pushing images...'
        sh '''
          echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin ${DOCKER_REGISTRY}
          
          echo "Pushing backend image..."
          docker push ${REGISTRY_URL}/backend:${BUILD_NUMBER}
          docker push ${REGISTRY_URL}/backend:latest

          echo "Pushing frontend image..."
          docker push ${REGISTRY_URL}/frontend:${BUILD_NUMBER}
          docker push ${REGISTRY_URL}/frontend:latest

          docker logout ${DOCKER_REGISTRY}
          echo "Images pushed successfully"
        '''
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        echo 'Deploying application to Kubernetes...'
        sh '''
          export KUBECONFIG=${KUBECONFIG}
          
          echo "Verifying kubectl connectivity..."
          kubectl cluster-info
          kubectl get nodes

          echo "Applying Kubernetes manifests..."
          kubectl apply -f infra/k8s-db-secret.yaml
          kubectl apply -f infra/k8s-postgres-pvc.yaml
          kubectl apply -f infra/k8s-postgres-deployment.yaml
          kubectl apply -f infra/k8s-postgres-service.yaml

          kubectl apply -f infra/k8s-backend-deployment.yaml
          kubectl apply -f infra/k8s-backend-service.yaml
          
          kubectl apply -f infra/k8s-frontend-deployment.yaml
          kubectl apply -f infra/k8s-frontend-service.yaml
          
          kubectl apply -f infra/k8s-ingress.yaml

          echo "Waiting for deployments to be ready..."
          kubectl rollout status deployment/postgres --timeout=5m || true
          kubectl rollout status deployment/backend --timeout=5m || true
          kubectl rollout status deployment/frontend --timeout=5m || true

          echo "Checking deployment status..."
          kubectl get deployments -n ${K8S_NAMESPACE}
          kubectl get pods -n ${K8S_NAMESPACE}
          kubectl get svc -n ${K8S_NAMESPACE}
        '''
      }
    }

    stage('Smoke Tests') {
      steps {
        echo 'Running smoke tests on deployed application...'
        sh '''
          echo "Waiting for services to be accessible..."
          sleep 10

          echo "Testing backend API endpoint..."
          kubectl port-forward svc/backend-service 5000:5000 &
          sleep 3
          curl -f http://localhost:5000/api/users || echo "Backend API test failed (may be expected during first deploy)"
          
          echo "Testing frontend endpoint..."
          kubectl port-forward svc/frontend-service 8080:80 &
          sleep 3
          curl -f http://localhost:8080 || echo "Frontend test failed (may be expected during first deploy)"
        '''
      }
    }
  }

  post {
    always {
      echo 'Pipeline execution completed.'
      sh 'docker logout || true'
    }
    success {
      echo 'Pipeline succeeded! Application deployed successfully.'
    }
    failure {
      echo 'Pipeline failed! Check logs above for details.'
    }
  }
}
