import json
import logging
import os
import subprocess
from pathlib import Path
from jsonschema import validate, ValidationError
from src.machine import Machine

project_root = Path(__file__).resolve().parent
(project_root / "logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(project_root / "logs" / "provisioning.log"),
    level=logging.DEBUG,
    format='%(asctime)s -%(levelname)s: %(message)s',
    force=True,
)

# show logs on console (errors and success messages)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logging.getLogger().addHandler(console_handler)

# JSON schema for VM validation
vm_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "os": {"type": "string", "enum": ["linux", "centos", "windows","win"]},
        "cpu": {"type": "number", "minimum": 0.1},
        "ram": {"type": "number", "minimum": 0.1}
    },
    "required": ["name", "os", "cpu", "ram"],
    "additionalProperties": False
}

# Validation helper
def validate_vm_data(instance):
    """Validate a VM dict against the JSON schema; returns (is_valid, error_message)."""
    try:
        validate(instance=instance, schema=vm_schema)
        return True, None
    except ValidationError as e:
        logging.error(f"Invalid input: {e.message}")
        return False, e.message

# helper to run installer per single machine
def run_script_for_machine(machine_name):
    try:
        script_path = (project_root / "scripts" / "install.sh").as_posix()
        subprocess.run(
            ["bash", script_path],
            check=True,
            cwd=project_root,
        )
        logging.info(f"Service installation completed for '{machine_name}'.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install service on '{machine_name}': {e}")
    except FileNotFoundError:
        logging.error("Bash not found. Ensure Git Bash or WSL is installed and accessible.")

# Interactive input
def vm_input():
    """Collect VM definitions interactively. Supports 'done' to finish and 'EXIT' to save-and-quit.
    Each field (name, OS, CPU, RAM) re-prompts until valid to avoid restarting the whole flow.
    """
    vm_list = []
    should_exit = False
    allowed_os_values = {"linux", "centos", "windows", "win"}

    while True:
        # Name loop
        finish_now = False
        while True:
            name = input("Enter machine name (or 'done' to finish, or 'EXIT' to quit): ").strip()
            low = name.lower()
            if low == "exit":
                should_exit = True
                break
            if low == "done":
                finish_now = True
                break
            if not name:
                logging.error("Machine name cannot be empty. Please try again.")
                continue
            break
        if should_exit or finish_now:
            break

        # OS loop
        while True:
            os_type = input("Enter OS (linux/centos/windows) or 'EXIT': ").strip()
            if os_type.lower() == "exit":
                should_exit = True
                break
            os_type = os_type.lower()
            if os_type not in allowed_os_values:
                logging.error("OS must be one of: linux, centos, windows, win. Please try again.")
                continue
            break
        if should_exit:
            break

        # CPU loop
        while True:
            cpu_str = input("Enter CPU (e.g., 2) or 'EXIT': ").strip()
            if cpu_str.lower() == "exit":
                should_exit = True
                break
            try:
                cpu = float(cpu_str)
                if cpu <= 0:
                    logging.error("CPU must be greater than 0. Please try again.")
                    continue
                break
            except ValueError:
                logging.error("CPU must be a valid number. Please try again.")
                continue
        if should_exit:
            break

        # RAM loop
        while True:
            ram_str = input("Enter RAM (e.g., 4) or 'EXIT': ").strip()
            if ram_str.lower() == "exit":
                should_exit = True
                break
            try:
                ram = float(ram_str)
                if ram <= 0:
                    logging.error("RAM must be greater than 0. Please try again.")
                    continue
                break
            except ValueError:
                logging.error("RAM must be a valid number. Please try again.")
                continue
        if should_exit:
            break

        machine_data = {
            "name": name,
            "os": os_type,
            "cpu": cpu,
            "ram": ram,
        }

        is_valid, err_msg = validate_vm_data(machine_data)
        if is_valid:
            machine = Machine(**machine_data)
            vm_list.append(machine.to_dict())
            logging.info(f"Machine '{name}' added successfully.")

            # Ask for per-machine service installation
            while True:
                answer = input("Do you want to install a service on this machine? (y/n or 'EXIT'): ").strip().lower()
                if answer == "exit":
                    should_exit = True
                    break
                if answer in ("y", "yes"):
                    run_script_for_machine(name)
                    break
                if answer in ("n", "no"):
                    break
                logging.info("Please enter 'y' or 'n' (or 'EXIT' to quit).")
        else:
            logging.error(f"Invalid input: {err_msg}")
            # Go back to start of machine entry (fields will be asked again)
            continue

        if should_exit:
            break

    return vm_list


if __name__ == "__main__":
    instances = vm_input()
    configs_path = project_root / "configs" / "instances.json"
    with open(configs_path, "w") as file:
        json.dump(instances, file, indent=4)
    logging.info(
        f"Provisioning completed. Saved {len(instances)} machine(s) to {configs_path}"
    )

    # Summary
    if instances:
        logging.info("Machines defined:")
        for i, inst in enumerate(instances, start=1):
            logging.info(
                f"  {i}. name={inst['name']}, os={inst['os']}, cpu={inst['cpu']}, ram={inst['ram']}"
            )
