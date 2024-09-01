# [config_gen.py](./config_gen.py)

- This script is used to generate the config file for the [auto_attendance.py](../auto_attendance/auto_attendance.py) script.
    - List of roll numbers and passwords can be provided as command line arguments or in a file. *Refer Usage*
- Output is printed to `stdout`, saving it to a file can be done by redirecting the output.
    - Ex: `python scraper.py [args] > config.txt`, refer to your shell's docs for more info.
    - Any errors are printed to `stderr`.
- The output is csv formatted with the following columns:
    - `Unique Web ID, Name, Roll Number, Password(DOB)`
        - *Note:* This is the same format as the config file for the [auto_attendance.py](../auto_attendance/auto_attendance.py) script.

### Usage:
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