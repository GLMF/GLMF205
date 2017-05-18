# Développement rapide d'applications GTK+ avec Glade
par Christophe BORELLY [Professeur de l'ENSAM – IUT de Béziers]

---

Glade [3] est un outil de développement rapide d'applications GTK+ et il permet de réaliser graphiquement à la souris l'essentiel de l'interface utilisateur. Je vais donc vous présenter son fonctionnement et ce qu'il apporte au niveau programmation.

---

Nécessite les paquets: cmake, pkg-config, libgtk-3-dev (minimum 3.10)

tar xvf cb-glade-tictactoe.tar.xz
cd cb-glade-tictactoe
cmake .
make

Pour installer les icones de l'application :
sudo make -C icons

Tester ensuite les programmes d'exemple :
./glade-01
./glade-02-1
./glade-02-2
...
./tictactoe-1
./tictactoe-2
./tictactoe-3
...

Pour désinstaller les icones de l'application :
sudo make -C icons uninstall
