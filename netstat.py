import subprocess
import json
import os
from datetime import datetime
import uuid 

def takeSnapshot(folder="sessions"):
    """Takes a netstat snapshot and saves it as JSON. Returns (filepath, data)."""
    
    os.makedirs(folder, exist_ok=True)
    sessionTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output_{sessionTime}.json"
    filepath = os.path.join(folder, filename)

    try:
        response = subprocess.run(
            ["netstat", "-tup"],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        print("netstat command not found. Is it installed?")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

    lines = response.stdout.splitlines()
    if len(lines) < 2:
        print("Not enough output from netstat")
        return None, None

    output = []
    for line in lines[2:]:
        column = line.split()
        if len(column) < 7:
            print(f"Skipping line (only {len(column)} columns): {line[:50]}...")
            continue
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        sessionID = str(uuid.uuid4())
        output.append({
            "sessionID": sessionID,
            "Protocal": column[0],
            "Local address": column[3],
            "Foreign address": column[4],
            "state": column[5],
            "pId": column[6],
            "time": time
        })

    data = {
        
        "timestamp": sessionTime,
        "output": output
    }

    try:
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error: Could not write to file. Details: {e}")
        return None, None

    return filepath, data

if __name__ == "__main__":
    
 takeSnapshot()
