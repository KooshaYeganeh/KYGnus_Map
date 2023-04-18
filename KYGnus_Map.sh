

cd /opt/KYGnus_Map


# In some Linux distributions, the command to run Python may be different. For example
# Ubuntu : python3 app.py
# peppermint : python3 app.py
# OpenSuse : python3 app.py
# Fodora : python app.py
## If there is a problem in running the program, one of the parts that you
##should consider in troubleshooting is changing the Python execution command

Fedora=` cat /etc/os-release | grep -o fedora | head -1`
Ubuntu=` cat /etc/os-release | grep -o ubuntu | head -1`
OpenSuse=` cat /etc/os-release | grep -o suse | head -1`


if [ "$Fedora" == "fedora" ];then
	sudo python app/main.py

elif [ "$Ubuntu" == "ubuntu" ];then
	sudo python3 app/main.py

elif [ "$OpenSuse" == "opensuse" ];then
	sudo python3 app/main.py
fi



