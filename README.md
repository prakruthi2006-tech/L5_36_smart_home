# Lab 5: Static Code Analysis - Smart Home Device Controller

**Name:** [Prakruthi.NK]
**SRN:** [PES2UG24AM118]
**Section:** [5B]

## About

A small Python controller for smart home devices. It adds devices to rooms, switches them on and off, sets the thermostat within a safe range (16-30), lists devices by room, reports power use and saves the home state to `home_state.json`.

This lab uses static code analysis. The starting code worked but had quality, style and security problems. I found them with Pylint, Flake8 and Bandit, documented them, and fixed them.

## How to run

```
python smart_home.py
```

Expected output includes `Light settings: {}` and `Hub address: 127.0.0.1:8080`.

## Running the analysis tools

```
python -m pip install pylint bandit flake8
python -m pylint smart_home.py
python -m bandit -r smart_home.py
python -m flake8 smart_home.py
```

## Results

| | Before | After |
|---|---|---|
| Pylint | 4.80/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 |
| Flake8 | 4 issues | 0 |

## Main fixes

- **Shared settings bug:** `settings={}` was a mutable default argument, so every device shared one dictionary and the thermostat's temperature appeared on the light. Each device now gets its own copy.
- **Command injection:** `run_scene` used `shell=True` with string concatenation. It now uses an argument list and rejects scene names containing a path.
- **Open network bind:** the hub bound to `0.0.0.0`; it now binds to `127.0.0.1`.
- **Hardcoded password:** the unused `HUB_PASSWORD` was removed.
- **Robustness:** `set_temperature` no longer crashes on unknown devices, `toggle_device` returns consistently, and `main()` runs only under `if __name__ == "__main__"`.
- **Style:** snake_case names, docstrings, `encoding="utf-8"` and PEP 8 formatting.

## Files

| File | Purpose |
|---|---|
| `smart_home.py` | Cleaned controller |
| `issues.md` | Issues found, with line numbers and fixes |
| `reflection.md` | Reflection on what the tools found and missed |
| `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` | Reports on the original code |
| `pylint_report_after.txt`, `bandit_report_after.txt`, `flake8_report_after.txt` | Reports on the fixed code |
| `home_state.json` | State file written when the program runs |

## Key takeaway

The tools found most of the problems, but not all of them. The shared-settings bug showed up only by reading the program's output, so a clean report is not proof that the code is correct.
