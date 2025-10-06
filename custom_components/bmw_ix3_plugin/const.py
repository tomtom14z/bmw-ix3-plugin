"""Constantes pour le plugin BMW iX3."""

DOMAIN = "bmw_ix3_plugin"

# Configuration
CONF_BMW_USERNAME = "bmw_username"
CONF_BMW_PASSWORD = "bmw_password"
CONF_V2C_IP = "v2c_ip"
CONF_V2C_USERNAME = "v2c_username"
CONF_V2C_PASSWORD = "v2c_password"

# Entités BMW
BMW_BATTERY_LEVEL = "battery_level"
BMW_CHARGING_STATUS = "charging_status"
BMW_CHARGING_POWER = "charging_power"
BMW_RANGE_ELECTRIC = "range_electric"
BMW_LAST_UPDATE = "last_update"

# Entités V2C
V2C_CHARGING_ENABLED = "charging_enabled"
V2C_CHARGING_POWER = "charging_power"
V2C_CHARGING_CURRENT = "charging_current"
V2C_STATUS = "status"

# Calculs de charge
CHARGE_TIME_80_3_7KW = "charge_time_80_3_7kw"
CHARGE_TIME_100_3_7KW = "charge_time_100_3_7kw"
CHARGE_TIME_80_7_4KW = "charge_time_80_7_4kw"
CHARGE_TIME_100_7_4KW = "charge_time_100_7_4kw"
CHARGE_TIME_80_11KW = "charge_time_80_11kw"
CHARGE_TIME_100_11KW = "charge_time_100_11kw"
CHARGE_TIME_80_22KW = "charge_time_80_22kw"
CHARGE_TIME_100_22KW = "charge_time_100_22kw"

# Planification
DEPARTURE_TIME = "departure_time"
TARGET_SOC = "target_soc"
OPTIMAL_START_TIME = "optimal_start_time"

# Capacité batterie BMW iX3 (kWh)
BATTERY_CAPACITY = 80.0

# Puissances de charge (kW)
POWER_3_7KW = 3.7
POWER_7_4KW = 7.4
POWER_11KW = 11.0
POWER_22KW = 22.0

# Efficacité de charge (facteur de perte)
CHARGE_EFFICIENCY = 0.9

# Courbe de charge (ralentissement après 80%)
FAST_CHARGE_THRESHOLD = 80.0
SLOW_CHARGE_FACTOR = 0.5  # Réduction de 50% après 80%

# Mise à jour des données
UPDATE_INTERVAL = 300  # 5 minutes
CHARGING_UPDATE_INTERVAL = 60  # 1 minute pendant la charge

# Notifications iOS
NOTIFICATION_CHARGING_START = "charging_start"
NOTIFICATION_CHARGING_80 = "charging_80_percent"
NOTIFICATION_CHARGING_100 = "charging_100_percent"
NOTIFICATION_CHARGING_STOP = "charging_stop"
