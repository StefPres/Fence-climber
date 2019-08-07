import Adafruit_PCA9685
import time
from evdev import InputDevice, categorize

pwm = Adafruit_PCA9685.PCA9685()
pwm_frequency = 50
pwm.set_pwm_freq(pwm_frequency)
servo_min = (145 * pwm_frequency) // 50
servo_max = (580 * pwm_frequency) // 50

def servoSetting(angle):
    return ((servo_max - servo_min) * angle//180 + servo_min)

def motorSetting(speed):
    return int(speed * 4095.0 / 100.0)

gamepad = InputDevice('/dev/input/event0')
print(gamepad)

if __name__ == '__main__':
    try:

        pwm.set_pwm(0, 0, servoSetting(180)) #arm 1
        pwm.set_pwm(1, 0, servoSetting(0)) #arm 2
        pwm.set_pwm(3, 0, servoSetting(180)) #claw 1
        pwm.set_pwm(4, 0, servoSetting(0)) #claw 2
        
        noError = True
        while noError:
            try:
                for event in gamepad.read():
                    eventinfo = categorize(event)
                    if event.type == 1:
                        newbutton = True
                        codebutton  = eventinfo.scancode
                        valuebutton = eventinfo.keystate
                        if(codebutton == 308):
                            if(valuebutton == 1):
                                print("Arms out...")
                                pwm.set_pwm(0, 0, servoSetting(115)) #arm 1
                                pwm.set_pwm(1, 0, servoSetting(45)) #arm 2
                                time.sleep(1)
                                print("Latching fence...")
                                pwm.set_pwm(3, 0, servoSetting(80)) #claw 1
                                pwm.set_pwm(4, 0, servoSetting(100)) #claw 2
                                time.sleep(1)
                                print("Positive latch. \nPulling robot up...")
                                pwm.set_pwm(0, 0, servoSetting(180)) #arm 1
                                pwm.set_pwm(1, 0, servoSetting(0)) #arm 2
                                time.sleep(2)
                                print("Unlatching...")
                                pwm.set_pwm(3, 0, servoSetting(180)) #claw 1
                                pwm.set_pwm(4, 0, servoSetting(0)) #claw 2
                                time.sleep(1)
                                print("Unlatched")
            except:
                pass
                            

                
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pwm.set_pwm(0, 0, servoSetting(180))
        pwm.set_pwm(1, 0, servoSetting(0))
        pwm.set_pwm(3, 0, servoSetting(180))
        pwm.set_pwm(4, 0, servoSetting(0))
        time.sleep(1)
        print("Program stopped by User")
        #GPIO.cleanup()
