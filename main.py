#UnicornAp 1.0
import os

print("\033[0;31m"+
"""
888     888          d8b                                          d8888          
888     888          Y8P                                         d88888          
888     888                                                     d88P888          
888     888 88888b.  888  .d8888b .d88b.  888d888 88888b.      d88P 888 88888b.  
888     888 888 "88b 888 d88P"   d88""88b 888P"   888 "88b    d88P  888 888 "88b 
888     888 888  888 888 888     888  888 888     888  888   d88P   888 888  888 
Y88b. .d88P 888  888 888 Y88b.   Y88..88P 888     888  888  d8888888888 888 d88P 
 "Y88888P"  888  888 888  "Y8888P "Y88P"  888     888  888 d88P     888 88888P"  
                                                                        888
                                                                        888    
                                                                        888
"""+'\033[0;m'+
"""By MByte 
Version 0.1""")
##Variables Globales
dir_hostapdconf="/etc/hostapd/hostapd.conf" 

#Update
install_d=input("Desea instalar dependencias?(S/n): ")
if install_d==install_d.lowwer == "s":
    os.system("apt update")
    os.system("apt install hostapd")
    os.system("apt install isc-dhcp-server")


#Preguntas
interfaceAp=input("Ingrese nombre de la interface inalambrica: ")
interfaceInternet=input("Ingrese nombre de la interface conectada a internet: ")
nombreRedWifi=input("Nombre de la red que desea crear: ")
canal=input("Ingrese nombre del canal a usar(1-11): ")
seguridad_d=input("Desea que la red tenga password(y/n):  ")

if seguridad_d=="y" or seguridad_d=="Y" :
    passwordWifi=input("Ingrese un password para el punto de Acceso: ")
    hostapdString = "interface=" + interfaceAp + "\ndriver=nl80211\nssid=" + nombreRedWifi + "\nhw_mode=g\nchannel=" + canal + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase=" + passwordWifi + "\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP\n"
else:
    hostapdString = "interface=" + interfaceAp + "\ndriver=nl80211\nssid=" + nombreRedWifi + "\nhw_mode=g\nchannel=" + canal + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\n"



sslstrip_d=input("Desea activar Sslstrip+: ")
dnsSpoofing_d=input("Desea activar DnsSpoofing: ")












