import json
import platform
import subprocess
import os

def get_machine_name():
    return platform.node()

def get_users_and_groups():
    users = []
    if platform.system() == 'Linux':
        for entry in os.scandir('/etc/passwd'):
            user_info = {
                "username": entry.name,
                "group": "N/A"
            }
            users.append(user_info)
    elif platform.system() == 'Windows':
        try:
            result = subprocess.check_output(['net', 'user']).decode().split('\n')
            for line in result:
                if 'User name' in line:
                    username = line.split()[-1]
                    user_info = {"username": username, "group": "N/A"}
                    users.append(user_info)
        except subprocess.CalledProcessError:
            users = [{"error": "Error fetching user info"}]

    return sorted(users, key=lambda x: x.get("username", ""))

def get_processor_info():
    processor_info = {}
    try:
        if platform.system() == 'Linux':
            result = subprocess.check_output(['cat', '/proc/cpuinfo']).decode().split('\n')
            for line in result:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    processor_info[key] = value
        elif platform.system() == 'Windows':
            result = subprocess.check_output(['systeminfo']).decode().split('\n')
            for line in result:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    processor_info[key] = value
    except subprocess.CalledProcessError:
        processor_info["error"] = "Error fetching processor info"
    return processor_info

def get_services_status():
    try:
        if platform.system() == 'Linux':
            # Use 'service' command on Linux
            services_status = subprocess.check_output(['service', '--status-all']).decode().strip()
        elif platform.system() == 'Windows':
            # Use 'sc' command on Windows
            services_status = subprocess.check_output(['sc', 'query', 'type=', 'service', 'state=', 'all']).decode().strip()
        return services_status.split('\n')
    except subprocess.CalledProcessError as e:
        return ["Error fetching services status", str(e)]


def write_to_json():
    data = {
        "machine_name": get_machine_name(),
        "users_and_groups": get_users_and_groups(),
        "processor_info": get_processor_info(),
        "services_status": get_services_status()
    }

    with open('Project_2.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    write_to_json()
