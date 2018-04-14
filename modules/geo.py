from geopy.distance import great_circle
import geopy

pointA = geopy.point.Point(43.34222, -86.233444)
pointB = geopy.point.Point(35.10, -85.11000)

print(great_circle(pointA, pointB).miles)



