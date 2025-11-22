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

SSH:
  python bruteBomb.py -c ssh -ip '1.1.1.1' -u 'username' -p /file/path/password.txt
  python bruteBomb.py -c ssh -ip '1.1.1.1' -u username.txt -p /file/path/password.txt
  python bruteBomb.py -c ssh -port 22 -ip '1.1.1.1' -u username.txt -p /file/path/password.txt

FTP:
  python bruteBomb.py -c ftp -ip '1.1.1.1' -u 'username' -p /file/path/password.txt
  python bruteBomb.py -c ftp -ip '1.1.1.1' -u username.txt -p /file/path/password.txt
  python bruteBomb.py -c ftp -port 21 -ip '1.1.1.1' -u username.txt -p /file/path/password.txt

HTTP/S (line command is the same):
  python bruteBomb.py -c http -ip '1.1.1.1/index.php?action=login2' -u 'username' -p password.txt --header 'User-Agent: Mozilla/2.0' 'Cookie: PHPSESSID=example1234' --data 'user' 'passw' 'otherthings' --valueData '0' -bc 'Username e password non corretti'
  python bruteBomb.py -c https -ip '1.1.1.1/index.php?action=login2' -u 'username' -p password.txt --header 'User-Agent: Mozilla/2.0' 'Cookie: PHPSESSID=example1234' --data 'user' 'passw' 'otherthings' --valueData '0' -bc 'Username e password non corretti'
