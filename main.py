import requests
import json
import time
import os

def update_by_id(filename, id: str = ""):
    assert isinstance(id, str)
    endpoint = "https://us-central1-kp24-fd486.cloudfunctions.net/hierarchy2"
    data = json.dumps({
        "data": {
            "id": id
        }
    })

    successful = False
    while not successful:
        retry_seconds = 5
        try:
            res = requests.post(
                endpoint,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "PythonRuntime/3.11.5",
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"
                },
                data=data
            )
            successful = True

        except requests.exceptions.ConnectionError:
            print(f"Request for id={id} not successful! Retrying in {retry_seconds} seconds ....")
            time.sleep(retry_seconds)
            retry_seconds *= 2

    with open(filename, mode="w") as fp:
        print(res.text, file=fp)

    return res.text

def update_for_one_iteration(prov_id: str, kota_id: str):
    total_requests = 0
    start_time = time.time()

    # Top update
    timestamp = int(time.time() // 1)
    root_dir = "private/data"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    filename = f"{root_dir}/{timestamp}.json"
    res_text = update_by_id(filename=filename, id="")
    total_requests += 1

    # Province update
    timestamp = int(time.time() // 1)
    prov_dir = f"{root_dir}/{prov_id}"
    if not os.path.exists(prov_dir):
        os.makedirs(prov_dir)

    filename = f"{prov_dir}/{timestamp}.json"
    res_text = update_by_id(filename=filename, id=prov_id)
    total_requests += 1

    # City/regency update
    timestamp = int(time.time() // 1)
    kota_dir = f"{prov_dir}/{kota_id}"
    if not os.path.exists(kota_dir):
        os.makedirs(kota_dir)

    filename = f"{kota_dir}/{timestamp}.json"
    res_text = update_by_id(filename=filename, id=kota_id)
    kota_res = json.loads(res_text)
    total_requests += 1

    for kec_id in kota_res["result"]["aggregated"].keys():
        timestamp = int(time.time() // 1)
        kec_dir = f"{kota_dir}/{kec_id}"
        if not os.path.exists(kec_dir):
            os.makedirs(kec_dir)

        filename = f"{kec_dir}/{timestamp}.json"

        try:
            res_text = update_by_id(filename=filename, id=kec_id)
            kec_res = json.loads(res_text)
            total_requests += 1
        except:
            raise ValueError(f"Error requesting kec_id={kec_id}")

        for kel_id in kec_res["result"]["aggregated"].keys():
            timestamp = int(time.time() // 1)
            kel_dir = f"{kec_dir}/{kel_id}"
            if not os.path.exists(kel_dir):
                os.makedirs(kel_dir)

            filename = f"{kel_dir}/{timestamp}.json"

            try:
                res_text = update_by_id(filename=filename, id=kel_id)
                total_requests += 1
            except:
                raise ValueError(f"Error requesting kel_id={kel_id}")
            
    return {
        "total_requests": total_requests,
        "duration": time.time() - start_time
    }

with open("config.json") as fp:
    config = json.load(fp)
print("Config:\n", config)

prov_id = str(config["prov_id"])
kota_id = str(config["kota_id"])
INTERVAL_SECONDS = int(config["interval_seconds"])

keyboard_interrupted = False
while not keyboard_interrupted:
    time_to_wait = INTERVAL_SECONDS - (time.time() % INTERVAL_SECONDS)

    try:
        print(f"Wait {time_to_wait} s ....")
        time.sleep(time_to_wait)
    except KeyboardInterrupt:
        print("Keyboard interrupted.")
        keyboard_interrupted = True

    if not keyboard_interrupted:
        print("Requesting ....")
        log = update_for_one_iteration(prov_id, kota_id)
        timestamp = int(time.time() // 1)

        print("Logging ....")
        log_dir = "private/log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(f"{log_dir}/{timestamp}.json", mode="w") as fp:
            json.dump(log, fp)

        print("One iteration done.")

print("Done gracefully~")
