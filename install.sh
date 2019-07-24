read -p "Enter AdafruitIO username: " aiousername
read -s -p "Enter AdafruitIO Secret Key: " aiokey
printf "\n"
read -p "Enter any remaining arguments for logger daemon: " loggerargs
crontab -l | { cat; echo "@reboot python3 ${PWD}/logger.py $aiousername $aiokey $loggerargs"; } | crontab -
crontab -l | { cat; echo "@reboot python3 -m http.server --directory ${PWD}"; } | crontab -
