# 🎨 Guide des Cartes Visuelles BMW iX3

Ce guide vous explique comment installer et utiliser les 3 cartes visuelles animées pour votre BMW iX3.

---

## 📋 Prérequis

### Composants HACS requis

Installez ces composants via **HACS > Frontend** :

1. **card-mod** - Pour les animations CSS personnalisées (obligatoire)
2. **mushroom** - Cartes modernes et barres de progression (recommandé)
3. **button-card** - Pour la carte premium avec image dynamique (optionnel)
4. **mini-graph-card** - Pour les graphiques historiques (optionnel)

**💡 Note** : Mushroom remplace bar-card et offre des composants plus stables et modernes.

### Installation via HACS

1. Allez dans **HACS** > **Frontend**
2. Cliquez sur **Explore & Download Repositories**
3. Recherchez et installez chaque composant listé ci-dessus
4. Redémarrez Home Assistant

---

## 🖼️ Préparation des Images

Pour que les cartes animées changent d'image selon l'état, créez le dossier `/config/www/` et ajoutez ces images :

### Images requises

- `bmw_ix3.png` - Image par défaut de votre BMW iX3
- `bmw_ix3_charging.png` - Image avec effet de charge (optionnel)
- `bmw_ix3_full.png` - Image batterie pleine (optionnel)
- `bmw_ix3_medium.png` - Image batterie moyenne (optionnel)
- `bmw_ix3_low.png` - Image batterie faible (optionnel)

**💡 Astuce** : Si vous n'avez qu'une seule image, utilisez le même fichier pour toutes. L'animation sera gérée par les effets CSS.

### Comment ajouter les images

1. Connectez-vous à Home Assistant
2. Allez dans **File Editor** (ajoutez-le via Modules complémentaires si absent)
3. Créez le dossier `www` dans `/config/` si inexistant
4. Uploadez vos images BMW iX3 dans `/config/www/`
5. Les images seront accessibles via `/local/nom_image.png`

---

## 🎴 Carte 1 : Mushroom Optimisée (Recommandée)

### Description
Carte moderne avec tous les avantages de Mushroom : chips interactifs, barres de progression, animations fluides. **C'est la carte recommandée !**

### Installation

1. Copiez le contenu de `bmw_ix3_mushroom_card.yaml`
2. Allez dans votre **Dashboard**
3. Mode édition > **Ajouter une carte** > **Manuel**
4. Collez le code YAML
5. Sauvegardez

### Fonctionnalités

- ✅ En-tête animé avec statut en temps réel
- ✅ Chips interactifs avec informations principales
- ✅ Barre de progression batterie moderne
- ✅ Contrôles avec feedback visuel
- ✅ Tableau détaillé des temps de charge
- ✅ Effets de transparence et flou

### Personnalisation

Modifiez les positions des éléments en changeant les valeurs `top`, `left`, `bottom`, `right` :

```yaml
style:
  top: 10%      # Distance du haut (0% = haut, 100% = bas)
  left: 10%     # Distance de gauche (0% = gauche, 100% = droite)
```

---

## 📱 Carte 2 : Mushroom Compacte (Mobile)

### Description
Carte ultra-compacte optimisée pour mobile. Parfait pour un aperçu rapide sur smartphone.

### Installation

1. Copiez le contenu de `bmw_ix3_mushroom_compact.yaml`
2. Allez dans votre **Dashboard**
3. Mode édition > **Ajouter une carte** > **Manuel**
4. Collez le code YAML
5. Sauvegardez

### Fonctionnalités

- ✅ Carte unique compacte
- ✅ Informations essentielles en un coup d'œil
- ✅ Animation de pulsation en charge
- ✅ Optimisée pour mobile
- ✅ Tap pour plus d'informations

---

## 📊 Carte 3 : Mushroom avec Graphique

### Description
Version complète avec graphique historique. Idéale pour analyser l'évolution de la batterie.

### Installation

1. Copiez le contenu de `bmw_ix3_mushroom_with_graph.yaml`
2. Allez dans votre **Dashboard**
3. Mode édition > **Ajouter une carte** > **Manuel**
4. Collez le code YAML
5. Sauvegardez

### Fonctionnalités

- ✅ En-tête compact avec statut
- ✅ Chips interactifs
- ✅ Barre de progression batterie
- ✅ Graphique historique 24h (nécessite mini-graph-card)
- ✅ Contrôles rapides

---

## 🌟 Carte 4 : Premium Card (Carte Ultra-Moderne)

### Description
Carte premium avec image dynamique qui change selon l'état de charge. Effets de lumière et animations avancées.

### Installation

1. **Requis** : `custom:button-card` doit être installé
2. Copiez le contenu de `bmw_ix3_premium_card.yaml`
3. Allez dans votre **Dashboard**
4. Mode édition > **Ajouter une carte** > **Manuel**
5. Collez le code YAML
6. Sauvegardez

### Effets Spéciaux

