# bruteBomb

### Brute-force SSH, FTP e HTTP/S
### Strumento da linea di comando per effettuare test di sicurezza su servizi di autenticazione.

## ⚠️ Disclaimer ⚠️

### Questo tool è pensato esclusivamente per test di sicurezza autorizzati (penetration testing, audit interni, esercitazioni).
### L'uso non autorizzato su sistemi di terzi può violare leggi locali e internazionali.
### L’autore non è responsabile per eventuali usi impropri.

## 🔧 Help

```bash
python bruteBomb3.py --help
usage: bruteBomb.py [-h] -c {ssh,ftp,https,http} [-port PORT] -ip IP -u USERNAME -p PASSWORDS [-H HEADER [HEADER ...]] [-d DATA [DATA ...]] [-vd VALUEDATA [VALUEDATA ...]] [-bc BADCONDITION [BADCONDITION ...]] [-gc GOODCONDITION [GOODCONDITION ...]]

Brute-force SSH, FTP, and HTTP/S

options:
  -h, --help            show this help message and exit
  -c, --command {ssh,ftp,https,http}
                        Command type (ssh/ftp/https/http)
  -port, --port PORT    Specify the port (it can be empty)
  -ip, --ip IP          Target IP address
  -u, --username USERNAME
                        Username (can be a file or a single string)
  -p, --passwords PASSWORDS
                        Password file or list of passwords
  -H, --header HEADER [HEADER ...]
                        Header HTTP/S. Non sei obbligato ad aggiungerlo
  -d, --data DATA [DATA ...]
                        Header HTTP/S. I primi due campi da dichiarare sono user e password, puoi aggiungerne altri ma poi devi dichiarare il valore con --valueData
  -vd, --valueData VALUEDATA [VALUEDATA ...]
                        Header HTTP/S. Usalo per dare i valori alla data
  -bc, --badCondition BADCONDITION [BADCONDITION ...]
                        La condizione negativa della risposta del server http/s per continuare a bruteforsare
  -gc, --goodCondition GOODCONDITION [GOODCONDITION ...]
                        La condizione positiva della risposta del server http/s per smettere di bruteforsare
```


## 👉 EXAMPLES
```bash
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
```
