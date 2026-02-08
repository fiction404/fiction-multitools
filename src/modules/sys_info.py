import platform
import sys
import os
from core.plugin_interface import Tool
from core.ui import UI

class SystemInfo(Tool):
    @property
    def name(self):
        return "Infos Système"

    @property
    def description(self):
        return "Affiche les détails de la machine et de l'OS."

    def execute(self):
        UI.print_info("Récupération des informations...")
        
        info = {
            "Système d'exploitation": platform.system(),
            "Version de l'OS": platform.release(),
            "Architecture": platform.machine(),
            "Processeur": platform.processor(),
            "Version Python": sys.version.split()[0],
            "Utilisateur": os.getlogin() if hasattr(os, 'getlogin') else "Inconnu"
        }

        print("\n" + "-"*30)
        for key, value in info.items():
            # On utilise un simple print ici pour faire un tableau propre
            print(f"{key:.<25}: {value}")
        print("-"*30 + "\n")
        
        UI.print_success("Analyse terminée.")