#### Changement d'image automatique

- **En charge** → `bmw_ix3_charging.png` avec effet de pulsation verte
- **Batterie ≥ 80%** → `bmw_ix3_full.png` avec fond vert
- **Batterie 50-79%** → `bmw_ix3_medium.png` avec fond orange
- **Batterie < 50%** → `bmw_ix3_low.png` avec fond rouge

#### Animations

- **En charge** : Effet de pulsation lumineuse verte
- **Batterie faible** : Fond rouge pour alerter
- **Barre de progression** : Animation fluide du niveau de batterie

---

## 🎯 Recommandations d'Usage

### Pour commencer (Recommandé)
1. **Installez** : `card-mod` + `mushroom`
2. **Utilisez** : `bmw_ix3_mushroom_card.yaml` (carte complète)
3. **Alternative mobile** : `bmw_ix3_mushroom_compact.yaml`

### Pour les utilisateurs avancés
1. **Ajoutez** : `mini-graph-card` pour les graphiques
2. **Utilisez** : `bmw_ix3_mushroom_with_graph.yaml`
3. **Optionnel** : `button-card` pour la carte premium

### Pour les utilisateurs minimalistes
1. **Installez** : `card-mod` uniquement
2. **Utilisez** : `bmw_ix3_simple_card.yaml` (composants de base)

---

## 🎨 Personnalisation Avancée

### Changer les Couleurs

Dans n'importe quelle carte, modifiez les couleurs en changeant les codes hexadécimaux :

```yaml
color: '#4CAF50'  # Vert
color: '#FFC107'  # Orange
color: '#FF5252'  # Rouge
color: '#2196F3'  # Bleu
```

### Changer les Animations

Modifiez la vitesse d'animation :

```yaml
animation: pulse 2s ease-in-out infinite;
#              ↑ Durée (2 secondes)
```

### Ajouter des Effets de Transparence

```yaml
background: rgba(255, 255, 255, 0.1)
#                               ↑ Transparence (0 = invisible, 1 = opaque)
backdrop-filter: blur(10px)  # Effet de flou
```

---

## 🔧 Dépannage

### Les images ne s'affichent pas

1. Vérifiez que les images sont dans `/config/www/`
2. Vérifiez les noms de fichiers (sensible à la casse)
3. Rechargez la page (Ctrl+F5)
4. Vérifiez les logs Home Assistant pour les erreurs

### Les animations ne fonctionnent pas

1. Vérifiez que **card-mod** est installé
2. Videz le cache du navigateur
3. Redémarrez Home Assistant

### Les cartes personnalisées ne se chargent pas

1. Vérifiez que tous les composants HACS sont installés
2. Allez dans **HACS** > **Frontend** et vérifiez les mises à jour
3. Redémarrez Home Assistant après chaque installation

### Les entités ne sont pas trouvées

1. Vérifiez que le plugin BMW iX3 est actif
2. Vérifiez que BMW CarData HA remonte bien les données
3. Allez dans **Outils pour développeurs** > **États** et vérifiez les noms d'entités
4. Adaptez les noms d'entités dans les cartes si nécessaire

---

## 💡 Conseils d'Utilisation

### Placement Recommandé

1. **Page d'accueil** : Carte Premium (vue d'ensemble rapide)
2. **Page Véhicule** : Dashboard Moderne (détails complets)
3. **Vue Mobile** : Picture Elements (compact et visuel)

### Combinaisons

Vous pouvez combiner plusieurs cartes dans une vue :

```yaml
type: vertical-stack
cards:
  - !include bmw_ix3_premium_card.yaml
  - !include bmw_ix3_dashboard_card.yaml
```

---

## 📱 Optimisation Mobile

Pour une meilleure expérience mobile, ajoutez à chaque carte :

```yaml
card_mod:
  style: |
    ha-card {
      margin: 5px;
    }
    @media (max-width: 768px) {
      ha-card {
        font-size: 14px;
      }
    }
```

---

## 🎯 Exemples de Configurations Complètes

### Configuration Simple (1 carte)

Utilisez la **Carte Premium** pour une vue rapide et moderne.

### Configuration Complète (Multi-onglets)

Créez plusieurs vues :

- **Vue 1 - Aperçu** : Carte Premium
- **Vue 2 - Détails** : Dashboard Moderne
- **Vue 3 - Historique** : Mini-graph-card étendu

---

## 🚀 Aller Plus Loin

### Ajouter des Notifications

Combinez avec des automatisations pour envoyer des notifications avec capture d'écran de la carte.

### Intégration Widget iOS

Les données sont automatiquement disponibles pour le widget iOS Live Activity.

### Partage sur Apple Watch

Créez des complications Apple Watch avec les données principales.

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs Home Assistant
2. Consultez la documentation des composants HACS
3. Ouvrez une issue sur GitHub avec une capture d'écran

---

**Bon usage de vos cartes BMW iX3 ! 🚗⚡**

