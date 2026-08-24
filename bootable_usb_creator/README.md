# Créateur de Clé USB Bootable (Bootable USB Creator)

Une application de bureau légère et facile à utiliser (similaire à Rufus), conçue pour copier les fichiers d'images de disque système (.iso) sur des clés USB et les rendre amorçables (bootables).

Ce projet a été initialement conçu selon les spécifications de l'ingénieur Mesbah Mourad, Wilaya de Menia, Algérie, et a été mis à jour avec une interface moderne en langue française.

## Fonctionnalités
* Interface utilisateur moderne et repensée avec `CustomTkinter`
* Interface complète en français
* Détection automatique des clés USB (et masquage des disques durs principaux pour plus de sécurité)
* Prise en charge de la sélection du schéma de partition (MBR ou GPT)
* Messages d'avertissement pour protéger l'utilisateur contre la perte accidentelle de données

## Prérequis techniques
* Python 3.x
* Environnement Windows (pour une compatibilité optimale avec les commandes système comme wmic et diskpart)

## Instructions d'utilisation

1. **Configurer un environnement virtuel (optionnel mais recommandé) :**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Installer les dépendances requises :**
```bash
pip install -r requirements.txt
```

3. **Lancer le programme (doit être exécuté en tant qu'administrateur) :**
```bash
python main.py
```

## Compilation (Windows)
Pour compiler le programme en un fichier exécutable `.exe` :
Exécutez le script `build.bat` fourni, ou utilisez la commande suivante après avoir installé PyInstaller :
```bash
pyinstaller --noconfirm --onedir --windowed --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --name "Createur_USB_Bootable" "main.py"
```

## Remarque importante
* Le programme nécessite les privilèges d'Administrateur pour interagir avec les lecteurs de disque.
* Soyez très prudent lors de la sélection de votre périphérique USB, car l'opération effacera toutes les données existantes.
