import subprocess
import json
from datetime import datetime


response = subprocess.run(
    ["netstat", "-tup"],
    capture_output=True,
    text=True
)

lines = response.stdout.splitlines()
column=lines[1].split()

output=[]

for line in lines[2:]:

    column=line.split()
    now = datetime.now()
    time= now.strftime("%H:%M:%S")
    connections={

        "Protocal":column[0],
        "Local address":column[3],
        "Foreign address":column[4],
        "state":column[5],
        "pId":column[6],
        "time":time

    }
    output.append(connections)
        
output={"output":output}
with open('output.json', 'w') as json_file:
    json.dump(output, json_file,indent=4)  

