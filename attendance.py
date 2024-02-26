import os
from random import choices
import requests as req
import json
import string


# BASE_URL = "https://erp.iith.ac.in/MobileAPI/"
BASE_URL = "http://127.0.0.1:5000/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"
TIMETABLE_PATH = "GetStudentTimeTableForAttendance"
MARK_ATTENDANCE_PATH = "UpSertStudentAttendanceDetails"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

CONFIG = {}

temp = ''.join(choices(string.ascii_letters + string.digits, k=160))
FAKE_FCMID = f"{temp[:14]}-{temp[14:21]}:{temp[21:47]}-{temp[47:160]}" + ",OS:33,Model:SM-M325F,BRAND:microsoft,MANUFACTURER:microsoft,Build ID:RSR1.210722.013"

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
        return False, f"{e}\nProbably a server-side error, IDK tho\n"
    
    if res.status_code == 200:
        data = res.json()[0]
        if data["errorId"] == 0:
            return True, data["referenceId"]
        else:
            return False, data["errorMessage"] + "\n"
    else:
        return False, f"Http Status {res.status_code}\n{res.text}"


def login_page():
    cls()

    userid = input("\nEnter User ID: ")
    
    password = input("\nEnter Password: ")

    print("\nLogging in...\n")
    
    success, data = login_req(userid, password)

    if success:
        modify_config("WebIdentifier", data)
    else:
        print("Error:", data)
        input("Enter to retry (or) Ctrl+C to exit")


def logout():
    modify_config("WebIdentifier", None)


def timetable_req():
    body = { "WebIdentifier": CONFIG["WebIdentifier"] }

    try:
        res = req.post(BASE_URL + TIMETABLE_PATH, json=body)
    except Exception as e:
        return False, f"{e}\nProbably a server-side error, IDK\n"
    
    if res.status_code == 200:
        return True, res.json()["table"]
    else:
        return False, f"Http Status {res.status_code}\n{res.text}"


def print_timetable(timetable):
    if len(timetable) == 0:
        print("No classes today!")
        return
    else:
        idx = 1
        for course in timetable:
            print(f"{idx})",
                    course["courseCode"],
                    course["courseName"],
                    course["timePeriod"],
                    course["classGroup"],
                    course["attendanceMarked"],
                    sep=", ")
            idx += 1


def get_not_marked_courses(timetable):
    not_marked = []
    idx = 1
    for course in timetable:
        if not course["attendanceMarked"]:
            not_marked.append(idx)
        idx += 1
    return not_marked


def mark_attendance(timeTableId):
    body = {
        "Webidentifier": CONFIG["WebIdentifier"],
        "TimeTableId": timeTableId
    }

    try:
        res = req.post(BASE_URL + MARK_ATTENDANCE_PATH, json=body)
    except Exception as e:
        return False, f"{e}\nProbably a server-side error, IDK\n"
    
    if res.status_code == 200:
        data = res.json()["table"][0]
        if data["errorid"] == 0:
            return True, None
        else:
            return False, data["errormessage"] + "\n"
    else:
        return False, f"Http Status {res.status_code}\n{res.text}"



def home_page():
    while True:
        cls()
        print("Fetching timetable...")
        success1, data = timetable_req()

        if not success1:
            cls()
            print("\nCtrl+C: Exit\n0)Lougout\n")
            print("\nUnable to fetch timetable.", "\n\nError:", data)
            opt = input("Choose from above options (or) Enter to retry: ")
            if opt == "0":
                logout()
                return
        else:
            while True:
                cls()
                print("\nCtrl+C: Exit\n0)Lougout\n")
                print_timetable(data)
                not_marked = get_not_marked_courses(data)
                opt = input("\nChoose from above options (or) Enter to refresh: ")
                if opt == "":
                    break
                elif opt == "0":
                    logout()
                    return
                else:
                    try:
                        opt = int(opt)
                    except Exception:
                        input("\nInvalid option. Press Enter to retry")
                        continue

                    if opt not in not_marked:
                        input("\nInvalid option. Press Enter to retry")
                        continue
                    else:
                        print("\nMarking attendance...\n")
                        success2, err_msg = mark_attendance(data[opt-1]["timeTableId"])
                        if success2:
                            input(f"Attendance marked for {data[opt-1]['courseCode']}. Enter to continue")
                            break
                        else:
                            input(f"Error: {err_msg}\nEnter to retry")
                            break
    
    
        
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



