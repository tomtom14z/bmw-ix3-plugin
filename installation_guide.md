# Guide d'installation - Plugin BMW iX3 pour Home Assistant

## Prérequis

### Matériel requis
- BMW iX3 avec BMW Connected Drive activé
- Borne de recharge V2C Trydan compatible Home Assistant
- Home Assistant (version 2023.1 ou plus récente)
- iPhone avec l'application Home Assistant Companion

### Comptes et accès
- Compte BMW Connected Drive avec accès à l'API
- Accès administrateur à votre borne V2C Trydan
- Accès administrateur à votre instance Home Assistant

## Installation étape par étape

### 1. Préparation de l'environnement

#### 1.1 Accès SSH à Home Assistant
```bash
# Si vous utilisez Home Assistant OS
ha ssh

# Si vous utilisez Home Assistant Supervised
ssh root@votre-ip-homeassistant
```

#### 1.2 Création du répertoire custom_components
```bash
# Naviguer vers le répertoire de configuration
cd /config

# Créer le répertoire custom_components s'il n'existe pas
mkdir -p custom_components

# Naviguer dans le répertoire
cd custom_components
```

### 2. Installation du plugin

#### 2.1 Téléchargement du plugin
```bash
# Cloner le plugin (remplacez par votre URL de repository)
git clone https://github.com/votre-username/bmw-ix3-plugin.git bmw_ix3_plugin

# Ou copier manuellement les fichiers
# Copiez tous les fichiers du plugin dans /config/custom_components/bmw_ix3_plugin/
```

#### 2.2 Vérification de la structure
```bash
# Vérifier que la structure est correcte
ls -la bmw_ix3_plugin/
# Vous devriez voir :
# __init__.py
# manifest.json
# config_flow.py
# const.py
# coordinator.py
# services.py
# sensor/
# switch/
# number/
# README.md
```

### 3. Configuration des secrets

#### 3.1 Création du fichier secrets.yaml
```bash
# Créer le fichier secrets.yaml dans /config/
nano /config/secrets.yaml
```

#### 3.2 Contenu du fichier secrets.yaml
```yaml
# Identifiants BMW Connected Drive
bmw_username: "votre_email@example.com"
bmw_password: "votre_mot_de_passe_bmw"

# Configuration V2C Trydan
v2c_ip: "192.168.1.100"  # Adresse IP de votre borne V2C
v2c_username: "admin"     # Nom d'utilisateur V2C
v2c_password: "votre_mot_de_passe_v2c"

# Configuration des notifications
notification_recipients:
  - "votre_telephone_iphone"
```

### 4. Configuration de Home Assistant

#### 4.1 Ajout de la configuration
Ajoutez le contenu du fichier `configuration.yaml` à votre configuration Home Assistant :

```yaml
# Dans votre configuration.yaml principal
bmw_ix3_plugin:
  bmw_username: !secret bmw_username
  bmw_password: !secret bmw_password
  v2c_ip: !secret v2c_ip
  v2c_username: !secret v2c_username
  v2c_password: !secret v2c_password
```

#### 4.2 Ajout des automatisations
Copiez le contenu des fichiers `automations.yaml` et `advanced_automations.yaml` dans votre fichier `automations.yaml` ou créez des fichiers séparés.

### 5. Redémarrage et configuration

#### 5.1 Redémarrage de Home Assistant
```bash
# Redémarrer Home Assistant
ha core restart
```

#### 5.2 Ajout de l'intégration
1. Allez dans **Configuration** > **Appareils et services**
2. Cliquez sur **Ajouter une intégration**
3. Recherchez **BMW iX3 Plugin**
4. Suivez les instructions de configuration

### 6. Configuration des intégrations existantes

#### 6.1 BMW Connected Drive
1. Ajoutez l'intégration officielle BMW Connected Drive
2. Configurez avec vos identifiants BMW
3. Vérifiez que les entités sont créées

#### 6.2 V2C Trydan
1. Ajoutez l'intégration officielle V2C
2. Configurez avec l'adresse IP de votre borne
3. Vérifiez la connectivité

#### 6.3 Home Assistant Companion (iOS)
1. Installez l'application Home Assistant Companion sur votre iPhone
2. Configurez la connexion à votre instance Home Assistant
3. Activez les notifications push

### 7. Configuration du tableau de bord

#### 7.1 Import du tableau de bord
1. Allez dans **Configuration** > **Tableaux de bord**
2. Cliquez sur les trois points > **Importer un tableau de bord**
3. Copiez le contenu du fichier `dashboard.yaml`

#### 7.2 Personnalisation
- Ajustez les entités selon vos besoins
- Modifiez les couleurs et icônes
- Ajoutez ou supprimez des cartes selon vos préférences

### 8. Test et validation

#### 8.1 Vérification des entités
Vérifiez que toutes les entités sont créées :
- Capteurs BMW (batterie, charge, autonomie)
- Calculateurs de temps de charge
- Capteurs V2C
- Commutateurs de contrôle
- Entités numériques

#### 8.2 Test des fonctionnalités
1. **Calculs de temps** : Vérifiez que les temps de charge sont calculés correctement
2. **Contrôle V2C** : Testez l'activation/désactivation de la charge
3. **Notifications** : Vérifiez que les notifications iOS fonctionnent
4. **Planification** : Testez la planification de charge

### 9. Optimisation et maintenance

#### 9.1 Surveillance des logs
```bash
# Surveiller les logs du plugin
tail -f /config/home-assistant.log | grep bmw_ix3
```

#### 9.2 Mise à jour du plugin
```bash
# Mettre à jour le plugin
cd /config/custom_components/bmw_ix3_plugin
git pull origin main
ha core restart
```

#### 9.3 Sauvegarde de la configuration
```bash
# Créer une sauvegarde
ha backups new --name "BMW_iX3_Plugin_Backup"
```

## Dépannage

### Problèmes courants

#### 1. Plugin non reconnu
- Vérifiez la structure des fichiers
- Redémarrez Home Assistant
- Vérifiez les logs pour les erreurs

#### 2. Erreurs de connexion BMW
- Vérifiez vos identifiants BMW Connected Drive
- Testez la connexion sur l'application BMW
- Vérifiez que votre compte a accès à l'API

#### 3. Problèmes V2C
- Vérifiez l'adresse IP de la borne
- Testez la connectivité réseau
- Vérifiez les identifiants V2C

#### 4. Notifications iOS non reçues
- Vérifiez la configuration de l'application Companion
- Activez les notifications dans les paramètres iOS
- Testez les notifications depuis Home Assistant

### Support

Pour obtenir de l'aide :
1. Consultez les logs Home Assistant
2. Vérifiez la documentation des intégrations officielles
3. Consultez les forums Home Assistant
4. Ouvrez une issue sur le repository du plugin

## Sécurité

### Bonnes pratiques
- Utilisez des mots de passe forts
- Ne partagez jamais vos identifiants
- Mettez à jour régulièrement le plugin
- Surveillez les logs pour les activités suspectes

### Sauvegarde
- Sauvegardez régulièrement votre configuration
- Gardez une copie de vos paramètres personnalisés
- Documentez vos modifications

