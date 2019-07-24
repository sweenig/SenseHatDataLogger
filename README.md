# SenseHatDataLogger

I ran across [this project](https://projects.raspberrypi.org/en/projects/sense-hat-data-logger) and decided to give it a try. It used to be much simpler than this. However, I recently ran across Adafruit.io and decided to try it out. I really like it, so I added cloud logging to the script instead of local file. Then I wanted to bring the data into another graphing tool I have, so I built a small API to deliver the data via json over port 8000. Run the install.sh to add the logger and api server to crontab. If you don't need the API server, just edit your crontab (crontab -e) and remove the line with "http.server" in it.  After running the installer, reboot. Goes without saying that you need the SenseHat installed on your RaspberryPi.

If you're interested, [my graphs are here](https://io.adafruit.com/sweenig/dashboards/environmentals).
