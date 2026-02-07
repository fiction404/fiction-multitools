# 🛠️ Fiction Multitool

> Un outil modulaire, extensible et léger écrit en Python pur.

![Version](https://img.shields.io/badge/version-0.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 À propos

Son architecture **modulaire** permet d'ajouter, de supprimer ou de modifier des outils ("plugins") sans toucher au cœur du programme. Il est conçu pour fonctionner sans dépendances externes lourdes, utilisant principalement la librairie standard de Python pour une portabilité maximale.

### ✨ Fonctionnalités clés
* **Architecture Plugin :** Ajoutez simplement un fichier `.py` dans le dossier `modules/` pour créer un nouvel outil.
* **Cross-Platform :** Fonctionne nativement sur Windows, Linux et MacOS.
* **Léger :** Pas de `pip install` complexe requis pour le cœur du système.
* **Interface Unifiée :** Gestion des couleurs et des menus intégrée.

---

## 🚀 Installation

1.  Assurez-vous d'avoir **Python 3.x** installé sur votre machine.
2.  Clonez ce dépôt ou téléchargez l'archive :

```bash
git clone https://github.com/fiction404/fiction-multitool.git
cd fiction-multitools

```

---

## ⚡ Démarrage Rapide

### 🪟 Sur Windows

Il suffit de double-cliquer sur le fichier `start.bat` présent à la racine du projet.

Ou via l'invite de commande :

```cmd
start.bat

```

### 🐧 Sur Linux / MacOS

Vous devez d'abord rendre le script de lancement exécutable (à faire une seule fois), puis le lancer.

```bash
# 1. Rendre exécutable
chmod +x start.sh

# 2. Lancer
./start.sh

```

---

## 📂 Structure du projet

```text
fiction-multitools/
├── start.bat              # Lanceur Windows
├── start.sh               # Lanceur Linux/Mac
├── README.md              # Documentation
└── src/
    ├── main.py            # Point d'entrée principal
    ├── core/              # Cœur du système (UI, Config, Interface)
    ├── config/            # Fichiers de configuration (générés auto)
    └── modules/           # Dossier contenant vos plugins

```


## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
