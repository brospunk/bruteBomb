python bruteBomb3.py --help                                             
usage: bruteBomb3.py -c {ssh,ftp,http} -ip IP -u USERNAME -p PASSWORDS

Brute-force SSH, FTP, and HTTP

options:
  -h, --help            show this help message and exit
  -c, --command {ssh,ftp,http}
                        Command type (ssh/ftp/http)
  -ip, --ip IP          Target IP address
  -u, --username USERNAME
                        Username (can be a file or a single string)
  -p, --passwords PASSWORDS
                        Password file or list of passwords


EXAMPLES:
- python bruteBomb.py -c ssh -ip 10.210.96.20 -u "username" -p /file/path/password.txt
- python bruteBomb.py -c ssh -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
- python bruteBomb.py -c ftp -ip 10.210.96.20 -u "username" -p /file/path/password.txt
- python bruteBomb.py -c ftp -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
