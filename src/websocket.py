from websocket_server import WebsocketServer
import threading
import cv2
import base64
import time

camera1 = None
frame = cv2.imread("1.jpg", cv2.IMREAD_COLOR)
rtsp_path = 0


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # 发送给所有的连接
    try:
        server.send_message_to_all("Hey all, a new client has joined us")
    except:
        pass

# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s" % (client['id'], message))
    global camera1
    camera1 = cv2.VideoCapture(message)


# 发送给所有的连接
# server.send_message_to_all(message)
def from_vedio():
    thread1 = threading.Thread(target=vedio_thread1, args=(1,))
    #     thread1.setDaemon(True)
    thread1.start()
    thread2 = threading.Thread(target=vedio_thread2, args=(1,))
    #     thread1.setDaemon(True)
    thread2.start()
    print('start')


def vedio_thread1(n):
    print('send')
    while True:
        if len(server.clients) > 0:
            image = cv2.imencode('.jpg', frame)[1]
            base64_data = base64.b64encode(image)
            s = base64_data.decode()
            # print('data:image/jpeg;base64,%s'%s)
            server.send_message_to_all('data:image/jpeg;base64,%s' % s)
        time.sleep(0.05)

def facedetect(img):
    detector = cv2.CascadeClassifier('eyedetect.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    # if len(faces) >= 1:
        # print("发现{0}个人脸!".format(len(faces)))

    for (x, y, w, h) in faces:
        # cv2.rectangle(image,(x,y),(x+w,y+w),(0,255,0),2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imshow('',img)
    return img


def vedio_thread2(n):
    global camera1
    camera1 = cv2.VideoCapture(0)
    global frame
    while True:
        _, img_bgr = camera1.read()
        if img_bgr is None:
            camera1 = cv2.VideoCapture(0)
            print('丢失帧')
        else:
            frame = facedetect(img_bgr)


# Server Port
PORT = 8880
# 创建Websocket Server
server = WebsocketServer(PORT, '2001:da8:201d:1103:24a3:402a:4762:6501')
from_vedio()
# 有设备连接上了
server.set_fn_new_client(new_client)
# 断开连接
server.set_fn_client_left(client_left)
# 接收到信息
server.set_fn_message_received(message_received)
# 开始监听
server.run_forever()
