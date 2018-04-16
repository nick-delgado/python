

class Aircraft():
    def __init__(self, tailnumber):
        self.reg = tailnumber
        self._name = None
        self._cruising_speed = None
        self._cruising_altitude = None
        self._weight = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value = None):
        #check if it is the correct length
        self._name = value

    @property
    def cruising_speed(self):
        return self._cruising_speed

    @cruising_speed.setter
    def cruising_speed(self, value = None):
        #check if it is the correct length
        self._cruising_speed = value


    @property
    def cruising_altitude(self):
        return self._cruising_altitude

    @cruising_altitude.setter
    def cruising_altitude(self, value = None):
        #check if it is the correct length
        self._cruising_altitude = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value = None):
        #check if it is the correct length
        self._weight = value
