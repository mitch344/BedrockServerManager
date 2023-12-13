import ssl
import urllib.request
import zipfile
import json
import os
import shutil
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_json_file(src):
    with open(src, "r") as f :
        return json.load(f)
    
config = load_json_file("config.json")
server_path = config["ServerPath"]
dir_name = "bedrock-server"

def get_version_number(url):
    pattern = r'bedrock-server-(\d+\.\d+\.\d+\.\d+)\.zip'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
    
def get_latest_version_info(serverType):
    url = 'https://www.minecraft.net/en-us/download/server/bedrock'
    options = Options()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@data-platform]")))

    grabbed_urls = [link.get_attribute('href') for link in links]
    grabbed_platforms = [link.get_attribute('data-platform') for link in links]

    driver.quit()

    if serverType < len(grabbed_urls):
        infoDict = {
            'version': get_version_number(grabbed_urls[serverType]),
            'download_url': grabbed_urls[serverType]
        }
        infoJSON = json.dumps(infoDict)
        return infoJSON
    else:
        return "Server type index out of range"

def get_latest_version_info_to_file(serverType):
    url = 'https://www.minecraft.net/en-us/download/server/bedrock'
    options = Options()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@data-platform]")))

    grabbed_urls = [link.get_attribute('href') for link in links]
    grabbed_platforms = [link.get_attribute('data-platform') for link in links]
    
    driver.quit()

    if serverType < len(grabbed_urls):
        infoDict = {
            'version': get_version_number(grabbed_urls[serverType]),
            'download_url': grabbed_urls[serverType]
        }
        print(os.path.dirname(__file__) + os.path.sep + 'current_version.json')
        write_to_json(json.dumps(infoDict), os.path.dirname(__file__) + os.path.sep + 'current_version.json')
    else:
        return "Server type index out of range"

def download_stream(url) :
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(url, context=context)
    return response.read()

def write_stream(dst, stream) :
    with open(dst, "wb") as f:
        f.write(stream)

def unzip(src, dst) :
    with zipfile.ZipFile(src, "r") as z:
        z.extractall(dst)


def write_to_json(data, dst):
    with open(dst, "w") as outfile :
        json.dump(data, outfile)

def compare_versions(v1, v2) :
    v1_parts = v1.split('.')
    v2_parts = v2.split('.')
    for i in range(min(len(v1_parts), len(v2_parts))):
        if int(v1_parts[i]) > int(v2_parts[i]):
            return True
        elif int(v1_parts[i]) < int(v2_parts[i]):
            return False
    if len(v1_parts) > len(v2_parts):
        return True
    elif len(v1_parts) < len(v2_parts):
        return False
    else:
        return False
    
flavors = {
    "Windows": 0,
    "Linux": 1,
    "PreviewWindows": 2,
    "PreviewLinux": 3
}

def print_backup(value):
    print("Backing up %s..." % (value,))

def print_restore(value):
    print("Restoring %s..." % (value,))

def backup(server_path, dir_name, backup_path):
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    if os.path.exists(server_path + dir_name + os.path.sep + "worlds"):
        shutil.copytree(server_path + dir_name + os.path.sep + "worlds", backup_path + os.path.sep + "worlds")
        print_backup("worlds")

    if os.path.exists(server_path + dir_name + os.path.sep + "resource_packs"):
        shutil.copytree(server_path + dir_name + os.path.sep + "resource_packs", backup_path + os.path.sep + "resource_packs")
        print_backup("resource_packs")

    if os.path.exists(server_path + dir_name + os.path.sep + "behavior_packs"):
        shutil.copytree(server_path + dir_name + os.path.sep + "behavior_packs", backup_path + os.path.sep + "behavior_packs")
        print_backup("behavior_packs")

    if os.path.exists(server_path + dir_name + os.path.sep + "server.properties"):
        shutil.copy(server_path + dir_name + os.path.sep + "server.properties", backup_path)
        print_backup("server.properties")

    if os.path.exists(server_path + dir_name + os.path.sep + "allowlist.json"):
        shutil.copy(server_path + dir_name + os.path.sep + "allowlist.json", backup_path)
        print_backup("allowlist.json")

    if os.path.exists(server_path + dir_name + os.path.sep + "permissions.json"):
        shutil.copy(server_path + dir_name + os.path.sep + "permissions.json", backup_path)
        print_backup("permissions.json")
        
def restore(server_path, dir_name, backup_path):
    if not os.path.exists(backup_path):
        print("The backup directory does not exist.")
        return

    try:
        if os.path.exists(server_path + dir_name + os.path.sep + "worlds"):
            shutil.rmtree(server_path + dir_name + os.path.sep + "worlds")

        if os.path.exists(backup_path + os.path.sep + "worlds"):
            shutil.copytree(backup_path + os.path.sep + "worlds", server_path + dir_name + os.path.sep + "worlds")
            print_restore("worlds")

        if os.path.exists(server_path + dir_name + os.path.sep + "resource_packs"):
            shutil.rmtree(server_path + dir_name + os.path.sep + "resource_packs")

        if os.path.exists(backup_path + os.path.sep + "resource_packs"):
            shutil.copytree(backup_path + os.path.sep + "resource_packs", server_path + dir_name + os.path.sep + "resource_packs")
            print_restore("resource_packs")

        if os.path.exists(server_path + dir_name + os.path.sep + "behavior_packs"):
            shutil.rmtree(server_path + dir_name + os.path.sep + "behavior_packs")

        if os.path.exists(backup_path + os.path.sep + "behavior_packs"):
            shutil.copytree(backup_path + os.path.sep + "behavior_packs", server_path + dir_name + os.path.sep + "behavior_packs")
            print_restore("behavior_packs")

        if os.path.exists(backup_path + os.path.sep + "server.properties"):
            shutil.copy(backup_path + os.path.sep + "server.properties", server_path + dir_name)
            print_restore("server.properties")

        if os.path.exists(backup_path + os.path.sep + "allowlist.json"):
            shutil.copy(backup_path + os.path.sep + "allowlist.json", server_path + dir_name)
            print_restore("allowlist.json")

        if os.path.exists(backup_path + os.path.sep + "permissions.json"):
            shutil.copy(backup_path + os.path.sep + "permissions.json", server_path + dir_name)
            print_restore("permissions.json")           

    except Exception as e:
        print(f"An error occurred: {e}")
