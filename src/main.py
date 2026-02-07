from core import UI, Colors, ConfigManager, Tool

def main():
    config = ConfigManager()
    UI.banner()
    if config.get("error") and config.get("error") == True:
        UI.print_warning(config.warning())
        
    while True:
        command = UI.ask().strip().lower()
        if command == "help":
            UI.print_menu([
                "help - Afficher ce menu d'aide",
                "clear - Effacer l'écran et afficher la bannière",
                "exit - Quitter l'application"
            ])
        elif command == "clear":
            UI.banner()      
        elif command == "exit":
            UI.print_success("Au revoir !")
            break
        else:
            UI.print_warning("Commande inconnue. Tapez 'help' pour voir les commandes disponibles.")
    
if __name__ == "__main__":
    main()

