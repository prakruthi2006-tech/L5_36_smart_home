# Lab 5 - Issues in smart_home.py

Line numbers: fill from your own pylint/bandit/flake8 reports (original file). Locations below are by function or name.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Shell command injection (`shell=True` with string concatenation) | Security (Bandit B602, High) | `runScene` | Scene name is concatenated into a shell command, so input like `x; rm -rf ~` would execute. | Pass an argument list, drop `shell=True`, reject names containing paths. **Fixed** |
| Hub binds to all interfaces | Security (Bandit B104, Medium) | `HUB_HOST = "0.0.0.0"` | Exposes the hub to the whole network. | Bind to `127.0.0.1`. **Fixed** |
| Mutable default argument `settings={}` | Bug (Pylint W0102) | `addDevice` | One dict is shared by every device. Output shows `Light settings: {'temperature': 30}` because the thermostat change leaks into the light (and TV, fan). | Default to `None`, give each device its own `dict`. **Fixed** |
| Hardcoded password | Security (Bandit B105, Low) | `HUB_PASSWORD` | Secret in source control, and it is never used. | Removed (if needed later, read from an environment variable). **Fixed** |
| Crash on unknown device | Bug | `setTemperature` | `devices[deviceName]` raises `KeyError` for a missing device, unlike `toggleDevice` which handles it. | Use `.get()` and return `False` with a message. **Fixed** |
| Inconsistent return | Quality (Pylint R1710) | `toggleDevice` | Returns a bool when found but falls through to implicit `None` when not found. | Explicit `return None`, documented in docstring. **Fixed** |
| No `__main__` guard | Quality | bottom of file | `main()` runs on import, so the module can't be reused or tested. | `if __name__ == "__main__":`. **Fixed** |
| Naming style | Style (Pylint C0103) | all functions, `devices` | camelCase functions and lowercase module-level global. | snake_case functions, `DEVICES`. **Fixed** |
| Missing docstrings | Style (Pylint C0114/C0116) | module + every function | No documentation. | Added docstrings. **Fixed** |
| `open()` without encoding | Quality (Pylint W1514) | `saveState` | Encoding depends on the OS default. | `encoding="utf-8"`. **Fixed** |
| String concatenation | Style (Pylint C0209) | `hubAddress` | `HOST + ":" + str(PORT)`. | f-string. **Fixed** |
| Formatting | Style (Flake8 E203, E302, E305, E261) | `POWER_USAGE`, blank lines, inline comment | Space before `:`, wrong blank lines, one space before `#`. | Reformatted to PEP 8. **Fixed** |
| Magic numbers 16 / 30 | Quality | `setTemperature` | Unexplained limits. | `MIN_TEMP` / `MAX_TEMP`. **Fixed** |
