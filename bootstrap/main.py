import requests
import json
import pathlib import Path

data = json.loads(Path("outbox-postgres.json").read_text(ecording="utf-8"))
name = data['name']
config = data['config']


r = requests.get("htpp://connect:8083/connect/{name}/config", timeout = 5)

if r.status_code == 200:
    request.put("htpp://connect:8083/connect/{name}/config"
        json = config, timeout = 30
    ).raise_for_status()
else:
    request.post("htpp://connect:8083/connect/{name}/config"
        json = config, timeout = 30
    ).raise_for_status()