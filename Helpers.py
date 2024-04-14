import math

def float_range(start, stop, step):
    while start < stop:
        yield start
        start += step
        
def next_position(distance, rad, offset):
    x = int(distance * math.sin(rad)) + offset[0]
    y = int(-distance * math.cos(rad)) + offset[1]
    return (x,y)

def outside_bounds(val, min, max):
    if val <= min or val >= max:
       return True
    return False
        
