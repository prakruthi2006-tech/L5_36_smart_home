# Lab 5 - Reflection

## 1. Which problems did the tools find, and which did they miss?

Pylint, Bandit and Flake8 together found the naming, docstring and formatting problems, the `shell=True` command injection risk in `run_scene` (High), the `0.0.0.0` bind (Medium), the hardcoded password (Low) and the dangerous default argument `settings={}`. They did not tell me what that default argument actually caused. The program printed `Light settings: {'temperature': 30}`, so every device shared one settings dictionary and the thermostat's temperature leaked into the light. I only noticed it by reading the output. The tools also did not flag that `set_temperature` crashes with a `KeyError` on an unknown device, or that `main()` runs on import with no `__main__` guard.

## 2. Were there warnings that were not worth fixing, or that needed a judgement call?

Bandit warned about `import subprocess` (B404, Low). I kept the import because `run_scene` needs it, and made the call safe by using an argument list without `shell=True` and rejecting scene names that contain a path, then marked the import `# nosec B404`. `HUB_PASSWORD` was flagged as a hardcoded password, but it was never used, so the correct fix was to delete it. Docstring warnings are low risk, but they are cheap to fix and make the code easier to read.

## 3. Which tool was most useful?

Bandit was the most important, because it found the one High severity issue and the open network bind, which are real security problems. Pylint found the most issues overall (4.80/10 at the start) and its W0102 warning pointed to the real bug. Flake8 only covers formatting, so it was the least important, but it is quick to satisfy.

## 4. How would I use these tools in a real project, and what did I learn?

I would run all three in CI on every pull request, and fail the build on High severity Bandit findings. After my fixes Pylint went from 4.80/10 to 10.00/10, Bandit from 4 findings (1 High, 1 Medium, 2 Low) to none, and Flake8 from 4 findings to none, and the program still works the same. I also learned that clean reports do not prove the program is correct. The shared-settings bug would have passed a lint check if I had not run the program and looked at what it printed.
