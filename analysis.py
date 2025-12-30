import json
import netstat
import subprocess
from datetime import datetime
import os

folder = "sessions"

# listing all the files in the folder
files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json")]
latest_file = max(files, key=os.path.getmtime) if files else None

previous_data = None
if latest_file:
    with open(latest_file,'r') as f:
        previous_data = json.load(f) 

with open (latest_file,'r') as f:
     data=json.load(f)  


#time comparisons
def timeCheck(data):
    now = datetime.now()
    
    for item in data["output"]:
        if "session_start" not in item:
            item["session_start"] = now.isoformat()
            print(f"New session started: {item.get('pId', 'Unknown')}")
            continue  # Skip time check for newly started sessions

    

        stored_datetime = datetime.fromisoformat(item["session_start"])
        diff = now - stored_datetime
        diff_minutes = diff.total_seconds() / 60
        
        if diff_minutes > 60:  # 60 minutes
            print(f"Long session: {item.get('pId', 'Unknown')} for {diff_minutes:.0f}min")
        else:
            print(f"Session okay: {item.get('pId', 'Unknown')}")

  
def track_process_changes(previous_data, current_data):

    
    stillRunning=[]
    previous_processes = set()
    current_processes = set()
    
    # creating a unique identifier: (PID, Protocol, Local Address, Foreign Addressa)
    for item in previous_data.get("output", []):
        key = (item.get("pId"), 
               item.get("Protocal"),
               item.get("Local address"),
               item.get("Foreign address"))
        previous_processes.add(key)
    
    for item in current_data.get("output", []):
        key = (item.get("pId"), 
               item.get("Protocal"),
               item.get("Local address"),
               item.get("Foreign address"))
        current_processes.add(key)
    
  
    # Finding differences
    ended_processes = previous_processes - current_processes
    started_processes = current_processes - previous_processes
    stillRunning = previous_processes & current_processes 
    return started_processes, ended_processes ,stillRunning

def checkSession(previous_data=None):
    # Take a new snapshot
    file, newdata = netstat.takeSnapshot()
    print("\nSnapshot saved to:", file)
    

    if previous_data:
        started, ended ,running= track_process_changes(previous_data, newdata)
        print("===================================================================")
        print("\nNewly started processes:")
        for proc in started:
            print(proc)
        print("===================================================================")    
        print("\nProcesses that ended:")
        for proc in ended:
            print(proc)
        print("===================================================================")
        print("\nprocesses that are still running:")
        for proc in running:
            print(proc)    
    else:
        print("No previous snapshot to compare.")
    
    return newdata 







checkSession(previous_data)