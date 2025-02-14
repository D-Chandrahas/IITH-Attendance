import os
import sys
from requests import Session

BASE_URL = "https://erp.iith.ac.in/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"

BODY = {
    "UserID": "",
    "DeviceType": "android",
    "FCMID" : "9uTC82PwTddsX7-l9My0M9:gQphngqrimY8RNWS3IPzZF4w9g-OU4FNwDpWPNmCQcF0sodLFZyuhU5JOI36faxcOT5f6roRi6oVHgVrprfht5kEMW6ei7LdeuPVlZ4wWHclEZhT2LTjh27ZDut8AcNB01kuz3vEdnpC,OS:33,Model:SM-M325F,BRAND:samsung,MANUFACTURER:samsung,Build ID:TP1A.220624.014",
    "Password": ""
}

req = Session()

def login_req():

    try:
        res = req.post(BASE_URL + LOGIN_PATH, json=BODY)
    except Exception as e:
        return False, f"{e}, Probably a server-side error, IDK tho"
    
    if res.status_code == 200:
        data = res.json()[0]
        if data["errorId"] == 0:
            return True, (data["referenceId"], data["studentName"])
        else:
            return False, data["errorMessage"]
    else:
        return False, f"Http Status {res.status_code}, {res.text}"


def print_help():
    print("\nUsage: (do not include brackets)\n    python config_gen.py [-h | --help]; Display this help page", file=sys.stderr)
    print("    python config_gen.py [rollno1,password1] [rollno2,password2] ...", file=sys.stderr)
    print("    python config_gen.py [file_path]\n\n", file=sys.stderr)
    print("Input file format:\nrollno1,password1\nrollno2,password2\n...\n", file=sys.stderr)
    print("Output format:\nWebID1,Name1,rollno1,password1\nWebID2,Name2,rollno2,password2\n...\n", file=sys.stderr)
    
    
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:

        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            exit(0)
        
        elif os.path.exists(sys.argv[1]):
            with open(sys.argv[1], "r") as f:
                user_creds = f.read().splitlines()

        else:
            user_creds = sys.argv[1:]
            if argc == 2:
                print(f"Error: No file found with path {sys.argv[1]}, treating it as rollno.,password", file=sys.stderr)

        for user_cred in user_creds:

            BODY["UserID"], BODY["Password"] = map(str.strip, user_cred.split(","))

            success, data = login_req()
            
            if (success):
                print(data[0], data[1], BODY["UserID"], BODY["Password"], sep=",")

            else:
                print("Error:", data, BODY["UserID"], BODY["Password"], file=sys.stderr)
    else:
        print_help()
