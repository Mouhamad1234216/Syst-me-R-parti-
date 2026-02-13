1. Introduction

Objectif du projet : Déployer une application web répartie composée d’un frontend, d’une API backend et d’une base PostgreSQL, avec conteneurisation, orchestration Kubernetes, automatisation Ansible et pipeline CI/CD Jenkins.

Auteur :

Date :

2. Énoncé (extrait)

Déploiement d’une Application Web Répartie avec Docker, Kubernetes, Ansible et Jenkins

3. Travaux réalisés (résumé)

Conception : schéma de l’architecture (à ajouter)

Développement : frontend statique et API Flask avec modèles User et Product (backend/app.py)

Conteneurisation : frontend/Dockerfile, backend/Dockerfile, docker-compose.yml

Orchestration local : tests via docker-compose (services db, backend, frontend)

Intégration frontend↔backend : Nginx proxy /api → backend (frontend/default.conf corrigé avec backend-service)

Seed de la DB : backend/seed.py insère des données d’exemple

Infrastructure K8s : manifests dans infra/ (Deployments + Services + PVC + Secret)

Automatisation : ansible/playbook.yml (ébauche)

CI/CD : Jenkinsfile (squelette)

4. Fichiers ajoutés / modifiés

PLAN.md, REPORT.md

frontend/index.html, frontend/Dockerfile, frontend/default.conf

backend/app.py, backend/Dockerfile, backend/requirements.txt, backend/seed.py

docker-compose.yml

infra/k8s-backend-deployment.yaml, infra/k8s-backend-service.yaml

infra/k8s-frontend-deployment.yaml, infra/k8s-frontend-service.yaml

infra/k8s-postgres-deployment.yaml, infra/k8s-postgres-service.yaml, infra/k8s-postgres-pvc.yaml, infra/k8s-db-secret.yaml

infra/k8s-ingress.yaml

ansible/playbook.yml, Jenkinsfile, .gitignore, README.md

5. Commandes exécutées (preuves)
Initialisation Git & push
git init -b main
git add .
git commit -m "Initial scaffold"
git remote add origin <repo_url>
git push -u origin main

Construction et lancement local (Docker Compose)
docker-compose build
docker-compose up --build -d
docker-compose ps
docker-compose logs --tail=50 backend

Tester les endpoints localement
Invoke-RestMethod http://localhost:5000/api/users
Invoke-RestMethod http://localhost:8080
Invoke-RestMethod http://localhost:8080/api/users

6. Détails techniques et choix

Backend : Flask + SQLAlchemy — simple et rapide à mettre en place

Base de données : PostgreSQL — robuste et compatible Kubernetes

Frontend : page statique servie par Nginx + proxy /api vers backend-service

Conteneurisation : Dockerfiles séparés, orchestration locale via docker-compose

Déploiement cible : Kubernetes (manifests fournis avec Services, PVC, Secret)

7. Tests réalisés
7.1 Pods Kubernetes

Commande :

kubectl get pods


Capture à insérer ici :

NAME                        READY   STATUS    RESTARTS   AGE
backend-6bb89c78f-ft6ng     1/1     Running   0          6m49s
frontend-7f9589fbff-c8d9r   1/1     Running   0          31s
postgres-7994c856-9dh86     1/1     Running   0          14m

7.2 Services Kubernetes

Commande :

kubectl get svc


Capture à insérer ici :

NAME               TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
backend-service    ClusterIP      10.104.155.142  <none>        5000/TCP       6m30s
frontend-service   LoadBalancer   10.107.240.124  <pending>     80:31579/TCP   6m3s
postgres-service   ClusterIP      10.96.41.96     <none>        5432/TCP       14m

7.3 Frontend dans le navigateur

Commande :

minikube service frontend-service


Capture à insérer ici :

Screenshot de la page frontend affichant les données récupérées via l’API backend

7.4 Logs Backend

Commande :

kubectl logs backend-6bb89c78f-ft6ng


Capture / texte à insérer ici :

Database ready and tables created
* Running on http://0.0.0.0:5000

7.5 Logs Frontend (optionnel)

Commande :

kubectl logs frontend-7f9589fbff-c8d9r


Texte à insérer si besoin :

[Startup Nginx] Configuration complete; ready for start up

8. Points restants (plans d'action)

Compléter playbook Ansible pour automatiser :

Installation Docker, Kubernetes, Minikube

Déploiement des manifests K8s

Déploiement Jenkins

Compléter Jenkinsfile pour pipeline complet : lint → test → build → push → déploiement

Générer PDF final ≤10 pages avec captures

9. Annexes

Ajouter ici captures d’écran terminal et navigateur

Ajouter logs backend / frontend complets si nécessaire pour preuve technique