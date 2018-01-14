from gpiozero import LightSensor

sensor = LightSensor(4)

while True:
    sensor.wait_for_light()
    print("It's dark! :)")
    sensor.wait_for_dark()
    print("It's light :(")