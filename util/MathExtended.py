import math
import numpy 

'''
Created on Sep 28, 2013

@author: Karl
'''
def distance(x1, y1, x2, y2):
    """Returns distance between point (x, y) and character icon""" 
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) **2))
 
def triangleAngle(x1, y1, x2, y2, x3, y3):
    """
    Returns angle of triangle in radians.
    Given three points, determine the lengths of each side, then return 
    the angle with (x1, y1) as the vertex. 
    """
    #x1,y1 = C, x2,y2 = A, x3,y3 = B
    c = distance(x2, y2, x3, y3)
    a = distance(x1, y1, x3, y3)
    b = distance(x1, y1, x2, y2)
    return math.acos(((a**2) + (b**2) - (c**2))/(2*a*b))
 
def polynomialFit(x, y, degree):
    return numpy.polyfit(x, y, degree)

def thirdDegreePolyFit(x):
    '''
    Returns the pixel distance for 1 second at each minimap level
    Coefficients:
                0.3452381    5.8452381   14.42857143'''
    #Divided by 5 because poly fit was determined with 5 second runs
    return ((-0.04395018 * (x**2)) + (4.13683274 * (x)) + 10.2411032) 
    
if __name__ == '__main__':

    x = [5, 10, 12, 15]
    y = [30, 46, 55, 62]
    print polynomialFit(x, y, 2)
    print thirdDegreePolyFit(18)
    