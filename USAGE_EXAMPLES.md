# Exemples d'utilisation - Plugin BMW iX3

## 🚀 Scénarios d'utilisation courants

### 1. Charge quotidienne optimisée

**Objectif** : Charger la voiture pour le travail du lendemain (8h00) à 80%

**Configuration** :
```yaml
# Dans votre tableau de bord
number.bmw_ix3_target_soc: 80
input_datetime.bmw_ix3_departure_time: "08:00:00"
switch.bmw_ix3_auto_stop_80_percent: "on"
```

**Résultat** :
- Le système calcule automatiquement l'heure de début de charge
- La charge démarre pendant les heures creuses (22h00-6h00)
- Arrêt automatique à 80% pour protéger la batterie
- Notification sur iPhone quand la charge est terminée

### 2. Charge complète pour un long trajet

**Objectif** : Charger à 100% pour un voyage de 300km

**Configuration** :
```yaml
number.bmw_ix3_target_soc: 100
input_datetime.bmw_ix3_departure_time: "06:00:00"
switch.bmw_ix3_auto_stop_80_percent: "off"
```

**Résultat** :
- Charge complète programmée
- Démarrage automatique pendant la nuit
- Widget iOS affiche le progrès en temps réel
- Notification à 100% avec rappel de déconnexion

### 3. Charge rapide pendant la journée

**Objectif** : Recharger rapidement pendant une pause déjeuner

**Configuration** :
```yaml
# Utilisation des contrôles rapides
switch.v2c_charging: "on"
number.bmw_ix3_target_soc: 85
```

**Résultat** :
- Démarrage immédiat de la charge
- Widget iOS mis à jour toutes les minutes
- Arrêt automatique à 85%
- Notification de fin de charge

## 📱 Utilisation du widget iOS

### Affichage en temps réel

Le widget affiche en permanence :
- **Pourcentage de batterie** : 65%
- **État de charge** : 🔌 Charge en cours
- **Puissance** : 7.4 kW
- **Heure 80%** : 14:30
- **Heure 100%** : 16:45

### Actions rapides depuis le widget

1. **Démarrer la charge** : Tap sur le bouton de démarrage
2. **Arrêter la charge** : Tap sur le bouton d'arrêt
3. **Actualiser** : Pull-to-refresh
4. **Voir détails** : Ouverture de l'app Home Assistant

### Notifications intelligentes

- **Début de charge** : "🚗 Charge démarrée - 65% → 80% prévu à 14:30"
- **À 80%** : "🔋 Charge à 80% atteinte - Protection batterie activée"
- **Fin de charge** : "✅ Charge terminée - N'oubliez pas de déconnecter"
- **Erreur** : "⚠️ Problème de charge détecté - Vérifiez la connexion"

## 🔧 Configuration avancée

### Optimisation tarifaire

```yaml
# Dans automations.yaml
- id: bmw_ix3_off_peak_optimization
  alias: "BMW iX3 - Optimisation heures creuses"
  trigger:
    - platform: time
      at: "22:00:00"  # Début des heures creuses
  condition:
    - condition: template
      value_template: "{{ states('input_boolean.bmw_ix3_charging_scheduled') == 'on' }}"
  action:
    - service: switch.turn_on
      entity_id: switch.v2c_charging
```

### Protection batterie personnalisée

```yaml
# Arrêt à 90% au lieu de 80%
number.bmw_ix3_target_soc: 90
switch.bmw_ix3_auto_stop_80_percent: "off"

# Automatisation personnalisée
- id: bmw_ix3_custom_stop_90
  alias: "BMW iX3 - Arrêt à 90%"
  trigger:
    - platform: numeric_state
      entity_id: sensor.bmw_ix3_battery_level
      above: 89.5
  action:
    - service: switch.turn_off
      entity_id: switch.v2c_charging
```

### Intégration avec la météo

```yaml
# Ajustement automatique selon la température
- id: bmw_ix3_weather_adjustment
  alias: "BMW iX3 - Ajustement météo"
  trigger:
    - platform: state
      entity_id: weather.home
  action:
    - service: python_script.bmw_ix3_weather_charge_adjustment
      data:
        temperature: "{{ state_attr('weather.home', 'temperature') }}"
        condition: "{{ states('weather.home') }}"
```

## 📊 Surveillance et statistiques

