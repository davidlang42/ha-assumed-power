"""Sensor platform for Assumed Power and Energy."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.components.integration.sensor import IntegrationSensor
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the assumed power and energy sensors from a config entry."""
    power_sensor = AssumedPowerSensor(entry)
    
    energy_sensor = IntegrationSensor(
        integration_method="trapezoidal",
        name=f"{entry.data.get('name', 'Assumed Power')} Energy",
        unique_id=f"{entry.entry_id}_energy",
        source_entity=f"sensor.{entry.entry_id}_power",
        unit_prefix="k",
        unit_time="h",
        round_digits=3,
    )
    
    async_add_entities([power_sensor, energy_sensor])

class AssumedPowerSensor(SensorEntity):
    """Representation of an Assumed Power Sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_name = f"{entry.data.get('name', 'Assumed Power')} Power"
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._update_config()
        entry.async_on_unload(entry.add_update_listener(self._async_update_listener))

    @callback
    def _update_config(self) -> None:
        """Fetch latest configuration or options."""
        data = self._entry.options if self._entry.options else self._entry.data
        self._state_entities = data.get("state_entities") or self._entry.data.get("state_entities") or []
        self._available_entities = data.get("on_if_available_entities") or self._entry.data.get("on_if_available_entities") or []
        self._always_on_count = int(data.get("always_on_count") or 0)
        self._power_when_on = float(data.get("power_when_on", 10.0))
        self._power_when_off = float(data.get("power_when_off") or 0.0)

    async def _async_update_listener(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Handle options update."""
        self._update_config()
        self.async_write_ha_state()

    @property
    def native_value(self):
        """Return the calculated power state based on active/inactive states and power levels."""
        total_power = 0.0

        # Evaluate state entities (on vs off)
        for entity_id in self._state_entities:
            state_obj = self.hass.states.get(entity_id)
            if state_obj and state_obj.state == "on":
                total_power += self._power_when_on
            else:
                total_power += self._power_when_off

        # Evaluate availability entities (available vs unavailable/unknown)
        for entity_id in self._available_entities:
            state_obj = self.hass.states.get(entity_id)
            if state_obj and state_obj.state not in ("unavailable", "unknown"):
                total_power += self._power_when_on
            else:
                total_power += self._power_when_off

        # Add always-on devices using the 'power when on' wattage
        total_power += self._always_on_count * self._power_when_on

        return round(total_power, 3)

    @property
    def extra_state_attributes(self):
        """Return device state attributes for reference."""
        return {
            "state_entities": self._state_entities,
            "on_if_available_entities": self._available_entities,
            "always_on_count": self._always_on_count,
            "power_when_on": self._power_when_on,
            "power_when_off": self._power_when_off,
        }