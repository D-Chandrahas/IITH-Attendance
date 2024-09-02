### If you are interested in automating the process of marking attendance, check out [auto-attendance](./auto_attendance/).
### If you are interested in scraping/brute-forcing credentials/passwords, check out [scraper](./scraper/).

---

### This is a simple alternative for the iith attandance app. It uses the same api endpoint as the official app. *
\* I am **not** responsible for any consequences of using this script. Use at your own risk.

# Features
- You can mark attendance from anywhere.
- No facial recognition, location checking etc.
- ~~Attendance can be marked before the class starts or after the class ends.~~
    - This feature is no longer available as time-of-request check is added on the server side.


# Usage
- Make sure you have `requests` installed.
    - If not, install it using `pip install requests`.
- Download and place [`attendance.py`](/attendance.py) in a folder of your choice.
- Run the script using `python attendance.py`.
    - The script creates a `config.json` file in the same folder as the script.
        - This file stores your credentials.
- Enter your username and password to login.
    - Enter `S.No` of the class you want to mark attendance for.

# Screenshots
![Screenshot1](/assets/img1.png)

# Advanced usage
```
usage: python attendance.py [filepath]

optional arguments:
    filepath                Path to the config file. If it doesn't exist, it will be created.
```
### Examples:
```
python attendance.py 'C:\Users\<user>\Documents\config1.json'
python attendance.py '.\file3.json'
```

# Notes
- The program was tested with `python 3.10`, `requests==2.31.0` on windows 10.
    - It should work on other versions of python and requests but I can't guarantee it.
- Only **one** user can be logged in at a time (**per config file**).
    - To use multiple accounts, create multiple config files.
        - Refer to [Advanced usage](#advanced-usage) for details.

# Troubleshooting
- If you encounter any issues, try deleting the `config.json` file and running the script again.
    - If the issue persists, open an issue on github with steps to reproduce the issue.
    
