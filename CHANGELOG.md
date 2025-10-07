# Changelog - Plugin BMW iX3 pour Home Assistant

## [1.0.2] - 2025-10-06

### ✨ Nouvelles fonctionnalités
- **Synchronisation flexible avec BMW** : Le plugin récupère maintenant les vraies données de votre véhicule
- **Compatible avec BMW Connected Drive ET BMW CarData** : Détection automatique de l'intégration disponible
- Détection intelligente des entités BMW avec recherche étendue (battery, soc, state_of_charge, etc.)
- Logs informatifs affichant le pourcentage de batterie, l'état de charge et l'autonomie lors de chaque mise à jour

### 🔧 Améliorations
- Recherche flexible des entités BMW (compatible avec différents noms d'entités)
- Validation des valeurs pour éviter les erreurs (batterie entre 0-100%, autonomie positive, etc.)
- Meilleure gestion des erreurs lors de la récupération des données
- Logs de débogage détaillés montrant les entités détectées
- Avertissement si aucune entité BMW n'est trouvée

### 📝 Notes importantes
- Suite aux problèmes de l'API BMW Connected Drive, le plugin est compatible avec BMW CarData comme alternative
- Le plugin détecte automatiquement l'intégration disponible (Connected Drive ou CarData)

## [1.0.1] - 2025-10-06

### 🐛 Corrections de bugs
- **Correction critique** : Remplacement de `async_forward_entry_setup` par `async_forward_entry_setups` pour compatibilité avec Home Assistant 2023.1+
- Cette correction résout l'erreur `AttributeError: 'ConfigEntries' object has no attribute 'async_forward_entry_setup'` lors de l'installation
- **Configuration V2C facultative** : L'intégration de la borne V2C Trydan est maintenant optionnelle lors de la configuration initiale
- Les capteurs et switches V2C ne sont créés que si une borne est configurée
- Possibilité d'utiliser le plugin uniquement avec la BMW iX3 sans borne de charge

## [1.0.0] - 2024-01-06

### 🎉 Version initiale

#### Fonctionnalités principales
- **Intégration BMW iX3** : Récupération des données via BMW Connected Drive
- **Intégration V2C Trydan** : Contrôle complet de la borne de charge
- **Calculs de temps de charge** : Temps estimé pour 80% et 100% à différentes puissances
- **Widget iOS Live Activity** : Affichage en temps réel sur iPhone
- **Tableau de bord personnalisé** : Interface complète avec planification
- **Automatisations intelligentes** : Protection batterie et optimisation

#### Capteurs implémentés
- `sensor.bmw_ix3_battery_level` : Niveau de batterie (%)
- `sensor.bmw_ix3_charging_status` : État de charge
- `sensor.bmw_ix3_charging_power` : Puissance de charge (kW)
- `sensor.bmw_ix3_range_electric` : Autonomie électrique (km)
- `sensor.bmw_ix3_charge_time_80_3_7kw` : Temps charge 80% (3.7kW)
- `sensor.bmw_ix3_charge_time_100_3_7kw` : Temps charge 100% (3.7kW)
- `sensor.bmw_ix3_charge_time_80_7_4kw` : Temps charge 80% (7.4kW)
- `sensor.bmw_ix3_charge_time_100_7_4kw` : Temps charge 100% (7.4kW)
- `sensor.bmw_ix3_charge_time_80_11kw` : Temps charge 80% (11kW)
- `sensor.bmw_ix3_charge_time_100_11kw` : Temps charge 100% (11kW)
- `sensor.bmw_ix3_charge_time_80_22kw` : Temps charge 80% (22kW)
- `sensor.bmw_ix3_charge_time_100_22kw` : Temps charge 100% (22kW)
- `sensor.v2c_status` : État de la borne V2C
- `sensor.v2c_charging_power` : Puissance V2C (kW)
- `sensor.v2c_charging_current` : Courant V2C (A)

#### Commutateurs implémentés
- `switch.v2c_charging` : Contrôle de la charge V2C
- `switch.bmw_ix3_auto_stop_80_percent` : Arrêt automatique à 80%

#### Entités numériques implémentées
- `number.bmw_ix3_departure_time` : Heure de départ (h)
- `number.bmw_ix3_target_soc` : SOC cible (%)

#### Services personnalisés
- `bmw_ix3_plugin.send_charging_notification` : Envoi de notifications
- `bmw_ix3_plugin.update_ios_widget` : Mise à jour du widget iOS
- `bmw_ix3_plugin.schedule_charging` : Planification de charge

#### Automatisations
- **Arrêt automatique à 80%** : Protection de la batterie
- **Notifications de charge** : Début, 80%, 100%, arrêt
- **Mise à jour widget iOS** : Toutes les 5 minutes pendant la charge
- **Planification intelligente** : Calcul automatique de l'heure de début
- **Optimisation tarifaire** : Utilisation des heures creuses
- **Gestion des pannes** : Redémarrage automatique après coupure

#### Scripts Python
- `bmw_ix3_calculate_charging_schedule.py` : Calcul de planification
- `bmw_ix3_weather_charge_adjustment.py` : Ajustement météorologique
- `bmw_ix3_daily_statistics.py` : Statistiques quotidiennes
- `bmw_ix3_backup_user_settings.py` : Sauvegarde des paramètres

#### Configuration
- **Interface de configuration** : Configuration flow intégré
- **Gestion des secrets** : Stockage sécurisé des identifiants
- **Tableau de bord** : Interface utilisateur complète
- **Documentation** : Guide d'installation et exemples d'utilisation

### 🔧 Améliorations techniques
- **Gestion d'erreurs robuste** : Gestion des pannes de connexion
- **Mise à jour intelligente** : Intervalle adaptatif selon l'état
- **Logs détaillés** : Traçabilité complète des opérations
- **Validation des données** : Vérification des valeurs avant traitement

### 📱 Intégration iOS
- **Widget Live Activity** : Affichage en temps réel
- **Notifications push** : Alertes intelligentes
- **Actions rapides** : Contrôles depuis les notifications
- **Mise à jour automatique** : Synchronisation avec Home Assistant

### 🛡️ Sécurité et fiabilité
- **Protection batterie** : Arrêt automatique à 80%
- **Surveillance température** : Ajustement selon les conditions
- **Gestion des pannes** : Redémarrage automatique
- **Sauvegarde automatique** : Protection des paramètres

### 📊 Fonctionnalités avancées
- **Calculs précis** : Prise en compte de la courbe de charge
- **Optimisation tarifaire** : Utilisation des heures creuses
- **Statistiques** : Rapports quotidiens et économies
- **Planification** : Calcul automatique de l'horaire optimal

## 🔮 Roadmap future

### Version 1.1.0 (prévue)
- [ ] Intégration avec d'autres bornes de charge
- [ ] Support des tarifs dynamiques
- [ ] Intégration avec les panneaux solaires
- [ ] Prédiction de l'autonomie selon le trajet

### Version 1.2.0 (prévue)
- [ ] Interface web personnalisée
- [ ] Export des données vers Excel/CSV
- [ ] Intégration avec Google Calendar
- [ ] Support des véhicules BMW supplémentaires

### Version 2.0.0 (prévue)
- [ ] Intelligence artificielle pour l'optimisation
- [ ] Intégration avec les réseaux de charge publics
- [ ] Support multi-véhicules
- [ ] Interface mobile native

## 🐛 Corrections de bugs

### Version 1.0.0
- Correction de l'affichage des temps de charge
- Amélioration de la gestion des erreurs de connexion
- Correction des notifications iOS
- Amélioration de la stabilité du widget

## 📝 Notes de développement

### Architecture
- **Coordinateur centralisé** : Gestion des données BMW et V2C
- **Entités modulaires** : Capteurs, commutateurs et entités numériques
- **Services personnalisés** : Fonctionnalités avancées
- **Scripts Python** : Calculs complexes et automatisations

### Dépendances
- `aiohttp>=3.8.0` : Communication HTTP asynchrone
- `async_timeout>=4.0.0` : Gestion des timeouts
- Home Assistant 2023.1+ : Version minimale requise

### Compatibilité
- **BMW iX3** : Véhicule principal supporté
- **V2C Trydan** : Borne de charge supportée
- **iOS 14+** : Support des widgets Live Activity
- **Home Assistant** : Toutes les versions 2023.1+

## 🤝 Contribution

### Comment contribuer
1. Fork le repository
2. Créez une branche feature
3. Committez vos changements
4. Ouvrez une Pull Request

### Standards de code
- Respect des conventions Python
- Documentation des fonctions
- Tests unitaires pour les nouvelles fonctionnalités
- Logs détaillés pour le débogage

### Signaler un bug
1. Vérifiez les logs Home Assistant
2. Consultez la documentation
3. Ouvrez une issue avec les détails
4. Incluez les logs d'erreur

## 📄 Licence

Ce plugin est distribué sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- Équipe Home Assistant pour la plateforme
- Communauté BMW Connected Drive
- Développeurs V2C Trydan
- Testeurs bêta du plugin

