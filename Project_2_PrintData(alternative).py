'''
Name: Project_2_PrintData
Authors: Roman Kapitoulski, Eric Russon, Maryam Bunama
Version: 1.2.1
Date: June 19, 2023
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

# Formatted text for Users info
users_info = ""
for user in info['users']:
    sorted_groups_info = sorted(user['groups'])
    groups_info = ', '.join(sorted_groups_info)
    user_info = f"Name: {user['uname']}\nGroups: {groups_info}\n"
    users_info += user_info

# Formatted text for Services info
services_info = ""
for service in info['services']:
    service_info = f"Service: {service['sname']}\nStatus: {service['status']}\n"
    services_info += service_info

# Added the formatted text to a list for Tabulate
full_list = [[info['machine'], cpu_info, users_info, services_info]]

## Tabulate outputting 

# Created Tabulate table for the list created earlier
# and formatted them with appropriate headers and table styles.
print(tabulate(full_list, headers=["Machine", "Cpu", "Users", "Services"], tablefmt='fancy_grid'))
