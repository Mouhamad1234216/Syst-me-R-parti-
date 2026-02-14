Projet Système Réparti — Déploiement Web avec Docker, Kubernetes, Ansible et Jenkins
1. Description

Ce projet consiste à déployer une application web répartie composée de :

Frontend : Angular/React servie via Nginx

Backend : API REST Flask connectée à PostgreSQL

Base de données : PostgreSQL

Infrastructure : Conteneurisation Docker, orchestration Kubernetes, automatisation Ansible et pipeline CI/CD Jenkins

Objectif pédagogique : démontrer la maîtrise des technologies DevOps modernes pour déployer une application microservices.

2. Arborescence du projet
ProjetSystemRepartie/
├── ansible/
│   ├── inventory.ini
│   └── playbook.yml
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── seed.py
├── frontend/
│   ├── index.html
│   ├── Dockerfile
│   └── default.conf
├── infra/
│   ├── k8s-backend-deployment.yaml
│   ├── k8s-backend-service.yaml
│   ├── k8s-frontend-deployment.yaml
│   ├── k8s-frontend-service.yaml
│   ├── k8s-db-secret.yaml
│   ├── k8s-ingress.yaml
│   ├── k8s-postgres-deployment.yaml
│   ├── k8s-postgres-service.yaml
│   └── k8s-postgres-pvc.yaml
├── docker-compose.yml
├── Jenkinsfile
├── REPORT.md
└── README.md

3. Prérequis

Docker et Docker Compose

Kubernetes / Minikube (local) ou cluster distant

Ansible 2.12+ et Python

Accès root ou sudo sur la machine cible

4. Déploiement avec Ansible

Le playbook Ansible automatise :

Installation Docker et Docker Compose

Installation kubectl

Installation Minikube (optionnel pour local)

Construction des images Docker (backend et frontend)

Déploiement des manifests Kubernetes (Secrets, PVC, Deployments, Services, Ingress)

Vérification du déploiement (pods et services)

Commandes

Sur une machine locale (Linux/Ubuntu) :

cd ansible/
ansible-playbook -i inventory.ini playbook.yml


Sur une machine distante via SSH :

Modifier inventory.ini pour ajouter l’IP du cluster :

[kubernetes_cluster]
192.168.1.100 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa


Lancer le playbook :

ansible-playbook -i inventory.ini playbook.yml

5. Vérification

Vérifier que les pods sont en Running :

kubectl get pods


Vérifier les services exposés :

kubectl get svc


Accéder au frontend via Minikube :

minikube service frontend-service


Tester l’API backend via le frontend /api/*

6. Construction et tests locaux avec Docker Compose

Build et lancement :

docker-compose build
docker-compose up -d


Vérifier les services :

docker-compose ps


Tester les endpoints API :

curl http://localhost:5000/api/users
curl http://localhost:8080/api/users

7. Variables personnalisables

kubectl_version : version kubectl à installer (défaut v1.27.0)

minikube_version : version Minikube (défaut v1.31.2)

8. Bonnes pratiques

Minikube utilise son propre Docker interne, utiliser eval $(minikube docker-env) si nécessaire

Ne jamais exposer directement les secrets en production

Backend protégé derrière le frontend pour plus de sécurité

Préparer la réplication PostgreSQL pour la production

9. CI/CD (Jenkins)

Pipeline défini dans Jenkinsfile : linting, tests, build Docker, push sur Docker Hub, déploiement K8s

Jenkins peut être installé via Ansible ou Docker

10. Contact

Auteur : [Ton nom]

Email : [Ton email]