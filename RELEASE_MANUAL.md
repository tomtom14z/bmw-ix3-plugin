# 📦 Guide de Publication Manuelle des Releases

## 🚀 Processus de Release

### 1. Préparer la Release

```bash
# 1. Mettre à jour la version dans manifest.json
# 2. Mettre à jour le CHANGELOG.md
# 3. Commiter les changements
git add .
git commit -m "Version X.Y.Z - Description des changements"
git push origin main

# 4. Créer le tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

### 2. Créer la Release sur GitHub

1. **Allez sur GitHub** : https://github.com/tomtom14z/bmw-ix3-plugin/releases/new

2. **Remplissez le formulaire** :
   - **Tag** : Sélectionnez `vX.Y.Z` dans le menu déroulant (ou créez-le si nécessaire)
   - **Titre** : `Release vX.Y.Z`
   - **Description** : Copiez-collez le contenu du CHANGELOG pour cette version

3. **Exemple de description** :
   ```markdown
   ## Version X.Y.Z
   
   ### Corrections
   - Description de la correction 1
   - Description de la correction 2
   
   ### Améliorations
   - Description de l'amélioration 1
   
   Consultez le [CHANGELOG.md](https://github.com/tomtom14z/bmw-ix3-plugin/blob/main/CHANGELOG.md) pour plus de détails.
   ```

4. **Cliquez sur "Publish release"**

### 3. Vérification HACS

Après la publication de la release :

1. Dans Home Assistant, allez dans **HACS** → **Intégrations**
2. Cliquez sur les **3 points** (⋮) → **Mettre à jour les informations**
3. Recherchez "BMW iX3 Plugin"
4. La nouvelle version devrait apparaître avec un bouton **"Mettre à jour"**

## 📋 Checklist de Release

- [ ] Version mise à jour dans `manifest.json`
- [ ] CHANGELOG.md mis à jour avec la nouvelle version
- [ ] Code testé et fonctionnel
- [ ] Commit créé et poussé sur GitHub
- [ ] Tag créé et poussé sur GitHub
- [ ] Release créée manuellement sur GitHub
- [ ] Vérification que HACS détecte la nouvelle version

## 🔗 Liens Utiles

- **Repository** : https://github.com/tomtom14z/bmw-ix3-plugin
- **Releases** : https://github.com/tomtom14z/bmw-ix3-plugin/releases
- **Nouvelle Release** : https://github.com/tomtom14z/bmw-ix3-plugin/releases/new

