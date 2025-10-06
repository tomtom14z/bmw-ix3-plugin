# 🚀 Configuration GitHub et HACS - Plugin BMW iX3

## 📋 Informations du repository

### Nom du repository
```
bmw-ix3-plugin
```

### URL complète
```
https://github.com/tomtom14z/bmw-ix3-plugin
```

## 🔧 Étapes pour publier sur GitHub

### 1. Créer le repository sur GitHub

1. Allez sur [GitHub](https://github.com)
2. Cliquez sur "New repository"
3. **Nom du repository** : `bmw-ix3-plugin`
4. **Description** : `Plugin Home Assistant pour BMW iX3 électrique avec intégration V2C Trydan, calculs de temps de charge, widget iOS Live Activity et automatisations intelligentes`
5. **Visibilité** : Public
6. **Initialiser** : Ne pas cocher (nous avons déjà les fichiers)
7. Cliquez sur "Create repository"

### 2. Initialiser le repository local

```bash
# Naviguer vers le dossier du plugin
cd /Users/thomasvernouillet/bmw_ix3_plugin

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: BMW iX3 Plugin v1.0.0"

# Ajouter le remote
git remote add origin https://github.com/tomtom14z/bmw-ix3-plugin.git

# Pousser vers GitHub
git push -u origin main
```

### 3. Créer la première release

```bash
# Créer un tag pour la version 1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Pousser le tag
git push origin v1.0.0
```

## 📦 Configuration HACS

### 1. Fichier hacs.json
Le fichier `hacs.json` est déjà configuré avec :
- Nom du plugin
- Compatibilité Home Assistant 2023.1+
- Pays supportés
- Configuration pour HACS

### 2. Structure requise
✅ Tous les fichiers sont en place :
- `manifest.json` - Métadonnées du plugin
- `hacs.json` - Configuration HACS
- `README.md` - Documentation
- Structure de dossiers correcte

## 🔗 Liens de release pour HACS

### URL de base pour HACS
```
https://github.com/tomtom14z/bmw-ix3-plugin
```

### URL de release spécifique
```
https://github.com/tomtom14z/bmw-ix3-plugin/releases/latest
```

### URL pour installation directe via HACS
```
https://github.com/tomtom14z/bmw-ix3-plugin
```

## 📱 Installation via HACS

### 1. Ajouter le repository dans HACS

1. Ouvrez Home Assistant
2. Allez dans **HACS** > **Intégrations**
3. Cliquez sur les trois points (⋮) > **Repositories personnalisés**
4. Ajoutez l'URL : `https://github.com/tomtom14z/bmw-ix3-plugin`
5. Sélectionnez **Integration** comme catégorie
6. Cliquez sur **Ajouter**

### 2. Installer le plugin

1. Recherchez "BMW iX3 Plugin" dans HACS
2. Cliquez sur **Télécharger**
3. Redémarrez Home Assistant
4. Allez dans **Configuration** > **Appareils et services**
5. Cliquez sur **Ajouter une intégration**
6. Recherchez "BMW iX3 Plugin"

## 🔄 Mise à jour automatique

### 1. Workflow GitHub Actions
Le fichier `.github/workflows/release.yml` est configuré pour :
- Créer automatiquement une release lors du push d'un tag
- Générer les assets de release
- Notifier HACS des nouvelles versions

### 2. Processus de mise à jour

```bash
# 1. Modifier le numéro de version dans manifest.json
# 2. Commiter les changements
git add .
git commit -m "Update to version 1.0.1"

# 3. Créer un nouveau tag
git tag -a v1.0.1 -m "Release version 1.0.1"

# 4. Pousser les changements et le tag
git push origin main
git push origin v1.0.1
```

### 3. HACS détectera automatiquement la nouvelle version

## 📋 Checklist de publication

### ✅ Avant la publication
- [x] Fichier `manifest.json` configuré
- [x] Fichier `hacs.json` créé
- [x] Documentation complète
- [x] Licence MIT ajoutée
- [x] `.gitignore` configuré
- [x] Workflow GitHub Actions configuré

### ✅ Après la publication
- [ ] Repository créé sur GitHub
- [ ] Code poussé vers GitHub
- [ ] Première release créée (v1.0.0)
- [ ] Repository ajouté dans HACS
- [ ] Test d'installation via HACS

## 🎯 Commandes finales

### Initialisation complète
```bash
cd /Users/thomasvernouillet/bmw_ix3_plugin
git init
git add .
git commit -m "Initial commit: BMW iX3 Plugin v1.0.0"
git remote add origin https://github.com/tomtom14z/bmw-ix3-plugin.git
git push -u origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Pour les futures mises à jour
```bash
# Modifier le code
git add .
git commit -m "Update: description des changements"
git push origin main

# Créer une nouvelle release
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

## 🌟 Résultat final

Une fois publié, votre plugin sera disponible :
- **Sur GitHub** : https://github.com/tomtom14z/bmw-ix3-plugin
- **Dans HACS** : Recherche "BMW iX3 Plugin"
- **Installation** : Un clic dans HACS
- **Mises à jour** : Automatiques via HACS

**🎉 Votre plugin BMW iX3 sera accessible à toute la communauté Home Assistant !**
