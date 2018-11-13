import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import urllib.parse
import winsound
from datetime import datetime
import json
import time


def createHeader(filename):
    s = '入力方法,学籍番号,氏名'
    f = open(filename, 'r')
    jsonData = json.load(f)
    list_labo = jsonData['labo']
    for labo_name in list_labo:
        s = s + ',' + labo_name
    
    return s


def beep(freq, dur=100):
    winsound.Beep(freq, dur)


def createSaveFilename():
    st = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = 'QRdecode_' + st + '.csv'
    return filename


def saveRecord(record, filename, header):
    with open(filename, mode='w') as f:
        f.write(header + "\n")
        for line in record:
            s = 'QR,' + line + "\n"
            f.write(s)


def loop(cap, record):
    code = 0
    while True:
        if code == 0:
            ret, img = cap.read()
            cv2.imshow('camera', img)
            pil_img = Image.fromarray(img)
            data = decode(pil_img)
            
            if len(data) > 0:
                code = 1
                beep(4000, 500)
                s = data[0][0].decode('utf-8', 'ignore')
                s2 = urllib.parse.unquote(s)
                record.append(s2)
                print(s2)
                time.sleep(1)
                
                ret, img = cap.read()
                break
        
        key = cv2.waitKey(1)
        if key == 27:
            code = -1
            break
    
    return code



if __name__ == '__main__':
    labo_data_filename = '研究室.json'
    header = createHeader(labo_data_filename)

    save_filename = createSaveFilename()
    record = []

    while True:
        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 800)
        cap.set(5, 15)
        
        if loop(cap, record) == -1:
            cap.release()
            break
        
        cap.release()
    
    if len(record) > 0:
        saveRecord(record, save_filename, header)
    
    cv2.destroyAllWindows()
