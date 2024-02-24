import os
import requests as req
import json


# BASE_URL = "https://erp.iith.ac.in/MobileAPI/"
BASE_URL = "http://127.0.0.1:5000/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

CONFIG = {}


def cls():
    os.system("cls" if os.name=="nt" else "clear")


def load_config():
    global CONFIG
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)
    else:
        CONFIG["Webidentifier"] = None
        with open(CONFIG_PATH, "w") as f:
            json.dump(CONFIG, f)

def modify_config(key, value):
    global CONFIG
    CONFIG[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(CONFIG, f)


def login_req(userid, password):
    body = { # fixme all keys
        "UserID": userid,
        "Password": password
    }
    # ! headers
    res = req.post(BASE_URL + LOGIN_PATH, json=body) # fixme body text spacing

    if res.status_code == 200:
        success = True
        webid = res.json()["Webidentifier"] # fixme proper json key
        error_msg = None
    else:
        success = False
        webid = None
        error_msg = res.text # fixme proper json key

    return success, webid, error_msg


def login_page():
    cls()

    userid = input("\nEnter User ID: ")
    
    password = input("\nEnter Password: ")
    
    success, webid, error_msg = login_req(userid, password)

    if success:
        modify_config("Webidentifier", webid)
    else:
        print(f"\nError: {error_msg}")
        input("\nPress Enter to retry (or) Ctrl+C to exit")


def logout():
    modify_config("Webidentifier", None)


def home_page(): # todo implement
    cls()
    print("Home Page")
    input("\nPress Enter to logout (or) Ctrl+C to exit")
    logout()
    
    
        
def main():
    cls()
    load_config()
    while True:
        while CONFIG["Webidentifier"] is None:
            login_page()
        home_page()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        exit(0)



