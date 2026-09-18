import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

class AssumedPowerConfigFlow(config_entries.ConfigFlow, domain="assumed_power"):
    """Handle a config flow for Assumed Power."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step via UI."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input.get("name", "Assumed Power"), data=user_input)

        schema = vol.Schema({
            vol.Required("name", default="Device Power"): str,
            vol.Optional("state_entities", default=[]): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
            vol.Optional("on_if_available_entities", default=[]): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
            vol.Optional("always_on_count", default=0): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=1000, step=1)),
            vol.Required("power_when_on", default=10.0): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=10000, step=0.1, unit_of_measurement="W")),
            vol.Optional("power_when_off", default=0.0): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=10000, step=0.1, unit_of_measurement="W")),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AssumedPowerOptionsFlowHandler(config_entry)

class AssumedPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow to edit values later from the UI."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options if self.config_entry.options else self.config_entry.data

        schema = vol.Schema({
            vol.Optional("state_entities", default=current.get("state_entities", [])): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
            vol.Optional("on_if_available_entities", default=current.get("on_if_available_entities", [])): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
            vol.Optional("always_on_count", default=current.get("always_on_count", 0)): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=1000, step=1)),
            vol.Required("power_when_on", default=current.get("power_when_on", 10.0)): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=10000, step=0.1, unit_of_measurement="W")),
            vol.Optional("power_when_off", default=current.get("power_when_off", 0.0)): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=10000, step=0.1, unit_of_measurement="W")),
        })

        return self.async_show_form(step_id="init", data_schema=schema)