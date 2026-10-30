import math

# Evaporation rate of water in kilograms per hour (kg/h)
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


# Total time taken using rate (kg/h) and volume of water
def total_time_hours(rate, volume) :
	return round(volume/(rate * 1000), 2)

def total_time_seconds(rate, volume) :
	return int(round(volume/(rate * 1000)*3600, 0)) 



rate = get_evaporation_rate(0.02, 15, 20)
total_time_hours = total_time_hours(rate, 50) 
total_time_seconds = total_time_seconds(rate, 50)
print(f"The water evaporates at a rate of {rate} kg/h.")
print(f"It will take approx. {total_time_hours} hours or {total_time_seconds} seconds to completely evaporate.")
print("")


def time_convert(seconds) :
	hours = seconds // 3600
	minutes = (seconds - (hours * 3600)) // 60
	seconds = seconds - ((hours * 3600) + (minutes * 60))
	return (hours, minutes, seconds)

print(time_convert(total_time_seconds))
