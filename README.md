## Infrastructure Automation Simulator (Python)

A simple, modular simulator for provisioning virtual machines (VMs) and running a mock service installation via Bash. Future iterations can integrate AWS/Terraform to create real resources.

### Features
- Interactive VM input with per-field validation (name, OS, CPU, RAM)
- JSON Schema validation for the final VM object
- Clean class-based model (`src/machine.py`)
- Optional service installation after each VM using a Bash script (mocked)
- Logging to file and console

### Project Structure
```
infra-automation/
├─ src/
│  └─ machine.py
├─ scripts/
│  └─ install.sh
├─ configs/
│  └─ instances.json        # created/overwritten on each run
├─ logs/
│  └─ provisioning.log      # auto-created and appended by Python/Bash
├─ infra_simulator.py
├─ requirements.txt
└─ README.md
```

### Requirements
- Python 3.10+
- Windows users: Git Bash or WSL (so that `bash` is available to run `scripts/install.sh`)

### Setup
1) Create and activate a virtual environment
- Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
- macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

### Run
```bash
python infra_simulator.py
```

### What to expect (flow)
- You will be prompted to enter VM details.
  - Name: cannot be empty
  - OS: linux / centos / windows / win
  - CPU, RAM: positive numbers
  - Each field re-prompts until valid (no need to start over)
- After each valid VM is added, you will be asked:
  - "Do you want to install a service on this machine? (y/n or 'EXIT')"
  - If you choose y, the Bash script (`scripts/install.sh`) runs and asks you to type the service name. It then simulates an installation and logs it.
- Type `done` at the machine name prompt to finish.
- The final list is saved to `configs/instances.json` and a short summary prints to the console/log.

### Logging
- Python logs: `logs/provisioning.log` (auto-created)
- Bash logs: appended to the same file
- Console: info/error messages are shown during the run

### Windows note
- Run the program from a shell that has `bash` available (Git Bash or WSL). If you run from PowerShell/CMD without Git Bash/WSL installed, the Bash step will fail.

### Troubleshooting
- "Bash not found": Install Git Bash or WSL and run again from that environment.
- Script prompts but doesn’t accept input: Ensure you didn’t run with redirected input; the program is fully interactive.
- Nothing written to `instances.json`: Make sure you finished the input with `done` at the machine name prompt.

### Next Steps (optional enhancements)
- Add stricter service validation in Bash or move validation to Python
- Persist state across runs and support appending rather than overwrite
- Integrate real provisioning flows (cloud SDKs, Terraform)
- Add tests and CI




