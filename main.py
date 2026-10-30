from machine import Pin
from utime import sleep
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from dht import DHT11, InvalidChecksum
import math

dhtPIN = 15
dhtSensor = DHT11(Pin(dhtPIN, Pin.OUT, Pin.PULL_DOWN))

def theta(wind_speed) :
    return 25 + (19 * wind_speed)

def area(diameter) :
    return round((math.pi * math.pow(diameter/2, 2))/10000, 5)

def humid_ratio_saturated(temperature) :
    return round((14.7 * temperature)/20000, 5)

def humidity_ratio(area) :
    return round((0.0098 * area)/10000, 5)

def get_evaporation_rate(wind_speed, diameter, temperature) :
    return round(theta(wind_speed) * area(diameter) * (humid_ratio_saturated(temperature) - humidity_ratio(area(diameter))), 5)

def pump_on(time) :
    global pump
    pump.value(0)
    sleep(time)
    pump.value(1)

# Total time taken using rate (kg/h) and volume of water
def total_time_seconds(rate, volume) :
    return int(round(volume/(rate * 1000)*3600, 0))

def time_convert(seconds) :
    hours = seconds // 3600
    minutes = (seconds - (hours * 3600)) // 60
    seconds = seconds - ((hours * 3600) + (minutes * 60))
    return (hours, minutes, seconds)

def show_value_water(sign) :
    global water_level
    if sign == "+" :
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Current waterlvl")
        lcd.move_to(0, 1)
        lcd.putstr(f": {water_level + 10} ml")
        water_level += 10
        print(f"water level value: {water_level}")
    else :
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Current waterlvl")
        lcd.move_to(0, 1)
        lcd.putstr(f": {water_level - 10} ml")
        water_level -= 10
        print(f"water level value: {water_level}")
        
def show_value_diameter(sign) :
    global diameter
    if sign == "+" :
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Pot diameter")
        lcd.move_to(0, 1)
        lcd.putstr(f": {diameter + 1} cm")
        diameter += 1
        print(f"diameter value: {diameter}")
    else :
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Pot diameter")
        lcd.move_to(0, 1)
        lcd.putstr(f": {diameter - 1} cm")
        diameter -= 1
        print(f"diameter value: {diameter}")

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

# LCD variables
i2c = I2C(0, sda = machine.Pin(0), scl = machine.Pin(1), freq = 400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Button variables
button_toggle = Pin(2, Pin.IN, Pin.PULL_DOWN)
button_water_now = Pin(3, Pin.IN, Pin.PULL_DOWN)
button_plus = Pin(4, Pin.IN, Pin.PULL_DOWN)
button_minus = Pin(5, Pin.IN, Pin.PULL_DOWN)

# Pump variables
pump = Pin(16, Pin.OUT)

water_level = 10
diameter = 10
is_water_level = True
lcd.custom_char(0, bytearray([0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E]))
time_elapsed = 0
seconds_value = 0

# Intro screen
print(f"water_level value: {water_level}")
lcd.clear()
lcd.move_to(5, 0)
lcd.putstr("JARDIN")
for x in range(0, 17) :
    lcd.move_to(x, 1)
    lcd.putchar(chr(0))
    # Remember to change to 0.5 later... 
    sleep(0.1)
lcd.clear()

while True :
    if seconds_value % 100 == 0 :
        temperature = dhtSensor.temperature
        print(f"{time_elapsed}. Temp: {temperature}°C")
        
    evaporation_rate = get_evaporation_rate(0.02, diameter, temperature)
    predicted_time = total_time_seconds(evaporation_rate, water_level)
    
    # Increases selected value 
    while button_plus.value() :
        if is_water_level :
            show_value_water("+")
        else :
            show_value_diameter("+")
        while button_plus.value() :
            sleep(1)
        sleep(1)
        lcd.clear()
            
    # Decreases selected value
    while button_minus.value() :
        if is_water_level :
            show_value_water("-")
        else :
            show_value_diameter("-")
        while button_minus.value() :
            sleep(1)
        sleep(1)
        lcd.clear()
            
    # Toggles between "DIAMETER" and "WATER LEVEL"
    while button_toggle.value() :
        if is_water_level == True :
            lcd.clear()
            lcd.move_to(2, 0)
            lcd.putstr("Editing value")
            lcd.move_to(4, 1)
            lcd.putstr("DIAMETER")
            is_water_level = False
            print(f"Value changed : DIAMETER")
        else :
            lcd.clear()
            lcd.move_to(2, 0)
            lcd.putstr("Editing value")
            lcd.move_to(3, 1)
            lcd.putstr("WATER LEVEL")
            is_water_level = True
            print(f"Value changed : WATER LEVEL")
        while button_toggle.value() :
            sleep(0.01)
        sleep(1)
        lcd.clear()
            
    # Waters the plant immediately
    while button_water_now.value() :
        pump_on(water_level / 10)
        print("WATERING NOW ...")
        while button_water_now.value() :
            sleep(0.01)
            
    seconds_value += 10
    if seconds_value % 100 == 0 :
        time_elapsed += 1
    lcd.move_to(0, 0)
    lcd.putstr("Time left -~")
    lcd.move_to(0, 1)
    time_left = time_convert(predicted_time - time_elapsed)
    lcd.putstr(f": {time_left[0]} hr {time_left[1]} m {time_left[2]} s")
    
    if predicted_time - time_elapsed == 0 :
        pump_on(water_level / 10)
        time_elapsed = 0
    
    sleep(0.01)

    