

class Aircraft():
    def __init__(self, tailnumber):
        self.reg = tailnumber

    def setProperty(self, which, value):
        #Right now all these functions are being called
        switcher = {
                'name'  : self.__setNameProperty(value),
                'weight' : self.__setWeightProperty(value),
                'cruising-speed' : self.__setCruisingSpeedProperty(value),
                'cruising-altitude' : self.__setCruisingAltitudeProperty(value)
                }
        return switcher.get(which, 'error')

    def __setNameProperty(self, name):
        self.name = name
        print(self.name)
        return True

    def __setWeightProperty(self, name):
        return False

    def __setCruisingSpeedProperty(self, name):
        return False

    def __setCruisingAltitudeProperty(self, name):
        return False
