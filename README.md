# Bedrock Server Manager

Bedrock Server Manager is a tool/set of scripts that lets you easily set up and manage your own dedicated Bedrock server.

## Key Features
Install the latest server software, statup the server on machine boot, check for updates periodically, and update if there are updates.


## Dependencies

Before running the scripts, ensure the following dependencies are installed:
- Ubuntu Server, LTS, or Latest. (No Desktop Manager is required)
- python3 & pip3
- selenium: Install both as sudo and as user:
- ```sudo apt-get -y install python3-selenium```
- ```pip3 install selenium  #no worries if you get a satified requirement message. Your all good and can ignore this step.```
- The commands below generally will already be installed from above commands but, here they are just in case
```sudo snap install chromium```
```sudo apt-get -y install chromium-chromedriver```
## Installation

Clone the BedrockServerManager to a fixed location on your filesystem. If you move it, you will encounter issues. Run all scripts from the root of the BedrockServerManager directory. Remember to manually backup your server software/worlds occasionally! Follow the steps below exactly and you should be good to go!

1. ### Configure the Config File
Modify the config.json, ensuring to include the file separator at the end of ServerPath. Duration is how often you want the server to check for an update.

```
{
    "ServerPath": "/home/mitch/",
    "Flavor": "Linux",
    "Duration": 43200
}
```

For installing the preview version, prefix 'Preview' before your flavor choice:

```
{
    "Flavor": "PreviewLinux"
}
```

2. ### Install a fresh Server

Install a fresh copy of the server. Do not run this script as root, sudo, or su.

```
python3 install.py
```

Make sure to configure your server.properties, like the port number, etc... at this point if you need to.

3. ### Start server on boot

Create a service. This allows the server software to run on boot.

```
sudo python3 createMinecraftService.py
```

4. ### Auto Updating
Create the Manager Service
```
sudo python3 createManagerService.py
```

Create the Version Check service.

```
sudo python3 createVersionCheckService.py
sudo reboot
```
That's it!

Checkout the github wiki for updates and more in depth docs for installation and features :)
