To start a process or application automatically on Raspberry Pi at startup, use systemd service files.
Systemd service files can be found at cd /lib/systemd/system/
e.g. reboot_logging.service or soil_moisture.service


Step 1 - Create a Unit File
[Unit]
Description=My Sample Service
After=mulit-user.target

[Service]
Type=idle
ExecStart =/usr/bin/python /home/pi/sample.py

[Install]
WantedBy=multi-user.target

The permission on the file needs to be set to 644:
sudo chmod 644 /lib/systemd/system/sample.service

Step 2 - Configure systemd
sudo systemctl daemon-reload
sudo systemctl enable sample.service
sudo reboot

Step 3 - Check Status

sudo systemctl status sample.service
