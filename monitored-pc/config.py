import subprocess

# PowerShell command to get processes with a MainWindowTitle and select Description
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description"'

# List to store the obtained process descriptions
listt = []

# Execute the PowerShell command
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

# Iterate through the output lines and add non-empty lines to the list
for line in proc.stdout:
    if line.rstrip():
        # Decode the binary string and remove trailing whitespace
        x = line.decode().rstrip()
        listt += [x]

# Print the list of process descriptions
print(listt)

# Encoding
sttr = str(listt)
nstr = ""
for i in range(0, len(sttr)):
    b = i + 1
    a = ord(sttr[i]) + (b * b)
    # print(sttr[i],chr(a))
    nstr += chr(a)
# print((nstr),len(sttr))

# Write the encoded result to the "config.txt" file
f = open("config.txt", "w", encoding="utf-8")
f.write(str(nstr))
f.close()
