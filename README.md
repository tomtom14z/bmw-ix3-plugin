# Plugin BMW iX3 pour Home Assistant

## Description
Plugin personnalisé pour BMW iX3 électrique permettant :
- Calculs de temps de charge dynamiques (80%, 100% à différentes puissances)
- Activités iOS Live avec mise à jour en temps réel
- Intégration avec borne V2C Trydan
- Tableau de bord personnalisé avec planification de charge
- Automatisations intelligentes de protection batterie

## Installation

1. Copiez le dossier `bmw_ix3_plugin` dans votre répertoire `custom_components` de Home Assistant
2. Redémarrez Home Assistant
3. Ajoutez l'intégration via Configuration > Intégrations
4. Configurez vos identifiants BMW Connected Drive et adresse IP V2C Trydan

## Prérequis

- BMW iX3 avec **BMW Connected Drive** OU **BMW CarData** activé
  - ⚠️ **Note importante** : Suite aux problèmes de l'API BMW Connected Drive depuis octobre 2025, il est recommandé d'utiliser **BMW CarData HA** comme alternative
  - Le plugin détecte automatiquement l'intégration disponible
- Borne V2C Trydan (optionnelle)
- Home Assistant avec accès aux intégrations personnalisées
- Application Home Assistant Companion sur iPhone (pour le widget iOS)

## Fonctionnalités

### Calculs de temps de charge
- Temps estimé pour atteindre 80% et 100%
- Calculs pour différentes puissances (3.7kW, 7.4kW, 11kW, 22kW)
- Prise en compte de la courbe de charge (ralentissement après 80%)

### Activités iOS Live
- Widget affichant le pourcentage de charge actuel
- Heure estimée d'atteinte de 80% et 100%
- Mise à jour automatique toutes les 5 minutes pendant la charge

### Intégration V2C Trydan
- Contrôle de la borne de charge
- Surveillance de la puissance de charge
- Arrêt automatique à 80% ou pourcentage personnalisé

### Tableau de bord personnalisé
- Tuile de planification avec sélection d'heure de départ
- Calcul automatique du début de charge optimal
- Affichage des temps de charge estimés
- Contrôles de la borne V2C

### Automatisations
- Arrêt automatique à 80% pour protéger la batterie
- Démarrage de charge programmé
- Notifications iOS lors des changements d'état

## Configuration

Voir le fichier `configuration.yaml` pour les exemples de configuration.

## Support

Ce plugin est développé spécifiquement pour BMW iX3 et V2C Trydan.

