# Jardin
Jardin - An Automatic plant watering system

INTRODUCTION 
This is a device that I have made, which will enable you to water your plants when 
you are away from home especially on long vacations. It has been programmed to 
water your plants automatically when it determines that the amount of water in the 
pot is sub-optimal by intelligently detecting ambient temperature and calculating 
the approximate time after which the water in the pot will need to be replenished.

This device saves water because it only waters the plant when necessary, that is, 
when all the water in the pot evaporates away. It also delivers the water in fixed 
amounts, hence avoiding over-watering of the plant.

PRINCIPLE AND WORKING
As we all know evaporation depends on a number of factors, which include 
humidity, temperature, wind speed and surface area. Using the ambient  
temperature reading from the DHT11, it calculates the evaporation rate in 
kilograms per hour (kg/hr)

This evaporation rate is used to compute the total amount of time required for all 
the water in the pot to evaporate away.

This time is variable as the temperature varies constantly. Hence, a timer is started 
whenever the device is powered on and is reset when the plant is watered. The 
time till the next watering is the time calculated minus the timer value, thus 
providing us with a count-down timer.

When all the water in the pot is evaporated away, the device turns on a pump and 
waters the plant. This cycle then continues.

As you can see on the display, when the diameter is increased, the time decreases. 
When the water level is increased, the time increases. This is because evaporation 
rate is inversely proportional to surface area, and directly proportional to the 
volume of water.

COMPONENTS
• This device is powered by a micro-controller called the RaspberryPi Pico which 
is powered by 4 AA batteries.
• A pipe connects the source of water [Bottle] to the pump which in turn pumps 
the water into the pot. 
• A Pump helps transfer water from the reservoir which is powered by a 9V 
battery. 
• This pump can be controlled by the RaspberryPi by a 5V Relay. 
• An LCD Display provides a simple User Interface. 
• Four Buttons allow the user to edit and control various aspects of the device.
 - A Plus Button  to increase values be it water level or diameter.
 - A Minus Button to decrease values be it water level or diameter.
 - A Toggle Button to switch between diameter and water-level editing modes
 - A Water-Now Button to immediately water the plant.
• The device can monitor the ambient temperature by using a sensor called the 
DHT11.

The device is programmable in such a way that the user can input the value of the 
diameter of the plant pot and also adjust the amount of water given to the plant at 
each watering cycle. Thus, the device can be customised as per the plant’s needs.
