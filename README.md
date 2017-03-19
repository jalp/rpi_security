# Systemd
        sudo chmod 644 /lib/systemd/system/security.service

        sudo systemctl daemon-reload
        sudo systemctl enable security.service

        sudo reboot

## Check status
        sudo systemctl status security.service