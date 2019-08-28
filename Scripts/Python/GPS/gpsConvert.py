import re
import math

# Used to convert GPS from degrees to decimal
def gpsConvert(degrees, minutes):
    converted = degrees + (minutes/60)
    return converted
# End of GPS convert

print(gpsConvert(35, 10.244))
print(35 + (10.244/60))
print(89 + (50.241/60))