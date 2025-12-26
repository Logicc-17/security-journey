import json
import subprocess
import json
from datetime import datetime

#time comparisons
def timeCheck():
    now = datetime.now()
        
    for item in data["output"]:
            # Convert stored time string to datetime
            stored_time = datetime.strptime(item["time"], "%H:%M:%S")
            
            # Calculate difference (simplified)
            diff = now - stored_time
            diff_minutes = diff.total_seconds() / 60
            
            
            if diff_minutes > 60:  # 60 minutes
                print(f"Long session: {item['pId']} for {diff_minutes:.0f}min")
        

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

with open('second-snapshot.json', 'w') as json_file:
    json.dump(output, json_file,indent=4)  
with open("output.json", "r") as f:
    data = json.load(f)
with open("second-snapshot.json", "r") as f:
    newData = json.load(f)


timeCheck()