# AppTempRasp
Une fois l'application [*Température By Raspberry*](https://play.google.com/store/apps/details?id=fr.espace_raspberry_francais.espaceraspberry) installée, il suffit de suivre ce ReadMe pour lier l'application et le Raspberry Pi.

## Brancher la sonde au Raspberry Pi
La sonde se connecte au Raspberry en suivant le Schéma suivant :
![Schéma de branchement](http://espace-raspberry-francais.fr/Projets/Courbe-temp%C3%A9rature-accessible-avec-un-server-Web-Python/Images/Schema-Branchement-Raspberry-Model.3-DS18B20.png)

## Installer le git
Entrer les commandes suivantes pour télécharger le projet :
``` 
cd ~
git clone https://github.com/EspaceRaspberryFrancais/AppTempRasp.git
```

## Obtenir la référence de la sonde DS18B20 et actualiser le code
Pour que le code fonctionne, il faut modifier le code de *app.py* et renseigner le numéro de la sonde DS18B20. Pour obtenir ce numéro, entrer les commandes suivantes :
```
sudo modprobe w1-gpio
sudo modprobe w1-therm
ls /sys/bus/w1/devices/
```
Ceci renvoie quelque chose comme :
> **28-0317229e0bff**  w1_bus_master1

La référence de la sonde est la partie en gras, il faut la recopier et le coller dans le fichier *app.py*, dans la variable ***referenceSonde***.
