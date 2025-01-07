import os
import sys
from time import sleep
from requests import Session
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler

BASE_URL = "https://erp.iith.ac.in/MobileAPI/"

TIMETABLE_PATH = "GetStudentTimeTableForAttendance"
MARK_ATTENDANCE_PATH = "UpSertStudentAttendanceDetails"

# (hour, minute)
JOBS = ((9, 10),
        (10, 10),
        (11, 10),
        (12, 10),
        (14, 40),
        (16, 10),
        (17, 40))


TIMETABLE_MAX_TRIES = 3; TIMETABLE_RETRY_DELAY = 10 # seconds
MARK_ATTEN_MAX_TRIES = 3; MARK_ATTEN_RETRY_DELAY = 10 # seconds
ATTEN_ERR_MAX_TRIES = 3; ATTEN_ERR_RETRY_DELAY = 60 # seconds
RETRY_JOB_MAX_RUNS = 3; RETRY_JOB_INTERVAL = 10 # minutes


if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]
else:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")


class AttendanceError(Exception):
    pass


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return f.read().splitlines()
    else:
        return None


def timetable_req(webIdentifier):
    body = { "WebIdentifier": webIdentifier }

    for i in range(TIMETABLE_MAX_TRIES):
        try:
            res = req.post(BASE_URL + TIMETABLE_PATH, json=body)
        except Exception as e:
            if i == TIMETABLE_MAX_TRIES - 1:
                return False, f"{e}\nProbably a server-side error, IDK\n"
            else:
                sleep(TIMETABLE_RETRY_DELAY)
        else:
            break
    
    if res.status_code == 200:
        return True, res.json()["table"]
    else:
        return False, f"Http Status {res.status_code}\n{res.text}"


def mark_attendance_req(webIdentifier, timeTableId):
    body = {
        "Webidentifier": webIdentifier,
        "TimeTableId": timeTableId
    }

    for i in range(MARK_ATTEN_MAX_TRIES):
        try:
            res = req.post(BASE_URL + MARK_ATTENDANCE_PATH, json=body)
        except Exception as e:
            if i == MARK_ATTEN_MAX_TRIES - 1:
                return False, f"{e}\nProbably a server-side error, IDK\n"
            else:
                sleep(MARK_ATTEN_RETRY_DELAY)
        else:
            break
    
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
        print("\nUnable to fetch timetable for", name, "\nError:", data)
        raise AttendanceError
    else:
        for course in data:
            if course["classGroup"] == "Ongoing":
                if not course["attendanceMarked"]:
                    success2, err_msg = mark_attendance_req(webIdentifier, course["timeTableId"])
                    if success2:
                        print(f"Attendance marked for {name} for {course['courseCode']}.")
                    else:
                        print("Unable to mark attendance for", name, "\nError:", err_msg)
                        raise AttendanceError
                else:
                    print(f"Attendance already marked for {name} for {course['courseCode']}.")
                break
        else: # no break
            print(f"No attendance to mark for {name}.")


RETRY_COUNT = None

def main():
    global req, RETRY_COUNT
    req = Session()
    
    print(datetime.now())

    if config := load_config():
        print(f"Config loaded, found {len(config)} entries.\n")
        for entry in config:
            for i in range(ATTEN_ERR_MAX_TRIES):
                try:
                    check_and_mark( *map(str.strip, entry.split(",")[:2]) )
                except AttendanceError:
                    if i == ATTEN_ERR_MAX_TRIES - 1:
                        
                        print("\n\nTerminating current run.", end=" ")

                        if RETRY_COUNT is None:
                            SCHEDULER.add_job(main, "interval", minutes=RETRY_JOB_INTERVAL, misfire_grace_time = 60, id="retry")
                            RETRY_COUNT = 0
                            print("Retrying in 10 minutes.")
                        elif (RETRY_COUNT := RETRY_COUNT + 1) >= RETRY_JOB_MAX_RUNS:
                            SCHEDULER.remove_job("retry")
                            RETRY_COUNT = None
                            print("Max retries reached.")
                        else:
                            print("Retrying in 10 minutes.")

                        print(f"{'-'*50}\n")
                        return
                    
                    else:
                        sleep(ATTEN_ERR_RETRY_DELAY)
                else:
                    if RETRY_COUNT is not None:
                        SCHEDULER.remove_job("retry")
                        RETRY_COUNT = None
                    break
    else:
        print(f"No config found at {os.path.abspath(CONFIG_PATH)}")

    print(f"\n{'-'*50}\n")


def start_scheduler():
    global SCHEDULER
    SCHEDULER = Scheduler()
    for job in JOBS:
        SCHEDULER.add_job(main, "cron", day_of_week="mon-fri", hour=job[0], minute=job[1], misfire_grace_time = 120)
    print(datetime.now(), "Scheduler started", f"Config path: {os.path.abspath(CONFIG_PATH)}", "=" * 50, "\n", sep="\n")
    SCHEDULER.start()
    

if __name__ == "__main__":
    try:
        start_scheduler()
    except Exception as e:
        print("\nError: ", e)
        exit(1)

