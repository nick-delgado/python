

class Aircraft():
    def __init__(self, tailnumber):
        self.reg = tailnumber
        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value = ''):
        #check if it is the correct length
        self._name = value

    def setProperty(self, which, value):
        #Right now all these functions are being called
        switcher = {
                'name'  : self.__setNameProperty(value),
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
