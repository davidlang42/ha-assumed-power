# Assumed Power Calculator for Home Assistant

A lightweight custom integration for Home Assistant that calculates total live power (Watts) and cumulative energy consumption (kWh) based on configurable per-entity **Power When On** and **Power When Off** wattages.

## Features
- **UI Configurable & Options Flow:** Easily add devices, configure multi-entity tracking, and update wattage parameters on the fly via **Settings > Devices & Services**.
- **Multi-Entity Tracking:** Supports selecting multiple state-based entities and multiple availability-based entities simultaneously.
- **On/Off Wattage Mapping:** Specify separate power consumption values for when an entity is active vs. when it is inactive or unavailable.
- **Always-On Count:** Add a fixed quantity of always-on devices calculated at the *Power When On* rate.
- **Automatic Energy Integration:** Instantly provisions both a Power sensor ($W$) and an Energy integration sensor ($kWh$) ready for the Home Assistant Energy Dashboard.