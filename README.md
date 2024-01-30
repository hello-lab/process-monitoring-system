# process-monitoring-system
pings the server if any slave(computer to be monitored) is using any apps not in the whitelist

### Requisite:

 - python
- atleast 2 pcs 
	- one acts as server-pc
	- the others are the pc to be monitored will be referred as "**slave computers**" from now on
 - all pcs in the LAN or use tunelling(ngrok) or use virtual LAN(hamachi)
# server
put the file(s) in the server files in the server pc

    pip install Flask
    python server.py

# slave computers
put the monitored-pc files in the the slave computers 

     python config.py
     python main.py
config .py auto configs whitelist (all the programs which are allowed to run
