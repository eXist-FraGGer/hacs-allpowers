# Allpowers BLE Battery – Home Assistant Integration

Control and monitor **Allpowers portable power stations** over Bluetooth directly from Home Assistant.

This integration exposes power outputs, frequencies, work/eco modes, runtime data, and more — without using cloud services.

---

## ✨ Features

### Sensors
- Battery percentage
- Input power (W)
- Output power (W)
- Estimated remaining runtime

### Switches
- AC output
- DC output
- Light / torch
- Eco mode

### Select Controls
- AC frequency (50 Hz / 60 Hz)
- Work mode (Mute / Standard / Fast)
- Eco shutdown times (1 h / 2 h / 4 h / 6 h)

---

## ⚠ Important Notice

This integration **cannot detect** whether your specific Allpowers model supports every setting or feature.

If your device **does not have a feature physically** or **the mobile app does not show it**, Home Assistant will still create the entity.

👉 **Recommendation:** Disable unsupported entities in Home Assistant to avoid confusion:

**Settings → Devices & Services → Allpowers BLE Battery → Entities → Disable unsupported items.**

---

## 📦 Installation

### Option 1 — Via HACS (Recommended)
1. Open **HACS → Integrations**
2. Click **⋯ → Custom repositories**
3. Add this repository as type **Integration**
4. Search for **Allpowers BLE Battery** and install
5. Restart Home Assistant

### Option 2 — Manual
1. Download this repository
2. Copy the folder to:

```
config/custom_components/allpowers_ble
```

3. Restart Home Assistant

---

## 🔧 Configuration

1. Open **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Allpowers BLE Battery**
4. Choose your power station from the BLE devices list

The integration will automatically create all sensors, switches, and selects.

---

## 📝 Tips

- Close the official Allpowers mobile app — it may keep a BLE connection open and block Home Assistant.
- For the best connection stability, use a USB Bluetooth dongle on a short extension cable.
- State changes always follow what the power station reports via BLE; if a write fails, the UI will revert to the actual device state.

---

## 💬 Support & Contributions

Pull requests are welcome!
