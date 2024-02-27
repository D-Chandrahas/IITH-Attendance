### This is a simple alternative for the iith attandance app. It uses the same api as the official app and hence, is indistinguishable to the server. *
\* Not guaranteed. I am **not** responsible for any consequences of using this script. Use at your own risk.

# Features
- You can mark attendance from anywhere.
- No facial recognition, location checking etc.
- Attendance can be marked before the class starts or after the class ends.
    - However, this is not recommended since the erp server probably logs requests including time of request.
        - Although, I don't think anyone would check logs of thousands of students and requests per day.

# Usage
- Make sure you have `requests` installed.
    - If not, install it using `pip install requests`.
- Download and place [`attendance.py`](/attendance.py) in a folder of your choice.
- Run the script using `python attendance.py`.
    - The script creates a `config.json` file in the same folder as the script.
        - This file stores your credentials.

# Screenshots
![Screenshot1](/assets/img1.png)

# Notes
- The program was tested with `python 3.10`, `requests==2.31.0` on windows 10.
    - It should work on other versions of python and requests but I can't guarantee it.
- Only **one** user can be logged in at a time (per script file).
    - You can make multiple copies of the script and login as different user in each copy **but** make sure to place them in **different folders**.