### Tableau de bord personnalisé

Le tableau de bord affiche :
- **Gauges** : Niveau de batterie et autonomie
- **Calculs de temps** : Pour toutes les puissances
- **Contrôles** : Commutateurs V2C et arrêt auto
- **Planification** : Interface de programmation
- **Actions rapides** : Boutons de contrôle

### Statistiques quotidiennes

```yaml
# Rapport automatique quotidien
- id: bmw_ix3_daily_report
  alias: "BMW iX3 - Rapport quotidien"
  trigger:
    - platform: time
      at: "23:59:00"
  action:
    - service: python_script.bmw_ix3_daily_statistics
      data:
        date: "{{ now().strftime('%Y-%m-%d') }}"
```

**Exemple de rapport** :
```
📊 RAPPORT QUOTIDIEN BMW iX3 - 2024-01-15

🔋 ÉNERGIE CHARGÉE
• Total: 45.2 kWh
• Sessions: 2
• Temps total: 6.1 heures

⚡ PERFORMANCE
• Puissance moyenne: 7.4 kW
• Efficacité: Bon

💰 ÉCONOMIES
• Coût estimé: 6.78 €
• CO2 économisé: 18.1 kg

📈 RECOMMANDATIONS
• Excellente utilisation de votre véhicule électrique!
```

## 🛠️ Dépannage et maintenance

### Vérification des entités

```yaml
# Script de vérification
script:
  bmw_ix3_check_entities:
    alias: "BMW iX3 - Vérification entités"
    sequence:
      - service: system_log.write
        data:
          message: "Batterie: {{ states('sensor.bmw_ix3_battery_level') }}%"
      - service: system_log.write
        data:
          message: "Charge: {{ states('sensor.bmw_ix3_charging_status') }}"
      - service: system_log.write
        data:
          message: "V2C: {{ states('sensor.v2c_status') }}"
```

### Sauvegarde des paramètres

```yaml
# Sauvegarde automatique
- id: bmw_ix3_auto_backup
  alias: "BMW iX3 - Sauvegarde auto"
  trigger:
    - platform: state
      entity_id: number.bmw_ix3_target_soc
    - platform: state
      entity_id: input_datetime.bmw_ix3_departure_time
  action:
    - service: python_script.bmw_ix3_backup_user_settings
      data:
        target_soc: "{{ states('number.bmw_ix3_target_soc') | float }}"
        departure_time: "{{ states('input_datetime.bmw_ix3_departure_time') }}"
        auto_stop_enabled: "{{ states('switch.bmw_ix3_auto_stop_80_percent') == 'on' }}"
```

### Mise à jour du plugin

```bash
# Mise à jour via SSH
cd /config/custom_components/bmw_ix3_plugin
git pull origin main
ha core restart
```

## 🎯 Conseils d'optimisation

### 1. Utilisez les heures creuses
- Programmez la charge entre 22h00 et 6h00
- Économisez jusqu'à 50% sur votre facture d'électricité

### 2. Protégez votre batterie
- Arrêtez à 80% pour les trajets quotidiens
- Chargez à 100% uniquement pour les longs trajets

### 3. Surveillez la température
- Évitez la charge par temps très froid (< -10°C)
- Réduisez la puissance par temps très chaud (> 35°C)

### 4. Optimisez la puissance
- Utilisez 7.4kW pour un bon compromis vitesse/efficacité
- 11kW pour les charges rapides
- 22kW uniquement si votre installation le permet

### 5. Planifiez vos trajets
- Définissez votre heure de départ
- Laissez le système calculer l'heure de début optimale
- Recevez des notifications de progression

## 📞 Support et aide

### Logs utiles
```bash
# Surveiller les logs du plugin
tail -f /config/home-assistant.log | grep bmw_ix3

# Logs des erreurs
grep "ERROR.*bmw_ix3" /config/home-assistant.log
```

### Entités importantes à surveiller
- `sensor.bmw_ix3_battery_level` : Niveau de batterie
- `sensor.bmw_ix3_charging_status` : État de charge
- `sensor.v2c_status` : État de la borne
- `switch.v2c_charging` : Contrôle de la charge

### Redémarrage en cas de problème
```bash
# Redémarrage du plugin
ha core restart

# Redémarrage complet
ha host reboot
```
