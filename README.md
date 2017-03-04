# slack-random-picker-bot
Slack bot which picks a random person based on presence via network scanner. Run as root, otherwise mac addresses cannot be collected.

## Requirements
```
sudo apt-get install python python-pip nmap daemon
sudo pip install python-nmap
sudo pip install slackclient
```

## Run
Try it first with
```
sudo python random-picker-bot.py
```
Then you can demonize it and add it to /etc/rc.local to start on boot.
-r means respawn if it dies.
```
daemon -r sudo python random-picker-bot.py
```
