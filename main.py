import RPi.GPIO as gpio
from motor_module.motorclass import MotorInstance
from time import sleep
import picamera
from pathlib import Path
import threading

def motor_control(stop_event):
    """Motor control function to run in a separate thread"""
    basemotor = MotorInstance(kp = 6.5)
    arm = MotorInstance(kp = 1.1,kd = 0.08,ki = 0,PIN_PWM = 27,PIN_OUT1 = 5, PIN_OUT2 = 6,
                     PIN_IN1 = 16, PIN_IN2 = 19)

    print('starting motor movements ...')
    # Execute the motormovement sequence
    for i in range(5):
        print(f'Motor sequence {i+1}')
        arm.move(1300)
        basemotor.move(-50)
        #sleep(0.1)
        arm.move(-1220)
        basemotor.move(-50)

    arm.move(-500)
    for i in range(15):
        arm.move(1500)
        basemotor.move(-50)
        arm.move(-1420)
        basemotor.move(-50)

    arm.move(500)
    basemotor.move(2000)

    print("Motor Movements completed! ")
    # Signal the camera thread to stop
    stop_event.set()
    # Cleanup GPIO
    gpio.cleanup()
    
def camera_capture(stop_event, object_name):
    """Camera capture function to run in a separate thread"""
    # Create images directory using pathlib
    images_dir = Path.cwd() / "images" / object_name
    images_dir.mkdir(parents=True, exist_ok=True)
    print(f"Starting camera capture, saving to: {images_dir}")
    with picamera.PiCamera() as camera:
        # Camera settings
        camera.contrast = 0
        camera.brightness = 67
        camera.exposure_compensation = 25
        camera.shutter_speed = 8500
        camera.resolution = (1080, 720)
        camera.start_preview()

        counter = 0

        # Capture images until motor thread signals to stop
        while not stop_event.is_set():
            filename = images_dir / f"{counter}.jpeg"
            camera.capture(str(filename))
            print(f"Captured: {filename}")
            counter += 1
            sleep(0.1)  # Small delay between captures

        camera.stop_preview()
        print(f"Camera capture completed! Total images captured: {counter}")

def main():
    # Get object name from user
    print('Enter Object name:')
    object_name = input().strip()

    if not object_name:
        print("Object name cannot be empty!")
        return

    # Create an event to signal when motor movement is complete
    stop_event = threading.Event()

    # Create threads for motor control and camera capture
    motor_thread = threading.Thread(target=motor_control, args=(stop_event,))
    camera_thread = threading.Thread(target=camera_capture, args=(stop_event, object_name))

    # Start both threads
    print("Starting parallel execution...")
    motor_thread.start()
    camera_thread.start()


    # Wait for both threads to complete
    motor_thread.join()
    camera_thread.join()

    print("All operations completed successfully!")

if __name__ == "__main__":
    main()