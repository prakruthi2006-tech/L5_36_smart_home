"""Smart home device controller.

Adds devices to rooms, toggles them, sets thermostats within a safe range,
reports power use and saves the home state to a JSON file.
"""

import json
import os
import subprocess  # nosec B404

HUB_HOST = "127.0.0.1"  # bind to localhost only, not all interfaces
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
MIN_TEMP = 16
MAX_TEMP = 30
SCENES_DIR = "scenes"

DEVICES = {}


def add_device(name, kind, room="Living Room", settings=None):
    """Register a device. Each device gets its own copy of settings."""
    DEVICES[name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": dict(settings) if settings else {},
    }


def toggle_device(name):
    """Flip a device on/off. Return the new state, or None if not found."""
    if name in DEVICES:
        DEVICES[name]["on"] = not DEVICES[name]["on"]
        return DEVICES[name]["on"]
    print("Device not found:", name)
    return None


def set_temperature(name, value):
    """Set a thermostat's temperature, clamped to MIN_TEMP..MAX_TEMP."""
    device = DEVICES.get(name)
    if device is None:
        print("Device not found:", name)
        return False
    if device["kind"] != "thermostat":
        print(name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, MIN_TEMP), MAX_TEMP)
    return True


def devices_in_room(room):
    """Return the names of all devices in a room."""
    return [name for name, info in DEVICES.items() if info["room"] == room]


def power_usage():
    """Return total power draw (W) of devices that are switched on."""
    return sum(
        POWER_USAGE.get(info["kind"], 0)
        for info in DEVICES.values()
        if info["on"]
    )


def save_state(file_name="home_state.json"):
    """Write the current home state to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(DEVICES, file, indent=2)


def hub_address():
    """Return the hub address as host:port."""
    return f"{HUB_HOST}:{HUB_PORT}"


def run_scene(scene_script):
    """Run a scene script from SCENES_DIR (plain file name only, no paths)."""
    if os.path.basename(scene_script) != scene_script:
        raise ValueError("Scene name must be a plain file name")
    path = os.path.join(SCENES_DIR, scene_script)
    subprocess.run(["bash", path], check=True)  # nosec B603 B607


def main():
    """Run a short demonstration."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")

    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)

    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", DEVICES["Ceiling Light"]["settings"])
    on_now = [name for name, info in DEVICES.items() if info["on"]]
    print("Devices on:", on_now)
    save_state()


if __name__ == "__main__":
    main()
