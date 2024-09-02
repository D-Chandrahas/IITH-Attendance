# [config_gen.py](./config_gen.py)

- This script is used to generate the config file for the [auto_attendance.py](../auto_attendance/) script.
    - List of roll numbers and passwords can be provided as command line arguments or in a file. *Refer Usage*
- Output is printed to `stdout`, saving it to a file can be done by redirecting the output.
    - Ex: `python -u scraper.py [args] > config.txt`; `-u` for unbuffered output
        - refer to your shell's docs for more info about output redirection.
    - Any errors are printed to `stderr`.
- The output is csv formatted with the following columns:
    - `Unique Web ID, Name, Roll Number, Password(DOB)`
        - *Note:* This is the same format as the config file for the [auto_attendance.py](../auto_attendance/) script.
---
### Usage:
Requires `requests` module. Install with `pip install requests` if not already installed.
```
    python config_gen.py [-h | --help]; Display this help page
    python config_gen.py [rollno1,password1] [rollno2,password2] ...
    python config_gen.py [file_path]

(do not include brackets)
```
Input file format:
```
rollno1,password1
rollno2,password2
...
```
Output format:
```
WebID1,Name1,rollno1,password1
WebID2,Name2,rollno2,password2
...
```
### Note: Tested on Python 3.10, 3.11