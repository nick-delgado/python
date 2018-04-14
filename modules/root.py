from node import Aircraft


def check_status(planes):
    '''Check whether the airplanes can fly'''
    if planes.can_fly == True:
        print("Y")
    else:
        print("N")

AIRPLANES = Aircraft()
check_status(AIRPLANES)

