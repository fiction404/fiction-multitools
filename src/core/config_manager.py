import os
import json

class ConfigManager:
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.config = {}
        self.load()

    def load(self):
        if not os.path.exists(self.config_file):
            self.warning()
            self.config = {
                "info": 
                {
                    "version": "0.0", 
                    "name": "fiction-multitools"
                },
                "error": True
            }
            self.save()
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                if "error" in self.config and self.config["error"]:
                    self.warning()

    def save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key)
    
    def warning(self):
        return f"Warning: Fichier de configuration introuvable : {self.config_file} risque de mauvaise utilisation, veuillez réinstaller les outils."