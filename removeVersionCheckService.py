import os

service_file_path = "/etc/systemd/system/bedrock-version-check.service"

if os.path.exists(service_file_path):
    os.system("sudo systemctl stop bedrock-version-check.service")
    os.system("sudo systemctl disable bedrock-version-check.service")
    os.remove(service_file_path)
    os.system("sudo systemctl daemon-reload")
    print("Systemd service removed successfully.")
else:
    print("Systemd service file does not exist.")
