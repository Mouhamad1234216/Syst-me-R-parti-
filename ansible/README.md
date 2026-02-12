# Ansible Configuration for Projet Système Réparti

## Overview
Ce playbook Ansible automatise l'installation et le déploiement de l'application sur une machine ou un cluster Kubernetes.

## Sections du playbook

### 1. Installation Docker & Docker Compose
- Ajoute les dépôts et GPG keys Docker
- Installe Docker CE et docker-compose via pip
- Démarre et active le service Docker

### 2. Installation kubectl
- Télécharge kubectl (v1.27.0 par défaut)
- Vérifie l'installation

### 3. Installation Minikube (optionnel)
- Pour clusters Kubernetes locaux
- Télécharge Minikube et vérifie l'installation

### 4. Construction des images Docker
- Copie les fichiers du projet dans `/opt/projet-systeme-repartie`
- Construit les images `Mouhdev/backend:latest` et `Mouhdev/frontend:latest`

### 5. Déploiement des manifests Kubernetes
- Applique Secret K8s (`k8s-db-secret.yaml`)
- Applique PVC pour PostgreSQL (`k8s-postgres-pvc.yaml`)
- Déploie PostgreSQL, backend, frontend et leurs services
- Applique l'Ingress pour accès HTTP

### 6. Vérification du déploiement
- Attente des déploiements (rollout status)
- Affichage de l'état des pods et services

## Utilisation

### Sur une machine locale (Linux/Ubuntu)
```bash
cd ansible/
ansible-playbook -i inventory.ini playbook.yml
```

### Sur une machine distante via SSH
1. Édite `inventory.ini` et ajoute l'IP/hostname :
```ini
[kubernetes_cluster]
192.168.1.100 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
```

2. Exécute :
```bash
ansible-playbook -i inventory.ini playbook.yml
```

### Variables personnalisables
- `kubectl_version` : version kubectl à installer (défaut: v1.27.0)
- `minikube_version` : version Minikube (défaut: v1.31.2)

## Prérequis
- Machine cible : Debian/Ubuntu
- Accès root ou sudo
- Python + Ansible installés localement

## Prochaines étapes
- Compléter le déploiement Jenkins pour la CI/CD
- Configurer les secrets en production (ne pas utiliser `stringData`)
- Mettre en place les configurations de réplication PostgreSQL
