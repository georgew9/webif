# webif
raspberrypi 4 web UI for setting LAN and Wifi , base on flask + bootstrap

1. UI is Chiness languge
2. LAN page change the /etc/dhcpcd.conf file
3. wifi page change the /etc/wpa_supplicant/wpa_supplicant.conf file
4. username and password(hashed) save in 'users' file

# Run
sudo python3 webu.py

browser th RPi's IP 80 port (default username/Password: admin / 123456)

