<img src="https://raw.githubusercontent.com/MitchellKopczyk/BedrockServerManager/main/minecraft.png" width="200" height="200">

# Bedrock Server Manager

Bedrock Server Manager is a tool/set of scripts that lets you easily set up and manage your own dedicated Bedrock server.

## Key Features
Install the latest server software, statup the server on machine boot, check for updates periodically, and update if there are updates.


## Dependencies

Before running the scripts, ensure the following dependencies are installed:
- Ubuntu, python3, & pip3
- selenium: Install both as sudo and as user:
- ```sudo apt-get -y install python3-selenium```
- ```pip3 install selenium```
- chromium: Install using snap or your choice: ```sudo snap install chromium```
- chromedriver: Install using apt: ```sudo apt-get -y install chromium-chromedriver```
## Installation

Clone the BedrockServerManager to a fixed location on your filesystem. If you move it, you may encounter issues. Run all scripts from the root of the BedrockServerManager directory. Remember to manually backup your server software/worlds occasionally! Follow the steps below exactly and you should be good to go!

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
That's it! Feel free to play around with scripts and make them work for your application.

Please checkout the wiki for updates and the overall status of the project.
