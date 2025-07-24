import time #this is separate from datetime and only used to add a small delay
import platform
import socket
import uuid, re
import datetime
import speedtest
import pandas as pd
import os

# define functions for all of the requests (most of these are pretty self-explanatory)

def get_computer_name():
    return socket.gethostname()

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def get_mac_address():
    # uses the hex() function to convert uuid.getnode() to hexidecimal format 
    # [2:] and .upper() removes the "0x" prefix from hex() and makes the text uppercase the text in the string
    mac = hex(uuid.getnode())[2:].upper()
    # uses the re (regular expression) module to put ":" every 2 characters
    return ":".join(re.findall("..", mac))

def get_processor_model():
    return platform.processor()

# Gets operating system and version
def get_os():
    return f"{platform.system()} {platform.release()}" # platform.release gets the version

def get_system_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # strftime formats the year, month, date, and hour, minute, second

def get_internet_speed():
    try:
        st = speedtest.Speedtest()
        download_speed_mbps = st.download() / 1_000_000
        upload_speed_mbps = st.upload() / 1_000_000  # Converts to Mbps
        return f"Download speed: {download_speed_mbps:.2f} Mbps, Upload speed: {upload_speed_mbps:.2f} Mbps"
    except:
        return "Couldn't test your internet speed - Check your connection"

def get_active_ports(ip): # This function needs to call get_ip_address() in its parameter to run properly, as it scans the ports on an IP address.
    active_ports = []
    ports_to_scan = [22, 80, 443, 3306, 8080] # These are the five most common ports (22:SSH, 80:HTTPS, 3306:MySQL, 8080:Alternative HTTP)
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.settimeout(1) # The sets the timeout for each port to 1 second so it doesn't wait for a response for too long  
        result = sock.connect_ex((ip, port)) # Tries to connect to the IP and Port. If the connection is successful, it returns 0. If not, it returns an error code
        if result == 0:
            active_ports.append(port) 
        sock.close() # Closes the connection to free up resources
    if active_ports:
        return f"Active ports: {';'.join(map(str, active_ports))}"
    else:
        return "No active ports found"

def update_csv(file_name, computer_data):
    file_exists = os.path.isfile(file_name)
    # Create a dataframe with the computer data
    df = pd.DataFrame([computer_data], columns = ["Computer Name", "IP Address", "MAC Address", "Processor Model", "Operating System", "System Time", "Internet Speed", "Active Ports"]).astype(str) # makes all columns strings
    if file_exists: 
        existing_df = pd.read_csv(file_name) # Checks if the computer name is in the file. If it is, it saves the info into existing.df to prevent adding the same computer info twice
        if df["Computer Name"].iloc[0] in existing_df["Computer Name"].values:
            print(f"Updating record for {df["Computer Name"].iloc[0]}")
            existing_df.update(df) # replace the row where the computer name matches
        else:
            print(f"Adding a new record for {df["Computer Name"].iloc[0]}")
            existing_df = pd.concat([existing_df, df], ignore_index = True)    
        # write the updated DataFrame back to CSV
        existing_df.to_csv(file_name, index = False)
    else:
        # write a new file if it doesn't exist
        df.to_csv(file_name, index = False)

# Creates a main function to run all functions and save the data
def collect_system_info():
    computer_name = get_computer_name()
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    processor_model = get_processor_model()
    operating_system = get_os()
    system_time = get_system_time()
    internet_speed = get_internet_speed()
    active_ports = get_active_ports(ip_address)

    # Collect all the data in a list
    computer_data = [computer_name, ip_address, mac_address, processor_model, operating_system, system_time, internet_speed, active_ports]

    # Write or update the CSV file
    update_csv("Computer_Info.csv", computer_data)

    print(f"Data for {computer_name} collected and saved successfully.")

# Function to display the menu and handle user input
def display_menu():
    choice = input("""
Welcome to the MidTown IT Computer Fingerprint scanner.
Please pick one of the options below to display the corresponding information:
1: Get Computer Name
2: Get IP-address
3: Get MAC-Address
4: Get Processor Model
5: Get Operating System
6: System Time
7: Internet Connection Speed
8: Active Ports
9: Run all functions and put the results into a CSV file
Your choice: """)

    ip_address = get_ip_address()  # Needed for active ports function    

    # Execute functions based on user selection
    if choice == "9":
        collect_system_info()
    elif choice == "1":
        print(f"Computer Name: {get_computer_name()}")
    elif choice == "2":
        print(f"IP Address: {get_ip_address()}")
    elif choice == "3":
        print(f"MAC Address: {get_mac_address()}")
    elif choice == "4":
        print(f"Processor Model: {get_processor_model()}")
    elif choice == "5":
        print(f"Operating System: {get_os()}")
    elif choice == "6":
        print(f"System Time: {get_system_time()}")
    elif choice == "7":
        print("Testing internet speeds...")
        print(get_internet_speed())
    elif choice == "8":
        print(f"{get_active_ports(ip_address)}")
    else:
        print(f"""Invalid choice: "{choice}". Please select a valid option.""")
        time.sleep(2), display_menu()
    go_again = input("Press Y to bring the menu up again or press anything else to quit: ").lower()
    if go_again == "y":
        display_menu()
display_menu()

