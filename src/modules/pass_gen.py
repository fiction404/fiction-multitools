import random
import string
from core.plugin_interface import Tool
from core.ui import UI

class PasswordGenerator(Tool):
    @property
    def name(self):
        return "Générateur de MDP"

    @property
    def description(self):
        return "Crée un mot de passe sécurisé aléatoire."

    def execute(self):
        try:
            length_str = UI.ask("Longueur du mot de passe (défaut: 16) :")
            length = int(length_str) if length_str else 16
        except ValueError:
            UI.print_error("Veuillez entrer un nombre valide.")
            return

        if length < 4:
            UI.print_error("C'est trop court pour être sécurisé !")
            return

        # On définit les caractères possibles
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        
        # On génère le mot de passe
        password = "".join(random.choice(chars) for _ in range(length))
        
        UI.print_success("Mot de passe généré :")
        print(f"\n    {password}\n") # Affichage centré visuellement