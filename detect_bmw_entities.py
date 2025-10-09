#!/usr/bin/env python3
"""
Script d'aide pour détecter les entités BMW CarData HA
Exécutez ce script dans le terminal Home Assistant pour voir vos entités BMW
"""

import sys
import json

# Ce script doit être exécuté dans Home Assistant
# Allez dans Outils pour développeurs > Modèle et collez ce code :

TEMPLATE = """
{%- set bmw_entities = states | selectattr('entity_id', 'match', '.*(bmw|ix3|cardata).*') | list -%}

## 🔍 Entités BMW Détectées ({{ bmw_entities | length }})

{% for entity in bmw_entities %}
### {{ entity.entity_id }}
- **État** : {{ entity.state }}
- **Attributs** : {{ entity.attributes | tojson }}
- **Nom amical** : {{ entity.name }}
---
{% endfor %}

## 📋 Résumé pour Configuration

Copiez ces noms d'entités dans votre configuration :

```yaml
# Entités détectées :
{% for entity in bmw_entities -%}
# - {{ entity.entity_id }} ({{ entity.name }})
{% endfor %}
```

## 🔧 Détection Automatique du Plugin

Le plugin BMW iX3 recherche automatiquement ces entités BMW CarData :
- **Batterie** : "State of Charge", "Battery Charge Level", "SOC"
- **État de charge** : "Charging Status", "HV Charging Status"
- **Puissance** : "Predicted charge speed", "Charging Power"
- **Autonomie** : "Forecast Electric Range", "Electric Range", "Range"

### Vos entités correspondantes :

{% set battery_entities = bmw_entities | selectattr('name', 'match', '.*(state of charge|battery charge level|soc).*') | list -%}
{% if battery_entities %}
**🔋 Batterie :**
{% for entity in battery_entities -%}
- {{ entity.entity_id }} = {{ entity.state }}
{% endfor %}
{% endif %}

{% set charging_entities = bmw_entities | selectattr('name', 'match', '.*(charging status|hv charging status).*') | list -%}
{% if charging_entities %}
**⚡ État de charge :**
{% for entity in charging_entities -%}
- {{ entity.entity_id }} = {{ entity.state }}
{% endfor %}
{% endif %}

{% set power_entities = bmw_entities | selectattr('name', 'match', '.*(predicted charge speed|charging power).*') | list -%}
{% if power_entities %}
**🔌 Puissance :**
{% for entity in power_entities -%}
- {{ entity.entity_id }} = {{ entity.state }}
{% endfor %}
{% endif %}

{% set range_entities = bmw_entities | selectattr('name', 'match', '.*(forecast electric range|electric range|range).*') | list -%}
{% if range_entities %}
**🛣️ Autonomie :**
{% for entity in range_entities -%}
- {{ entity.entity_id }} = {{ entity.state }}
{% endfor %}
{% endif %}
"""

print("=" * 80)
print("🔍 DÉTECTEUR D'ENTITÉS BMW CARDATA HA")
print("=" * 80)
print()
print("📝 Instructions :")
print()
print("1. Allez dans Home Assistant")
print("2. Outils pour développeurs > Modèle")
print("3. Copiez-collez le template ci-dessous")
print("4. Exécutez pour voir vos entités BMW")
print()
print("=" * 80)
print("TEMPLATE À COPIER :")
print("=" * 80)
print()
print(TEMPLATE)
print()
print("=" * 80)
print()
print("💡 Astuce : Les résultats vous montreront exactement quelles entités")
print("   BMW CarData HA a créées et comment le plugin les détectera.")
print()

