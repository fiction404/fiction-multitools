import importlib.util
import inspect
import os
import sys
from typing import List

from core import UI, ConfigManager, Tool


def default_modules_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "modules")


def load_modules(modules_dir: str | None = None) -> List[Tool]:
    if modules_dir is None:
        modules_dir = default_modules_dir()

    if not os.path.exists(modules_dir):
        UI.print_error(f"Le dossier '{modules_dir}' n'existe pas.")
        return []

    loaded_modules: List[Tool] = []

    for filename in os.listdir(modules_dir):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        module_name = filename[:-3]
        file_path = os.path.join(modules_dir, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Tool) and obj is not Tool:
                    try:
                        tool_instance = obj()
                        loaded_modules.append(tool_instance)
                    except Exception as e:
                        UI.print_error(f"Erreur lors de l'instanciation de {obj}: {e}")
        except Exception as e:
            UI.print_error(f"Erreur lors du chargement de {filename} : {e}")

    return loaded_modules


def build_menu_items(tools: List[Tool]) -> List[str]:
    items = [
        "exit  - Quitter l'application",
        "help  - Afficher ce menu d'aide",
        "clear - Effacer l'écran",
    ]

    for tool in tools:
        items.append(f"{tool.name} - {tool.description}")

    return items


def run_cli(modules_dir: str | None = None) -> None:
    config = ConfigManager()
    UI.banner(config.get("info"))

    if config.get("error"):
        try:
            UI.print_warning(config.warning())
        except Exception:
            UI.print_warning("Configuration: erreur détectée.")

    tools = load_modules(modules_dir)
    UI.print_success(f"{len(tools)} outils chargés.")

    while True:
        command = UI.cmd().strip().lower()

        if command in ("help", "1"):
            UI.print_menu(build_menu_items(tools))
            continue

        if command in ("clear", "2"):
            UI.banner(config.get("info"))
            continue

        if command in ("exit", "0"):
            UI.print_success("Au revoir !")
            break

        if command.isdigit():
            choice = int(command)
            tool_index = choice - 3
            if 0 <= tool_index < len(tools):
                try:
                    tools[tool_index].execute()
                except Exception as e:
                    UI.print_error(f"Le tool a planté : {e}")
            else:
                UI.print_warning("Numéro invalide.")
            continue

        found = False
        for tool in tools:
            if tool.name.lower() == command:
                found = True
                try:
                    tool.execute()
                except Exception as e:
                    UI.print_error(f"Le tool a planté : {e}")
                break

        if not found:
            UI.print_warning(f"Commande '{command}' inconnue. Tapez 'help' pour la liste.")


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()

