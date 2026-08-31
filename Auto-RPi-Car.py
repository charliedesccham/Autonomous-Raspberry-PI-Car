import RPi.GPIO as GPIO
import time
import threading
import random


GPIO.setmode(GPIO.BOARD)

running = True
Left = 0
Right = 0

#servo

SERVO = 12
GPIO.setup(SERVO, GPIO.OUT)

pwm=GPIO.PWM(SERVO, 50)
pwm.start(7.6)


#ultrasonic sensor

TRIG = 29
ECHO = 31

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
time.sleep(2)

# getting distance

def get_distance():
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2

    return distance
    


#motor 1 

EN = 11 
IN1 = 13
IN2 = 15

GPIO.setup(EN, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

#motor 1 going foward
def motor_forward():
    GPIO.output(EN, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

#motor 1 going back

def motor_back():
    GPIO.output(EN, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

#motor 1 going backed timed

def motor_back_time(seconds):
    motor_back()
    time.sleep(seconds)
    motor_stop()

#motor 1 forward time 

def motor_forward_time(seconds):
    motor_forward()
    time.sleep(seconds)
    motor_stop()

#motor 1 stopping

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

#motor 2

EN1 = 19 
IN3 = 21
IN4 = 23

GPIO.setup(EN1, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

#motor 2 going foward
def motor2_forward():
    GPIO.output(EN1, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

#motor 2 going back

def motor2_back():
    GPIO.output(EN1, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

#motor 2 going backed timed

def motor2_back_time(seconds):
    motor2_back()
    time.sleep(seconds)
    motor2_stop()

def motor2_forward_time(seconds):
    motor2_forward()
    time.sleep(seconds)
    motor2_stop()
#motor 2 stopping

def motor2_stop():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)



# motor combined functions

#both of them forward

def bothforward():
    
    t3 = threading.Thread(target=motor2_forward) 
    t4 = threading.Thread(target=motor_forward)
    t3.start() 
    t4.start()
    t3.join()
    t4.join()
 
def bothforwardtime(seconds):
    
    t8 = threading.Thread(target=motor2_forward_time, args=(seconds,)) 
    t9 = threading.Thread(target=motor_forward_time, args=(seconds,))
    t8.start() 
    t9.start()
    t8.join()
    t9.join()


def bothstopping():
    motor2_stop()
    motor_stop()

def bothbacktime(seconds):
    t1 = threading.Thread(target=motor_back_time, args=(seconds,))
    t2 = threading.Thread(target=motor2_back_time, args=(seconds,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

#turning



def turning_correctly():
    global Left
    global Right
    
    time.sleep(2)

    if Right > Left:
        print(f" i choose Right")
        time.sleep(1)
        bothbacktime(2)
        bothstopping()
        time.sleep(1)
        pwm.ChangeDutyCycle(6.4)
        time.sleep(0.5)
        bothforwardtime(2)
        bothstopping()
        time.sleep(1)
        pwm.ChangeDutyCycle(8.6)
        bothforwardtime(2)
        bothstopping()
        pwm.ChangeDutyCycle(7.6)
    else:
        print(f"i choose left")
        time.sleep(1)
        bothbacktime(2)
        bothstopping()
        time.sleep(1)
        pwm.ChangeDutyCycle(8.6)
        time.sleep(0.5)
        bothforwardtime(2)
        bothstopping()
        time.sleep(1)
        pwm.ChangeDutyCycle(6.4)
        bothforwardtime(2)
        bothstopping()
        pwm.ChangeDutyCycle(7.6)

#variables
dist = 0
lock = threading.Lock()
 
def task1():
    global dist

    while True:
            
            
        d = get_distance()  
        print(f"Distance: {dist:.2f} cm")
        with lock:
            dist = d
        time.sleep(0.1)

    
def task2():
    global Left
    global Right
    time.sleep(1)
    while True:
        with lock:
            current_dist = dist
       
        if current_dist > 10:

            bothforward()
            
        else:
        

            print("Safe distance reached, stopped")
            
            bothstopping()

            time.sleep(1)
            
            pwm.ChangeDutyCycle(6.4)
            time.sleep(2)
            get_distance()
            Right = get_distance()
            time.sleep(2)
            pwm.ChangeDutyCycle(8.6)
            time.sleep(2)
            get_distance()
            Left = get_distance()
            time.sleep(2)
            pwm.ChangeDutyCycle(7.6)


            print(f"going to tunring function, left was:{Left}, right was {Right} ")

            

            turning_correctly()

            time.sleep(2)

            print("done else loop")

            

            
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)
        
try:

    t1.start()
    t2.start()
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    bothstopping()  # stop both motors immediately
    GPIO.cleanup()
