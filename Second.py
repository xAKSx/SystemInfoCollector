import json

def print_data():
    try:
        with open('Project_2.json', 'r') as json_file:
            data = json.load(json_file)
        
        print("Machine Name:", data.get("machine_name", "N/A"))
        
        print("\nUsers and Groups:")
        users_and_groups = data.get("users_and_groups", [])
        for user_info in users_and_groups:
            print(f"{user_info['username']}: {user_info['group']}")
        
        print("\nProcessor Info:")
        processor_info = data.get("processor_info", {})
        for key, value in processor_info.items():
            print(f"{key}: {value}")
        
        print("\nServices Status:")
        services_status = data.get("services_status", [])
        for status in services_status:
            print(status)

    except FileNotFoundError:
        print("Project_2.json not found. Run Project_2_WriteData.py first.")

if __name__ == "__main__":
    print_data()
