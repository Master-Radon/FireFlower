sudo apt upgrade -y
sudo apt update -y
sudo apt-get install iptables -y
sudo apt install ufw -y
sudo apt install build-essential libsystemd-dev -y
sudo apt install libsystemd-daemon-dev libsystemd-journal-dev -y
sudo pip install systemd-python
sudo pip install pyufw
sudo ufw enable -y
sudo pip install python-crontab
echo 'export $PATH=PATH:/home/FireFlower' >> ~/.bashrc