from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AllpowersBLE, AllpowersBLECoordinator
from .const import DOMAIN
from .models import AllpowersBLEData

FREQUENCY_SELECT_DESCRIPTION = SelectEntityDescription(
    key="frequency",
    name="AC Frequency",
    has_entity_name=True,
)

WORK_MODE_SELECT_DESCRIPTION = SelectEntityDescription(
    key="work_mode",
    name="Work Mode",
    has_entity_name=True,
)

ECO_TIMER_SELECT_DESCRIPTION = SelectEntityDescription(
    key="eco_timer",
    name="Eco Mode Timer",
    has_entity_name=True,
)

SELECT_DESCRIPTIONS = [
    FREQUENCY_SELECT_DESCRIPTION,
    WORK_MODE_SELECT_DESCRIPTION,
    ECO_TIMER_SELECT_DESCRIPTION,
]

FREQUENCY_OPTIONS = ["50 Hz", "60 Hz"]
WORK_MODE_OPTIONS = ["Mute Mode", "Standard Mode", "Fast Mode"]
ECO_TIMER_OPTIONS = ["1 h", "2 h", "4 h", "6 h"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform for Allpowers BLE."""
    data: AllpowersBLEData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AllpowersBLESelect(
            data.coordinator,
            data.device,
            entry.title,
            description,
        )
        for description in SELECT_DESCRIPTIONS
    )


class AllpowersBLESelect(CoordinatorEntity[AllpowersBLECoordinator], SelectEntity):
    """Select entity for Allpowers BLE."""

    def __init__(
        self,
        coordinator: AllpowersBLECoordinator,
        device: AllpowersBLE,
        name: str,
        description: SelectEntityDescription,
    ) -> None:
        """Initialize select."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._key = description.key
        self.entity_description = description
        self._attr_unique_id = f"{device.address}_{self._key}"
        self._attr_device_info = DeviceInfo(
            name=name,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
        )
        if self._key == "frequency":
            self._attr_options = FREQUENCY_OPTIONS
        elif self._key == "work_mode":
            self._attr_options = WORK_MODE_OPTIONS
        elif self._key == "eco_timer":
            self._attr_options = ECO_TIMER_OPTIONS
        else:
            self._attr_options = []

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Entity availability."""
        return True

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self._key == "frequency":
            return "60 Hz" if self._device.frequency_hz == 60 else "50 Hz"
        if self._key == "work_mode":
            return self._device.work_mode
        if self._key == "eco_timer":
            return f"{self._device.eco_shutdown_time} h"
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._key == "frequency":
            hz = 60 if option.startswith("60") else 50
            await self._device.set_frequency(hz)
        elif self._key == "work_mode":
            await self._device.set_work_mode(option)
        elif self._key == "eco_timer":
            hours = int(option.split()[0])
            await self._device.set_eco_shutdown_time(hours)
        self.async_write_ha_state()
