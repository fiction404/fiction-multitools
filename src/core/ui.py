import os
import sys
import pathlib
import getpass

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"

class UI:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def banner():
        banner="""  
 ███████████  ███            █████     ███                     
░░███░░░░░░█ ░░░            ░░███     ░░░                      
 ░███   █ ░  ████   ██████  ███████   ████   ██████  ████████  
 ░███████   ░░███  ███░░███░░░███░   ░░███  ███░░███░░███░░███ 
 ░███░░░█    ░███ ░███ ░░░   ░███     ░███ ░███ ░███ ░███ ░███ 
 ░███  ░     ░███ ░███  ███  ░███ ███ ░███ ░███ ░███ ░███ ░███ 
 █████       █████░░██████   ░░█████  █████░░██████  ████ █████
░░░░░       ░░░░░  ░░░░░░     ░░░░░  ░░░░░  ░░░░░░  ░░░░ ░░░░░ 
                                                                                                                                        
            42 79 20 66 69 63 74 69 6F 6E 34 30 34  
        """
        UI.clear()
        print(f"{Colors.CYAN}")
        print(banner)
        print(f"{Colors.BOLD} v0.0 - Full Standard Lib{Colors.RESET}\n")
        print(f"{Colors.GREEN}Ecrire 'help' pour afficher les commandes disponibles.\n{Colors.RESET}")
        

    @staticmethod
    def print_menu(options):
        for i, option in enumerate(options, 1):
            print(f"{Colors.GREEN}[{i}] {option}{Colors.RESET}")

    @staticmethod
    def print_warning(message):
        print(f"{Colors.YELLOW}[!] {message}{Colors.RESET}")

    @staticmethod
    def print_success(message):
        print(f"{Colors.GREEN}[+] {message}{Colors.RESET}")

    @staticmethod
    def print_error(message):
        print(f"{Colors.RED}[!] {message}{Colors.RESET}")

    @staticmethod
    def print_info(message):
        print(f"{Colors.BLUE}[*] {message}{Colors.RESET}")

    @staticmethod
    def ask():
        user = getpass.getuser() 
        pwd = pathlib.Path.cwd()
        return input(f"""{Colors.GREEN}┌──({Colors.RED}{user}@Fiction{Colors.GREEN}─[{Colors.BLUE}{pwd}{Colors.GREEN}]{Colors.RESET}
{Colors.GREEN}└─{Colors.RED}$ {Colors.RESET}""")