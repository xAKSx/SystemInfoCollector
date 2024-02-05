import json
import platform
import subprocess
import pwd

# Function to get the machine name using the platform module
def get_machine_name():
    return platform.node()

# Function to get information about users and groups
def get_users_and_groups():
    users = []
    if platform.system() == 'Linux':
        try:
            # Use the pwd module to fetch user information on Linux
            for entry in pwd.getpwall():
                user_info = {
                    "username": entry.pw_name,
                    "group": entry.pw_gid
                }
                users.append(user_info)
        except Exception as e:
            users = [{"error": f"Error fetching user info: {str(e)}"}]
    elif platform.system() == 'Windows':
        try:
            # Use 'net user' command on Windows to fetch user information
            result = subprocess.check_output(['net', 'user']).decode().split('\n')
            for line in result:
                if 'User name' in line:
                    username = line.split()[-1]
                    user_info = {"username": username, "group": "N/A"}
                    users.append(user_info)
        except subprocess.CalledProcessError:
            users = [{"error": "Error fetching user info"}]

    return sorted(users, key=lambda x: x.get("username", ""))

# Function to get information about the processor
def get_processor_info():
    processor_info = {}
    try:
        if platform.system() == 'Linux':
            # Use 'cat /proc/cpuinfo' command on Linux to get processor info
            result = subprocess.check_output(['cat', '/proc/cpuinfo']).decode().split('\n')
            for line in result:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    processor_info[key] = value
        elif platform.system() == 'Windows':
            # Use 'systeminfo' command on Windows to get processor info
            result = subprocess.check_output(['systeminfo']).decode().split('\n')
            for line in result:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    processor_info[key] = value
    except subprocess.CalledProcessError:
        processor_info["error"] = "Error fetching processor info"
    return processor_info

# Function to get the status of services
def get_services_status():
    try:
        if platform.system() == 'Linux':
            # Use 'service --status-all' command on Linux to get services status
            services_status = subprocess.check_output(['service', '--status-all']).decode().strip()
        elif platform.system() == 'Windows':
            # Use 'sc query type= service state= all' command on Windows to get services status
            services_status = subprocess.check_output(['sc', 'query', 'type=', 'service', 'state=', 'all']).decode().strip()
        return services_status.split('\n')
    except subprocess.CalledProcessError as e:
        return ["Error fetching services status", str(e)]

# Function to write the collected data to a JSON file
def write_to_json():
    data = {
        "machine_name": get_machine_name(),
        "users_and_groups": get_users_and_groups(),
        "processor_info": get_processor_info(),
        "services_status": get_services_status()
    }

    with open('Project_2.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Entry point of the script
if __name__ == "__main__":
    write_to_json()
