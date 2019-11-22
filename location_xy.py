# Make sure that you installed SciPy
# python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
from scipy.optimize import fsolve
import math

T1 = 0
T2 = 0
T3 = 0
D = 1
C = 343



#__________________________________________________________
#__________________________________________________________
#
#
#    The setup follows the diagram below:
#
#               M1-----O-----M2
#                  ---------
#                   -------
#                    -----
#                      -
#                      M3
#
# Where M1, M2, M3 represent the three microphones.
# They form a equilateral triangle, with side length of 2d.
# O is the origin of the coordinate.
#__________________________________________________________
#__________________________________________________________




# t1, t2, t3 are the time of arrivial recorded by the three microphones.
# d is half of the distance between each microphone
# c is the speed of sound
def locationXY(t1, t2, t3, d, c):
    global T1
    global T2
    global T3
    global D
    global C
    T1 = t1
    T2 = t2
    T3 = t3
    D = d
    C = c

    x, y =  fsolve(equations, (0, 0))
    print(x, y)
    # print('Off by: ', equations((x, y)))
    return((x, y))


def equations(p):
    x, y = p
    return(((x+D)**2 + y**2)**0.5 - ((x-D)**2 + y**2)**0.5 - (T1-T2)*C,
           (x**2 + (y+3**0.5*D)**2)**0.5 - ((x-D)**2 + y**2)**0.5 - (T3-T2)*C)



if __name__ == '__main__':
    print('\n Case: 3^0.5 meters above origin: ')
    locationXY(2/343, 2/343, (2*3**0.5)/343, 1, 343)

    print('\n Case: On Micorphone #1: ')
    locationXY(0+1, 2/343+1, 2/343+1, 1, 343)

    print('\n Case: On Micorphone #2: ')
    locationXY(2/343+1, 0+1, 2/343+1, 1, 343)

    print('\n Case: On Micorphone #3: ')
    locationXY(2/343+1, 2/343+1, 0+1, 1, 343)

