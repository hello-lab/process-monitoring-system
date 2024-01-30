import subprocess
import requests
import time

# PowerShell command to get the description of running processes
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'

# Get computer name and server IP from user input
cid = input("name of computer: ")
ip = input("IP of server: ")

# Read the encoded whitelist from the configuration file
f = open("config.txt", "r", encoding="utf-8")
strr = f.read()
nstr = ""

# Decode the whitelist
for i in range(0, len(strr)):
    b = i + 1
    a = ord(strr[i]) - (b * b)
    b = chr(a)
    nstr += b

f.close()

# Convert the decoded whitelist string to a Python list
whitelist = eval(nstr)

# Infinite loop to continuously monitor and send data
while True:
    # Run the PowerShell command to get the list of opened applications
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    # Iterate over the output of the command
    for line in proc.stdout:
        if line.rstrip():
            # Decode the binary string and remove trailing characters
            x = line.decode().rstrip()

            # Check if the opened application is in the whitelist
            if x in whitelist:
                continue
            else:
                # If not in whitelist, send the information to the server
                dictToSend = {'APPS-OPENNED': x, 'Computer Name': cid}
                res = requests.post(ip + "/login/", json=dictToSend)
                print('response from server:', res.text)

                # Check if the request was successful
                if res:
                    dictFromServer = res.json()

                # Make a GET request to trigger some action on the server (URL might need adjustment)
                requests.get('http://127.0.0.1:8080/')

    # Wait for 5 seconds before repeating the process
    time.sleep(5)
