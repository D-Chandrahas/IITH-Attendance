# [auto_attendance.py](./auto_attendance.py)

### This script can be used to automate the process of marking attendance for multiple users.

### Usage:
Requires `requests` & `apscheduler` module. Install with `pip install requests apscheduler` if not already installed.
```
python attendance.py [filepath]

optional arguments:
    filepath                Path to the config file. Default: <script_dir>/config.txt
```

- The **config file** can be generated using [config_gen.py](../config_gen/) or [scraper.py](../scraper/).
- The config file is csv formatted with the following columns:
    - `Unique Web ID, Name, Roll Number, Password(DOB)`
        - Refer to *output format* in above links for more info.
- The config file can be modified while the script is running. It is reloaded for every slot in the timetable.
    - However, the path to the config file cannot be changed while the script is running.
- Log output is printed to `stdout`, any errors to `stderr`; saving them to a file can be done by redirecting all streams.
    - Ex: `python -u auto_attendance.py [filepath] *> log.txt`; `-u` for unbuffered output
        - refer to your shell's docs for more info about output redirection.

## Autorun Instructions
- Since this script needs to automatically mark attendance for all classes on time, it should run 27/7 or at least 0900-1900 on weekdays for proper functioning.
- One recommended way to do this on **windows** is to create a startup task using **task scheduler**.
    - Task scheduler allows you to run the script in the background on device startup.
        - It also allows you to stop/restart the script when required. 
    - Here is a [guide](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10#section-how-to-create-an-advanced-task-on-task-scheduler) on creating a task in task scheduler.
    - You can also import [this](./attendance.xml) preconfigured task that I made into task scheduler.
        - **Be aware** that this was made specifically for my system.
        - You need to explore the properties and modify them accordingly.
            - Change the **start-in/working directory** path in actions tab -> edit settings.
            - Change the **user account** in general tab -> security options.
    - You will still need to turn on your device at/before 0900 and keep it running throughout the day.
- **Linux** users can use `crontab` or `systemd` to achieve similar functionality.
- You can deploy this script on a VM/container in the cloud for hassle-free operation.
    - You can get free access to azure cloud by signing up for [GitHub student developer pack](https://education.github.com/pack).

## Advanced Details
- The script does not handle errors well.
    - Any problems with internet connection or problems on the server side may cause the script to crash.
- The script uses [Advanced Python Scheduler](https://apscheduler.readthedocs.io/en/3.x/userguide.html) to run during the specified timetable slots.
    - The exact time during which attendance is marked can be changed in the `start_scheduler` function.
- The scheduling is done inside the script using the `APScheduler` library.
    - If you want to fully control the scheduling using external methods (like task scheduler or crontab), you need to replace the call to `start_scheduler` with a call to `main`.
    
### Note: Tested on Python 3.10
    