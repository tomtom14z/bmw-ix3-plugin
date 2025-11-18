# 🧠 Système d'Apprentissage des Courbes de Recharge

## 📋 Vue d'ensemble

Le plugin BMW iX3 intègre maintenant un **système d'apprentissage automatique** qui apprend des vraies données de recharge de votre véhicule pour améliorer la précision des prédictions de temps de charge.

## 🎯 Fonctionnement

### 1. Enregistrement Automatique

Pendant chaque session de recharge, le plugin enregistre automatiquement :
- **SOC actuel** (State of Charge)
- **Temps restant** (depuis BMW CarData)
- **Puissance de charge** (kW)
- **SOC cible** (80%, 100%, etc.)
- **Timestamp** de chaque point de données

### 2. Catégorisation par Type de Chargeur

Les données sont organisées par catégorie de chargeur :
- **7kW** : Chargeurs domestiques (5-9 kW)
- **11kW** : Chargeurs triphasés (9-15 kW)
- **22kW** : Chargeurs publics (15-30 kW)
- **50kW** : Charge rapide (30-70 kW)
- **150kW** : Charge ultra-rapide (70-200 kW)

### 3. Construction des Courbes d'Apprentissage

Pour chaque combinaison (type de chargeur + SOC cible), le système :
- Enregistre plusieurs sessions de recharge
- Construit des courbes SOC → Temps restant
- Utilise la moyenne pondérée des sessions précédentes

### 4. Prédiction Intelligente

Lors du calcul d'un temps de charge :
1. **Priorité 1** : Utilise les données d'apprentissage si disponibles
2. **Priorité 2** : Utilise le calcul théorique si pas assez de données

## 📊 Stockage des Données

Les données sont stockées dans :
```
/config/bmw_ix3_learning/charge_history_{entry_id}.json
```

Chaque fichier contient :
- Les sessions de recharge par catégorie
- Les points de données (SOC, temps restant, puissance)
- Les statistiques (durée réelle, SOC gagné, etc.)

## 🔄 Amélioration Progressive

Le système s'améliore avec le temps :
- **Après 2 sessions** : Commence à utiliser les données apprises
- **Après 10 sessions** : Prédictions très précises
- **Après 50 sessions** : Les anciennes sessions sont automatiquement supprimées (garder les 50 plus récentes)

## 📈 Utilisation

### Vérifier les Statistiques d'Apprentissage

Les logs Home Assistant affichent :
- `"Nouvelle session d'apprentissage: ..."` : Début d'une session
- `"Session finalisée: ..."` : Fin d'une session avec statistiques
- `"Utilisation des données d'apprentissage: X min"` : Utilisation des données apprises
- `"Utilisation du calcul théorique: X min"` : Utilisation du calcul théorique

### Données Requises

Pour que l'apprentissage fonctionne, le plugin doit détecter :
- ✅ `State of Charge (Last Known)` : SOC actuel
- ✅ `Charging Time Remaining` : Temps restant (depuis BMW CarData)
- ✅ `Predicted Charge Speed` : Puissance de charge
- ✅ `Target State of Charge` : SOC cible (optionnel, 100% par défaut)

## 🎓 Exemple d'Apprentissage

### Session 1 (Première charge)
- SOC: 20% → 80%
- Puissance: 11 kW
- Temps réel: 4h 30min
- **Résultat** : Données enregistrées, calcul théorique utilisé

### Session 2 (Deuxième charge)
- SOC: 30% → 80%
- Puissance: 11 kW
- Temps réel: 3h 45min
- **Résultat** : Données enregistrées, **début d'utilisation des données apprises**

### Session 10 (Charge habituelle)
- SOC: 25% → 80%
- Puissance: 11 kW
- **Résultat** : **Prédiction précise basée sur les 9 sessions précédentes**

## 🔧 Dépannage

### Le système n'apprend pas

1. **Vérifier les logs** : Cherchez "Nouvelle session d'apprentissage"
2. **Vérifier les entités** : Assurez-vous que BMW CarData expose bien :
   - `charging_time_remaining`
   - `target_state_of_charge`
3. **Vérifier le fichier** : Le fichier JSON devrait être créé dans `/config/bmw_ix3_learning/`

### Les prédictions ne sont pas précises

1. **Attendre plus de sessions** : Le système a besoin d'au moins 2 sessions
2. **Vérifier la cohérence** : Les sessions doivent être avec le même type de chargeur
3. **Vérifier les données** : Les temps restants de BMW CarData doivent être fiables

## 📝 Notes Techniques

- Les données sont sauvegardées toutes les 10 minutes ou lors d'un changement significatif de SOC
- Les sessions sont finalisées automatiquement quand la charge s'arrête
- Le système utilise une moyenne pondérée par distance pour les prédictions
- Les anciennes sessions (plus de 50) sont automatiquement supprimées

## 🚀 Avantages

✅ **Précision améliorée** : Les prédictions s'améliorent avec le temps  
✅ **Adaptation personnalisée** : Apprend de VOS habitudes de recharge  
✅ **Courbe réelle** : Prend en compte la vraie courbe de charge BMW iX3  
✅ **Automatique** : Aucune configuration nécessaire  
✅ **Robuste** : Fallback sur calcul théorique si pas de données

