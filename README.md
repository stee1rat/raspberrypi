# raspberrypi
```
sudo cp monitor.service /lib/systemd/system/monitor.service
sudo cp stats.service /lib/systemd/system/stats.service

sudo systemctl enable monitor
sudo systemctl enable stats

sudo systemctl start monitor
sudo systemctl start stats
```
