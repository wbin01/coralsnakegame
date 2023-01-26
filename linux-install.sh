#!/bin/bash
SCRIPT=$(realpath -s "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
echo "Installing..."

sudo cp -r $SCRIPTPATH /usr/share/
sudo cp $SCRIPTPATH/coral-snake-game /usr/bin/
sudo cp $SCRIPTPATH/coral-snake-game.png /usr/share/icons/hicolor/48x48/apps/
sudo cp $SCRIPTPATH/coral-snake-game.desktop /usr/share/applications/

echo "Done!"
echo "'Coral Snake Game' has been installed."
echo
