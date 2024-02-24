import os
import requests as req
import json


BASE_URL = "https://erp.iith.ac.in/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

CONFIG = {}

FAKE_FCMID = "WQaNTlvZNsk22L-3LmDu7Y:W4cKL23YQsnIkyfgk4QQ5uGotc-U6K40QO6ydXeou8eGLHtj3VZRJ2ixbJSYcqbN59vnz7TvVVpYfa5i95o0X2aa8kxv0lQ1RyBkpsqmz9YNWRpNh3fJ5u0t7ZtuX4Mm9FKdQGdt2V2W,OS:33,Model:SM-M325F,BRAND:samsung,MANUFACTURER:samsung,Build ID:RSR1.210722.013"


def cls():
    os.system("cls" if os.name=="nt" else "clear")


def load_config():
    global CONFIG
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)
    else:
        CONFIG["WebIdentifier"] = None
        with open(CONFIG_PATH, "w") as f:
            json.dump(CONFIG, f)

def modify_config(key, value):
    global CONFIG
    CONFIG[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(CONFIG, f)


def login_req(userid, password):
    body = {
        "UserID": userid,
        "DeviceType": "android",
        "FCMID" : FAKE_FCMID,
        "Password": password
    }

    try:
        res = req.post(BASE_URL + LOGIN_PATH, json=body)
    except Exception as e:
        return False, None, f"Error: {e}\nProbably a server-side error, IDK tho"
    
    data = res.json()[0]
    if res.status_code == 200:
        if data["errorId"] == 0:
            success = True
            webid = data["referenceId"]
            error_msg = None
        else:
            success = False
            webid = None
            error_msg = data["errorMessage"]
    else:
        success = False
        webid = None
        error_msg = f"Http Status {res.status_code}\n{res.text}"

    return success, webid, error_msg


def login_page():
    cls()

    userid = input("\nEnter User ID: ")
    
    password = input("\nEnter Password: ")
    
    success, webid, error_msg = login_req(userid, password)

    if success:
        modify_config("WebIdentifier", webid)
    else:
        print(f"\nError: {error_msg}")
        input("\nPress Enter to retry (or) Ctrl+C to exit")


def logout():
    modify_config("WebIdentifier", None)


def home_page(): # todo implement
    cls()
    print("Home Page")
    input("\nPress Enter to logout (or) Ctrl+C to exit")
    logout()
    
    
        
def main():
    cls()
    load_config()
    while True:
        while CONFIG["WebIdentifier"] is None:
            login_page()
        home_page()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        exit(0)



