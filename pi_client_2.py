import socket
import RPi.GPIO as GPIO
from time import sleep

LED_PIN = 18
PWM_FREQ = 50
DUTY_CYCLE = 100

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
pwm_laser = GPIO.PWM(LED_PIN, PWM_FREQ)
pwm=GPIO.PWM(7, 50)

server_ip = '192.168.137.48'
server_port = 5431
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
client_socket.connect((server_ip, server_port))


def setAngle(angle):
    if angle <= 0:
        angle = 0
    if angle >= 180:
        angle = 180
    pwm.start(0)
    duty_1 = angle / 18 + 2
    duty = abs(duty_1)
    print(duty)
    print(type(duty))
    #if int(duty) >= 0 and int(duty) <= 180: 
    GPIO.output(7, True)
    pwm.ChangeDutyCycle(duty)
    #sleep(1)
    
    #GPIO.output(12, False)
    #pwm.ChangeDutyCycle(duty)

def main():
    setAngle(90)
    x = 90
    while True:       
    #message = ("192, 169, 1")
        message = client_socket.recv(1024).decode()
  
        print("Message from server:", message)
        values = message.strip("()").split(",")
        print(type(values))
        right = values[0]
        #left = values[1]
        #centre_x = values[1]
#         centre_y = values[3]
        flag_laser = values[1]
        print("Value 1:",right)
#         print("Value 2:",left)
        #print("Value 3:", centre_x)
#         print("Value 4:", centre_y)
        print("Value 4:",flag_laser)
        print(type(flag_laser))
        print(int(flag_laser))
        
        if int(flag_laser) == 1:
            print("laser")
            pwm_laser.start(DUTY_CYCLE)
            print("values")
            if int(right) == 1:
                print("hello world")
                setAngle(x)
                x = x + 10
            elif int(right) == 2:
                print("left world")
                setAngle(x)
                x = x - 10
#             if int(centre_x) >= int(lower) and int(centre_x) <= int(upper):
#                 print("No movement")
#             else:
#                 if int(centre_x) < int(lower):
#                     #if x >= 0 and x <= 180:
#                     setAngle(x)
#                     x = x + 10
#                 elif int(centre_x) > int(upper):
#                     #if x >= 0 and x <= 180:
#                     setAngle(x)
#                     x = x - 10
        
#         if int(value_5) == 1:
#             pwm.start(DUTY_CYCLE)
        
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(LED_PIN, GPIO.OUT)
        #pwm = GPIO.PWM(LED_PIN, PWM_FREQ)
        
            
        elif int(flag_laser) == 0:
            pwm_laser.stop()
        #GPIO.cleanup()

        
        
    
# Printing the values stored in different variables
        # Close client socket
    client_socket.close()
    
if __name__ == "__main__":
    main()

