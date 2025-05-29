import RPi.GPIO as gpio
import time as t

class MotorInstance:

    def __init__(self,PIN_PWM = 18,PIN_OUT1 = 25,PIN_OUT2 = 9,PIN_IN1 = 22,PIN_IN2 = 23,
                  freq = 50, kp = 2.1, kd = 0.05, ki = 0, Ts = 0.01, n=100, margin = 10):

        # Validate n parameter
        if abs(n) > 100:
            raise ValueError(f"Parameter 'n' must be between 0 and 100, got {n}")
        
        gpio.setmode(gpio.BCM)
        self.PIN_PWM = PIN_PWM
        self.PIN_OUT1 = PIN_OUT1
        self.PIN_OUT2 = PIN_OUT2
        self.PIN_IN1 = PIN_IN1
        self.PIN_IN2 = PIN_IN2
        self.freq = freq
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.Ts = Ts
        self.revs = 492 #amount of ticks per cycle for the specific motor used.
        self.n = n #PWM limit. maximum is 100%
        self.count = 0
        self.margin = margin

        gpio.setup(self.PIN_OUT1,gpio.OUT)
        gpio.setup(self.PIN_OUT2,gpio.OUT)
        gpio.setup(self.PIN_PWM,gpio.OUT)
        self.pwm_in = gpio.PWM(PIN_PWM,freq)
        gpio.setup(self.PIN_IN1,gpio.IN)
        gpio.setup(self.PIN_IN2,gpio.IN)
        gpio.add_event_detect(self.PIN_IN1, gpio.RISING, callback=self.cb)

    def forward(self):
        gpio.output(self.PIN_OUT1,True)
        gpio.output(self.PIN_OUT2,False)

    def backward(self):
        gpio.output(self.PIN_OUT1,False)
        gpio.output(self.PIN_OUT2,True)

    def stop_motor(self):
        gpio.output(self.PIN_OUT1,False)
        gpio.output(self.PIN_OUT2,False)

    def cb(self,channel):
        # global cnt
        if gpio.event_detected(channel):
            if gpio.input(self.PIN_IN2):
                #print('cw')
                self.count += 1
                #print(cnt)
            else:
                #print('ccw')
                self.count -= 1
                #print(cnt)
        return self.count

    def move(self, deg):
        
        Eacum = 0
        x = deg * self.revs / 360
        E = [x]
        self.pwm_in.start(0)
        stopper = False

        while not stopper:
            t.sleep(self.Ts)
            pos = self.cb(self.PIN_IN1)  # Read the position
            e = x - pos  # Calculate error
            e = round(e, 1)

            # Integral part
            Eacum += e

            # Derivative part
            E.append(e)
            d_e = (E[-1] - E[-2]) / self.Ts  # Calculate derivative

            # PID Control Law
            P = self.kp * e
            D = self.kd * d_e
            I = self.ki * Eacum
            u = P + I + D  # Control signal
            u = round(u, 2)

            # Apply control law
            duty_cycle = min(abs(u), self.n)
            self.pwm_in.ChangeDutyCycle(duty_cycle)
            
            if u >= 0:
                self.forward()
            else:
                self.backward()

            # Remove oldest error if array is too large
            if len(E) >= 50:
                E.pop(0)

            # Stop if error is consistently small
            if abs(e) <= self.margin and len(set(E[-15:])) == 1:
                stopper = True
        
        self.count = 0 #reset count
        self.stop_motor()  # Stop motor once in desired position
        self.pwm_in.stop() # stop pwm signal

    def __repr__(self):
        return (f"MotorInstance(\n"
                f"  PWM Pin: {self.PIN_PWM} (Output signal to motor controller),\n"
                f"  Output Pin 1: {self.PIN_OUT1} (Output signal to motor controller),\n"
                f"  Output Pin 2: {self.PIN_OUT2} (Output signal to motor controller),\n"
                f"  Encoder Input Pin 1: {self.PIN_IN1} (Motor encoder input pin),\n"
                f"  Encoder Input Pin 2: {self.PIN_IN2} (Motor encoder input pin)\n"
                f")")

if __name__ == "__main__":
    myinstance = MotorInstance()
    print(myinstance)
    myinstance.move(30)
    myinstance.move(30)
    myinstance.move(30)
    myinstance.move(30)
    myinstance.move(30)
    myinstance.move(30)
