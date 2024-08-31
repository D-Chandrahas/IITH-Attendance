import os
import sys
from requests import Session
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler

BASE_URL = "https://erp.iith.ac.in/MobileAPI/"


TIMETABLE_PATH = "GetStudentTimeTableForAttendance"
MARK_ATTENDANCE_PATH = "UpSertStudentAttendanceDetails"


if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]
else:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return f.read().splitlines()
    else:
        return None


def timetable_req(webIdentifier):
    body = { "WebIdentifier": webIdentifier }

    try:
        res = req.post(BASE_URL + TIMETABLE_PATH, json=body)
    except Exception as e:
        return False, f"{e}\nProbably a server-side error, IDK\n"
    
    if res.status_code == 200:
        return True, res.json()["table"]
    else:
        return False, f"Http Status {res.status_code}\n{res.text}"


def mark_attendance_req(webIdentifier, timeTableId):
    body = {
        "Webidentifier": webIdentifier,
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


def check_and_mark(webIdentifier, name):
    success1, data = timetable_req(webIdentifier)

    if not success1:
        print("\nUnable to fetch timetable.", "\n\nError:", data)
    else:
        for course in data:
            if course["classGroup"] == "Ongoing" and not course["attendanceMarked"]:
                success2, err_msg = mark_attendance_req(webIdentifier, course["timeTableId"])
                if success2:
                    print(f"Attendance marked for {name} for {course['courseCode']}.")
                else:
                    print(f"Error: {err_msg}\n")
                break
        else: # no break
            print(f"No attendance to mark for {name}.")

        
def main():
    global req
    req = Session()
    
    print(datetime.now())

    if config := load_config():
        print(f"Config loaded, found {len(config)} entries.\n")
        for entry in config:
            check_and_mark( *map(str.strip, entry.split(",")[:2]) )
    else:
        print(f"No config found at {os.path.abspath(CONFIG_PATH)}")

    print(f"\n{'-'*50}\n")


def start_scheduler():
    scheduler = Scheduler()
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour= 9, minute=40, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=10, minute=40, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=11, minute=40, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=12, minute=40, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=15, minute=40, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=17, minute=10, misfire_grace_time = 120)
    scheduler.add_job(main, "cron", day_of_week="mon-fri", hour=18, minute=40, misfire_grace_time = 120)
    print(datetime.now(), "Scheduler started", f"Config path: {os.path.abspath(CONFIG_PATH)}", "=" * 50, "\n", sep="\n")
    scheduler.start()
    

if __name__ == "__main__":
    try:
        start_scheduler()
    except Exception as e:
        print("\nError: ", e)
        exit(1)

