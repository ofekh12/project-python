import json
import logging
import os
import subprocess
from jsonschema import validate, ValidationError
from src.machine import Machine

logging.basicConfig(
    filename="logs/provisioning.log",
    level=logging.DEBUG, format='%(asctime)s -%(levelname)s: %(message)s', force=True)

# סכמה לוולידציה
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

# פונקציית ולידציה נפרדת
def validate_vm_data(instance):
    try:
        validate(instance=instance, schema=vm_schema)
        return True
    except ValidationError as e:
        logging.error(f"Invalid input: {e.message}")
        return False

# פונקציית קלט
def vm_input():
    vm_list = []
    while True:
       try:

        name = input("Enter machine name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            exit()
        if not name:
                logging.warning("[INPUT] Empty input received, prompting again")
                continue
            

        os_type = input("Enter OS (linux/centos/windows): ").strip().lower()

        cpu = float(input("Enter CPU (e.g., 2): "))
        ram = float(input("Enter RAM (e.g., 4): "))
       except ValueError:
            logging.error("CPU and RAM must be valid numbers.")
            continue

       machine_data = {
            "name": name,
            "os": os_type,
            "cpu": cpu,
            "ram": ram
        }

       if validate_vm_data(machine_data):
            # רק אם תקין יוצרים את האובייקט
            machine = Machine(**machine_data)
            vm_list.append(machine.to_dict())
            logging.info("Machine added successfully.")
       else:
            logging.warning("Machine not added due to validation error.")

       return vm_list

# הפעלת התוכנית
instances = vm_input()

# שמירת הנתונים
os.chdir(os.path.dirname(__file__))
with open("configs/instances.json", "w") as file:
    json.dump(instances, file, indent=4)

def run_script():
    try:
        subprocess.run(["bash", "scripts/install.sh" ],check=True)
        logging.info("server installation completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f" Failed to install server: {e}")

if __name__ == "__main__":
    run_script()
