#!/bin/bash
SCRIPT=$(realpath -s "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
echo "Uninstalling..."

sudo rm -rf /usr/share/coralsnakegame
sudo rm /usr/bin/coral-snake-game
sudo rm /usr/share/icons/hicolor/48x48/apps/coral-snake-game.png
sudo rm /usr/share/applications/coral-snake-game.desktop

echo "Done!"
echo "'Coral Snake Game' has been uninstalled."
echo
