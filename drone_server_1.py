from ultralytics import YOLO
import cv2
import cvzone
import math
import io
import socket
import struct
from PIL import Image
import cv2
import numpy
import sys
import torch
import data
#import droneEdit_2 as de

x = 0
def new():
	global x
	return x

def GET(message):
    reply = message
    return reply
#x=0
y=0
lst = []

def main():

	global threshold
	threshold = 50
	global send_data
	global lst
	global x
	global y
	global right
	global left
	right = 2
	left = 2
	server_socket = socket.socket()
	server_socket.bind(("192.168.137.48", 8000))
	server_socket.listen(0)
	print("Listening")
	connection = server_socket.accept()[0].makefile('rb')

	model = YOLO("kaggleDroneModel.pt")
	device: str = "gpu" if torch.backends.mps.is_available() else "cpu"
	model.to(device)
	classNames = ["drone"]
	img = None


	while True:
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))
		image_stream.seek(0)
		image = Image.open(image_stream)
		img = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
		img_cpy = img.copy()
		height, width , hello = img.shape
		print(height,width)
		cv2.line(img, (0,height//2), (width, height//2), (255, 0, 255), 4)
		cv2.line(img, (width//2, 0), (width//2,height), (255, 255, 0), 4)
		upper_limit = (width//2) + threshold
		lower_limit = (width // 2) - threshold
		cv2.line(img, (upper_limit, 0), (upper_limit,height), (0, 255, 0), 1)
		cv2.line(img, (lower_limit, 0), (lower_limit, height), (0, 255, 0), 1)

		results = model(img_cpy, stream=True) # Stream=True means it wil use generaters and it will be more efficient
		objects_detected = False

		for r in results:
			boxes = r.boxes
			for box in boxes:
				x1, y1, x2, y2 = box.xyxy[0]
				x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
				w, h = x2-x1, y2-y1

				conf = math.ceil((box.conf[0] * 100))/100
				print(conf)
				print(type(conf))
				print(x1,y1)
				print(x2,y2)
				print(w,h)
				print(w//2,h//2)

				if conf > 0.80:
					send_data = 1
					cvzone.cornerRect(img, (x1, y1, w, h))
					centre_x = ((x1 + x2) // 2)
					cv2.circle(img, (centre_x,(y1 + y2) // 2), 3, (255, 0, 0), 2)
					#cv2.circle(img, ((x1+w//2),(y1+h//2)), 3, (255, 0, 0), 2)
					cls = int(box.cls[0])
					cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=0.7, thickness=1)
					# error = (x1+w/2)-height/2
					# if error > 10:
					# 	right = 1
					# if error < -10:
					# 	right = 2
					if centre_x >= lower_limit and centre_x <= upper_limit:
						print("No Movement")
						right = 0
					else:
						if centre_x < lower_limit:
							right = 1
						elif centre_x > upper_limit:
							#left = 4
							right = 2


				else :
					send_data = 0

				data = (right, send_data)

				#data = f"{lower_limit} {upper_limit} {(x1+x2)//2} {(y1+y2)//2} {send_data}"
				print("Data is : ", data)
				lines = str(data)
				print(lines)
				with open('readme.txt', 'w') as f:
					for line in lines:
						f.write(line)

				#print(new())
		if not objects_detected:
			print("No objects detected in this frame.")
			send_data = 0
		cv2.imshow("Image", img)

		cv2.waitKey(1)

if __name__ == "__main__":
	main()
