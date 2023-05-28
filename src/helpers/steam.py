import requests
import json
from pathlib import Path
from alive_progress import alive_it


def get_steam_package_data(packages: list, refresh_data=True):
    """ connects to steam packagedetails api and downloads data

    Arguments:
        packages(list): list of packageids to collect data for

    Returns:
        list(dict): a list of dictionaries of all the data collected
    """
    data_path = Path(__file__).parent.parent.joinpath('data')
    base_url = "https://store.steampowered.com/api/packagedetails/"

    data = []

    if refresh_data:
        
        for package_id in alive_it(packages, title="Getting data"):

            response = requests.get(base_url, params={"packageids": package_id})
            json_response = json.loads(response.text)
            # if we get a response, and the "success" == True
            if json_response and json_response[str(package_id)]["success"]:
                d = json_response[str(package_id)]["data"]
                d["package_id"] = package_id
                data.append(d)
            else:
                data.append({"package_id": package_id})

        # writing to a file in case we want to look at the raw data from latest load
        with open(f"{data_path}/package_data.json", 'w') as f:
            f.write(json.dumps(data, indent=4))

    else:
        with open(f"{data_path}/package_data.json", 'r') as f:
            data = json.load(f)

    return data

