import os
import shutil
import getpass
import utils

config = utils.load_json_file("config.json")
server_path = config["ServerPath"]
dir_name = "bedrock-server"

script_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + "versionCheck.py"

unit_file_content = f"""[Unit]
Description=Version Check for MinecraftBedrockServerManager

[Service]
User={getpass.getuser()}
WorkingDirectory={os.path.dirname(script_path)}
ExecStart=/usr/bin/python3 {script_path}
Restart=no

[Install]
WantedBy=multi-user.target
"""

service_file_path = "/etc/systemd/system/bedrock-version-check.service"

with open(service_file_path, "w") as service_file:
    service_file.write(unit_file_content)

os.system("sudo systemctl daemon-reload")

os.system("sudo systemctl enable bedrock-version-check.service")

print("Systemd service created successfully.")
print("Please reboot your machine")
