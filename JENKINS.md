# Pipeline CI/CD Jenkins pour Projet Système Réparti

## Overview
Ce `Jenkinsfile` décrit un pipeline complet de CI/CD :
1. **Checkout** : récupère le code depuis le repo Git
2. **Lint & Test** : exécute flake8 pour le backend, eslint pour le frontend (optionnel)
3. **Build** : construit les images Docker pour backend et frontend
4. **Push** : pousse les images vers Docker Hub (ou registre privé)
5. **Deploy** : applique les manifests Kubernetes et attend la convergence
6. **Smoke Tests** : vérifie que l'application est accessible post-déploiement

## Configuration Jenkins requise

### 1. Credentials (Manage Jenkins > Credentials)
Crée les secrets suivants :
- `docker-username` : ton username Docker Hub
- `docker-password` : ton token/password Docker Hub
- `kubeconfig` : le contenu de ton fichier `~/.kube/config` (base64 ou fichier)

### 2. Pipeline Job
Crée un nouveau **Pipeline** job dans Jenkins :
- **Pipeline script from SCM** : Git
- **Repository URL** : `https://github.com/Mouhamad1234216/Syst-me-R-parti-.git`
- **Branch** : `main`
- **Script path** : `Jenkinsfile`

### 3. Plugins Jenkins requis
- Pipeline
- Docker
- Kubernetes
- Credentials Binding

## Stages détaillés

### Checkout
Clone le repo Git et prépare le workspace.

### Lint & Test (parallèles)
- **Backend Lint** : flake8 sur `app.py`
- **Backend Tests** : pytest (si tests existent)
- **Frontend Lint** : eslint (optionnel)

### Build Docker Images
Construit 2 images avec tags :
- `Mouhdev/backend:${BUILD_NUMBER}` et `:latest`
- `Mouhdev/frontend:${BUILD_NUMBER}` et `:latest`

### Push to Docker Registry
1. Authentifie auprès de Docker Hub
2. Pousse les images
3. Se déconnecte

### Deploy to Kubernetes
1. Vérifie l'accès au cluster (`kubectl cluster-info`)
2. Applique les manifests K8s (Secret, PVC, Deployments, Services, Ingress)
3. Attend la convergence des deployments (5min timeout)
4. Affiche l'état final (pods, services)

### Smoke Tests
Teste les endpoints après déploiement :
- `http://localhost:5000/api/users` (backend)
- `http://localhost:8080` (frontend)

## Variables d'environnement
- `BUILD_NUMBER` : numéro de build Jenkins
- `DOCKER_REGISTRY` : registre Docker (docker.io)
- `REGISTRY_URL` : namespace Docker Hub (Mouhdev)
- `K8S_NAMESPACE` : namespace Kubernetes (default)

## Utilisation (exécution manuelle)
```
Jenkins Web UI → Build Now
```

## Améliorations futures
- Intégrer des tests d'intégration complets
- Ajouter des métriques de santé des déploiements
- Notifications Slack/Email sur succès/échec
- Rollback automatique en cas d'erreur
- Déploiement blue-green ou canary
- Gestion des environnements (dev, staging, prod)
