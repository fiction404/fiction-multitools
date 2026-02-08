import socket
from core.plugin_interface import Tool
from core.ui import UI

class PortScanner(Tool):
    @property
    def name(self):
        return "PortScanner"

    @property
    def description(self):
        return "Vérifie si un port est ouvert sur une IP cible."

    def execute(self):
        target = UI.ask("Entrez l'adresse IP cible (ex: 127.0.0.1) :")
        
        if not target:
            UI.print_error("IP invalide.")
            return

        port_input = UI.ask("Entrez le port à scanner (ex: 80) :")
        
        try:
            port = int(port_input)
        except ValueError:
            UI.print_error("Le port doit être un nombre.")
            return

        UI.print_info(f"Scan de {target}:{port} en cours...")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2) 
        
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                UI.print_success(f"Le port {port} est OUVERT !")
            else:
                UI.print_error(f"Le port {port} est FERMÉ.")
        except Exception as e:
            UI.print_error(f"Erreur de connexion : {e}")
        finally:
            sock.close()