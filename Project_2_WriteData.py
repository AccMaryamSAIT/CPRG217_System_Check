"""
Name: Project_2_WriteData
Authors: Roman Kapitoulski, Eric Russon, Maryam Bunama
Version: 1.0
Date: June 5, 2023
Description:
"""
import os
import socket  # Use socket module to get machine name


class Service:
    def __init__(self, name="", status=""):
        self._name = name
        self._status = status

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setStatus(self, status):
        self._status = status

    def getStatus(self):
        return self._status


class Cpu:
    def __init__(self, vendorID="", model="", modelName="", cache=""):
        self._vendorID = vendorID
        self._model = model
        self._modelName = modelName
        self._cache = cache

    def setVendorID(self, vendorID):
        self._vendorID = vendorID

    def getVendorID(self):
        return self._vendorID

    def setModel(self, model):
        self._model = model

    def getModel(self):
        return self._model

    def setModelName(self, modelName):
        self._modelName = modelName

    def getModelName(self):
        return self._modelName

    def setCache(self, cache):
        self._cache = cache

    def getCache(self):
        return self._cache


class User:
    def __init__(self, name=""):
        self._name = name
        self._groups = []

    def getName(self):
        return self._name

    def addGroup(self, group):  # Pass a list of groups to the function to set the user's group
        self._groups.append(group)

    def getGroups(self):
        # Return a copied list so a user is unable to modify the list of users outside of class methods
        copiedList = self._groups[:]
        return copiedList

    def __str__(self):
        return self._name


class Machine:
    def __init__(self, name="", cpu=Cpu()):
        self._name = name
        self._users = []
        self._cpu = cpu
        self._services = []

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def addUser(self, user):
        self._users.append(user)

    def getUsers(self):
        # Return a copied list so a user is unable to modify the list of users outside of class methods
        copiedList = self._users[:]
        return copiedList

    def setCpu(self, cpu):
        self._cpu = cpu

    def getCpu(self):
        return self._cpu

    def addService(self, service):
        self._services.append(service)

    def getServices(self):
        return self._services


### Retrieve machine name
# Create a machine object
# Use the socket.gethostname() function to retrieve the machine name and use it as a constructor argument
machine = Machine(socket.gethostname())

### Retrieve list of users
# File path containing list of users
passwdFile = "/etc/passwd"

try:
    # Open the passwdFile and retrieve the usernames
    with open(passwdFile, 'rt') as file:
        for line in file:
            # Remove any whitespace
            line = line.strip()
            # Get the username by splitting the line into parts separated by the ":" character.
            username = line.split(":")[0]
            # Create a user object and add it to the machine's list of users
            machine.addUser(User(username))

# If file not found return an error
except FileNotFoundError:
    print("Error file: " + passwdFile + " not found")

### Retrieve a list of groups for each user
for user in machine.getUsers():
    # Use os.popen to execute a command on the user's terminal.
    # Use the "groups user" command to retrieve the groups the user is part of
    output = os.popen(f"groups {user.getName()}").read()

    # Remove any whitespaces from output
    output = output.strip()

    # Split the output and obtain two items: 1. username 2. groups
    username, groups = output.split(":")

    # Split the groups string into a list of groups
    groups = groups.split()

    # Add the groups to the user object
    for group in groups:
        user.addGroup(group)

### Get CPU info
# File path that contains CPU information
cpuInfoFile = "/proc/cpuinfo"

try:
    with open(cpuInfoFile, "rt") as file:
        for line in file:
            # Remove any whitespace
            line = line.strip()

            try:
                # Map the lines of the file to key/value pairs by splitting the line at the ":"
                key, value = line.split(":")

                # Remove any extra white spacing
                key = key.strip()
                value = value.strip()

                # Check only for first processor
                if key == "processor":
                    # value of processor indicates which CPU. 0 is first CPU
                    # convert the value into an integer and compare to 0
                    if int(value) > 0:
                        break

                # Check if key corresponds to required CPU information.
                # Vendor ID
                if key == "vendor_id":
                    # Set the machine's CPU's vendorID attribute to the value
                    machine.getCpu().setVendorID(value)

                # Model
                if key == "model":
                    # Set the machine's CPU's model attribute to the value
                    machine.getCpu().setModel(value)

                # Model Name
                if key == "model name":
                    # Set the machine's CPU's modelName attribute to the value
                    machine.getCpu().setModelName(value)

                # Cache
                if key == "cache size":
                    # Set the machine's CPU's cache attribute to the value
                    machine.getCpu().setCache(value)

            # If line cannot be split into a key/value pair skip it and continue
            except ValueError:
                break

# If file not found return an error
except FileNotFoundError:
    print("Error file: " + passwdFile + " not found")

### Get a list of all running services
# Read the systemctl output
services = os.popen("systemctl list-units --type=service").read()

# Create a list of strings that each contain a line of the output
services = services.split("\n")

# Iterate through each line of output and retrieve service name and status
iteration = 0
for line in services:
    # Remove any extra white space
    line = line.strip()

    # Skip the first line
    if iteration == 0:
        iteration += 1
        continue

    # If a line doesn't contain characters it means it's reached an empty line
    # In this case that's the end of the services so exit the loop
    if len(line) < 1:
        break

    # Split each line into a list of values
    # Retrieve the service name
    name = line.split()[0]
    # Retrieve the service status
    status = line.split()[3]

    # Check if service is running, if so add it to the list of running services
    if status == "running":
        machine.addService(Service(name, status))

for service in machine.getServices():
    print(service.getName(), service.getStatus())
