'''
Name: Project_2_PrintData
Authors: Roman Kapitoulski, Eric Russon, Maryam Bunama
Version: 1.2
Date: June 9, 2023
Description: This code takes the JSON file created by "Project_2_WriteData.py" and 
formats its information into organized table. This information gets outputted to the 
command line/terminal. Additionally, this script can function independantly from operating
systems as long as the JSON file contains the correct information. 
'''

import json
from tabulate import tabulate # Module that allows creating and formatting tables

# Opening and loading JSON file
with open("Project_2.json", 'rt') as f:
    info = json.load(f)

## Preparing information for tabulate

# Formatted text for the CPU info.
cpu_info = f"Vendor_ID: {info['cpu']['vendorID']}\nModel name: {info['cpu']['mname']}\nModel: {info['cpu']['model']}\nCache: {info['cpu']['cache']}"

# Created list for tabular containing the machine name and formatted CPU info. 
machine_list = [[info['machine'], cpu_info]]

# Created list for tabular using a for loop that contains user and group info. 
users_info = []
for user in info['users']:
    user_info = []
    groups_info = ', '.join(user['groups'])
    user_info.append(f"{user['uname']}")
    user_info.append(groups_info)
    users_info.append(user_info)

# Created list for tabular using a for loop that contains service names and statuses.
services_info = []
for service in info['services']:
    service_info = []
    service_info.append(f"{service['sname']}")
    service_info.append(f"{service['status']}")
    services_info.append(service_info)


## Tabulate outputting 

# Created multiple Tabulate tables for each of the lists created earlier
# and formatted them with appropriate headers and table styles.
print(tabulate(machine_list, headers=["Machine", "Cpu"], tablefmt='fancy_grid'))
print(tabulate(users_info, headers=["Users", "Groups"], tablefmt='fancy_grid'))
print(tabulate(services_info, headers=["Service Name", "Status"], tablefmt='fancy_grid'))
