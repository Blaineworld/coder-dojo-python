INFINITY = float("inf")

class KitchenError(Exception):
    pass

class Thing:
    __container = False

    @property
    def available(self):
        if not self.__container:
            return False
        return not self.__container.closed

    @property
    def netWeight(self):
        return self.weight

    @property
    def state(self):
        return "generic"

    @property
    def volume(self):
        return 2

    @property
    def weight(self):
        return 5

    def update(self):
        return self # Chainable

    def __str__(self):
        return type(self).__name__ + ": " + self.state

    def __repr__(self):
        return "<" + str(self) + ">"

class Appliance(Thing):
    @property
    def weight(self):
        return 1000

class ContainerAppliance(Appliance):
    @property
    def capacity(self):
        return 50

    @property
    def closed(self):
        return False

    @property
    def fullness(self):
        x = 0
        for item in self.__contents:
            x += item.volume
        return x

    @property
    def itemCapacity(self):
        return 3

    @property
    def netWeight(self):
        x = self.weight
        for item in self.__contents:
            x += item.weight
        return x

    @property
    def state(self):
        self.update()
        x = str(len(self.__contents)) + " item"
        if x != "1":
            x += "s"
        return x

    @property
    def volume(self):
        return 60

    @property
    def weight(self):
        return 20000

    def insert(self, item):
        if not self.available:
            raise KitchenError("The container is not available.")
        if not isinstance(item, Thing):
            raise KitchenError("Only things can go in containers.")
        if self.closed:
            raise KitchenError("The container is closed.")
        if item == self:
            raise KitchenError("The item is the container.")
        if item._Thing__container:
            raise KitchenError("The item is already in a container.")
        if self.fullness + item.volume > self.capacity or (self.itemCapacity <= len(self.__contents)):
            raise KitchenError("The item will not fit.")
        self.__contents.append(item)
        item._Thing__container = self
        return self # Chainable

    def update(self):
        return self # Chainable

    def __init__(self):
        self.__contents = []

class ContainerApplianceWithDoor(ContainerAppliance):
    __closed = True

    @property
    def closed(self):
        return self.__closed

    @property
    def state(self):
        self.update()
        x = str(len(self.__contents)) + " item"
        if x != "1 item":
            x += "s"
        if self.__closed:
            x += ", shut"
        else:
            x += ", open"
        return x

    def close(self):
        if not self.available:
            raise KitchenError("The container is not available.")
        if self.__closed:
            raise KitchenError("The container is already shut.")
        self.__closed = True
        return self # Chainable

    def open(self):
        if not self.available:
            raise KitchenError("The container is not available.")
        if not self.__closed:
            raise KitchenError("The container is already open.")
        self.__closed = False
        return self # Chainable

    def __init__(self):
        self.__contents = []
        self._ContainerAppliance__contents = self.__contents

class Microwave(ContainerApplianceWithDoor):
    @property
    def capacity(self):
        return 60

    @property
    def itemCapacity(self):
        return 50

    @property
    def volume(self):
        return 75

    @property
    def weight(self):
        return 25000

class SmallMicrowave(Microwave):
    @property
    def capacity(self):
        return 25

    @property
    def volume(self):
        return 30

    @property
    def weight(self):
        return 12500
