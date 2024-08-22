import json
import os
import string
import sys
from random import choices
from requests import Session

BASE_URL = "https://erp.iith.ac.in/MobileAPI/"
# BASE_URL = "http://127.0.0.1:5000/MobileAPI/"

LOGIN_PATH = "GetMobileAppValidatePassword"
TIMETABLE_PATH = "GetStudentTimeTableForAttendance"
MARK_ATTENDANCE_PATH = "UpSertStudentAttendanceDetails"

req = Session()

if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]
else:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


CONFIG = {}


CLSCR_SYSCALL = "cls" if os.name=="nt" else "clear"
def cls():
    os.system(CLSCR_SYSCALL)


def modify_config(key, value):
    global CONFIG
    CONFIG[key] = value

def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(CONFIG, f)


def load_config():
    global CONFIG
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)
    else:
        modify_config("WebIdentifier", None)
        modify_config("Name", None)
        temp = ''.join(choices(string.ascii_letters + string.digits, k=160))
        fake_fcmid = f"{temp[:14]}-{temp[14:21]}:{temp[21:47]}-{temp[47:160]}" + ",OS:33,Model:SM-M325F,BRAND:samsung,MANUFACTURER:samsung,Build ID:TP1A.220624.014"
        modify_config("FCMID", fake_fcmid)
        save_config()


def login_req(userid, password):
    body = {
        "UserID": userid,
        "DeviceType": "android",
        "FCMID" : CONFIG["FCMID"],
        "Password": password
    }

    try:
        res = req.post(BASE_URL + LOGIN_PATH, json=body)
    except Exception as e:
        return False, f"{e}\nProbably a server-side error, IDK tho\n"
    
    if res.status_code == 200:
        data = res.json()[0]
        if data["errorId"] == 0:
            return True, data["referenceId"], data["studentName"]
        else:
            return False, data["errorMessage"] + "\n", None
    else:
        return False, f"Http Status {res.status_code}\n{res.text}", None


def login_page():
    cls()

    userid = input("\nEnter User ID: ")
    
    password = input("\nEnter Password: ")

    print("\nLogging in...\n")
    
    success, data, name = login_req(userid, password)

    if success:
        modify_config("WebIdentifier", data)
        modify_config("Name", name)
        save_config()
    else:
        print("Error:", data)
        input("Enter to retry (or) Ctrl+C to exit")


def logout():
    modify_config("WebIdentifier", None)
    modify_config("Name", None)
    save_config()


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
    idx = 1
    print("_"*97)
    print(f'| S.No | Course Code | {"Course Name":^30} | Time Period | Class Status | Attendance |')
    print(f'|{"-"*6}|{"-"*13}|{"-"*32}|{"-"*13}|{"-"*14}|{"-"*12}|')
    for course in timetable:
        print(f'| {str(idx)+".":^4} | {course["courseCode"]:^11} | {course["courseName"][:30]:^30} | {course["timePeriod"]} | {course["classGroup"]:^12} | {course["attendanceMarked"]!s:^10} |')
        idx += 1
    print(f'|{"_"*6}|{"_"*13}|{"_"*32}|{"_"*13}|{"_"*14}|{"_"*12}|')


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
            print(f"\nWelcome, {CONFIG['Name']}\n")
            print("\nCtrl+C: Exit\n     0: Logout\n")
            print("\nUnable to fetch timetable.", "\n\nError:", data)
            opt = input("Choose from above options (or) Enter to retry: ")
            if opt == "0":
                logout()
                return
        else:
            data = sorted(data, key=lambda x: int(x["timePeriod"][:2]))
            not_marked = get_not_marked_courses(data)
            while True:
                cls()
                print(f"\nWelcome, {CONFIG['Name']}\n")
                print("\nCtrl+C: Exit\n     0: Logout\n")
                print_timetable(data)
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
    except Exception as e:
        cls()
        print("\nError: ", e)
        print("\nTry deleting config file.\nNote: This program was only tested on Python 3.10")
        exit(1)

