# [scraper.py](./scraper.py)

- This script can be used to brute force passwords for the attendance app ( which are DOBs )
    - List of roll numbers can be provided as command line arguments or in a file. *Refer Usage*
- Scraping all credentials can be done by running the script with no arguments.
    - List of departments and batches to scrape can be changed by editing the lists at the end of the script.
- Output is printed to `stdout`, saving it to a file can be done by redirecting the output.
    - Ex: `python scraper.py [args] > output.txt`, refer to your shell's docs for more info.
    - Any errors are printed to `stderr`.
- The output is csv formatted with the following columns:
    - `Unique Web ID, Name, Roll Number, Password(DOB)`
        - *Note:* This is the same format as the config file for the [auto_attendance.py](../auto_attendance/auto_attendance.py) script.

### Usage: 
```
    python scraper.py [-h | --help]; Display this help page
    python scraper.py [rollno1] [rollno2] ...
    python scraper.py [file_path]
    python scraper.py; Scrape all btech students' credentials

(do not include brackets)
```
Input file format:
```
rollno1
rollno2
...
```
Output format:
```
WebID1,Name1,rollno1,password1
WebID2,Name2,rollno2,password2
...
```