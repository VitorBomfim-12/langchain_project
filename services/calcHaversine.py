import math
def calcHaversine(lat1,lon1,lat2,lon2):
    r=6372.8
    lat1= float(lat1)
    lat2= float(lat2)
    lon1= float(lon1)
    lon2= float(lon2)
    
    dlat = (lat2-lat1)
    dlon = (lon2-lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    
    dlat = math.radians(dlat)
    dlon = math.radians(dlon)

    a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
    b = math.asin((math.sqrt(a)))
    return 2*r*b
