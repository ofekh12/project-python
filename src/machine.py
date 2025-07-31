import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', force=True)

class Machine:
    def __init__(self, name, os, cpu, ram):
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram = ram
        logging.info(f"Machine created: '{self.name}'")

    def to_dict(self):
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram
        }
