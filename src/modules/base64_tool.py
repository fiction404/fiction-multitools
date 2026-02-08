import base64
from core.plugin_interface import Tool
from core.ui import UI

class Base64Tool(Tool):
    @property
    def name(self):
        return "Base64Tool"

    @property
    def description(self):
        return "Transforme du texte en Base64 et inversement."

    def execute(self):
        UI.print_info("1. Encoder du texte")
        UI.print_info("2. Décoder du texte")
        choice = UI.ask("Votre choix :")

        if choice == "1":
            text = UI.ask("Texte à encoder :")
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            UI.print_success(f"Résultat : {encoded}")

        elif choice == "2":
            text = UI.ask("Chaîne Base64 à décoder")
            try:
                decoded = base64.b64decode(text).decode('utf-8')
                UI.print_success(f"Résultat : {decoded}")
            except Exception:
                UI.print_error("Impossible de décoder. Chaîne invalide.")
        else:
            UI.print_error("Choix invalide.")