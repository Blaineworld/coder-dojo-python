version = "alpha 1" # The version number of this software.
timeScale = 30 # PyKitchen seconds for every real second.

def initialize():
    # For all the instances where we need them.
    INFINITY = float("Inf")
    NAN = float("NaN")

    # Can't have you messing yourself up!
    global initialize
    del initialize

    # Root Classes
    global KitchenError, Thing, Appliance, ContainerAppliance, ContainerApplianceWithDoor, Food, Meat

    # Specific Appliances
    global MicrowaveOven, Microwave, MiniMicrowaveOven, MiniMicrowave, Toaster

    # Specific Foods
    global ChickenNugget

    class KitchenError(Exception):
        # An error in the kitchen.
        pass

    class Thing:
        # A PyKitchen thing.
        __container = False

        @property
        def available(self):
            # Can we reach the thing?
            if not self.__container:
                return True
            return not self.__container.shut

        @property
        def netWeight(self):
            # What is the total weight of this thing?
            return self.weight

        @property
        def state(self):
            # What is the state of this thing?
            return "generic"

        @property
        def volume(self):
            # What is the volume of this thing in liters?
            return 2

        @property
        def weight(self):
            # What is the weight of this thing in grams?
            return 5

        def update(self):
            # Update the state of this thing.
            return self # Chainable

        def __str__(self):
            return type(self).__name__ + ": " + self.state

        def __repr__(self):
            return "<" + str(self) + ">"

    class Appliance(Thing):
        # A PyKitchen appliance.
        @property
        def weight(self):
            return 1000

    E_cito = "Can't insert an object " # Error shorthand.
    E_crto = "Can't to remove an object " # Error shorthand.
    class ContainerAppliance(Appliance):
        # A PyKitchen container appliance.
        @property
        def capacity(self):
            # What is the internal volume of this container?
            return 50

        @property
        def shut(self):
            # Is this container shut?
            return False

        @property
        def fullness(self):
            # What is the total volume of this container's contents?
            x = 0
            for item in self.__contents:
                x += item.volume
            return x

        @property
        def itemCapacity(self):
            # How many items can go in this container?
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
            return 10000

        def insert(self, item):
            # Put something in.
            if not isinstance(item, Thing):
                raise KitchenError(E_cito + "that's not a Thing!")
            if not item.available:
                raise KitchenError(E_cito + "that's unavailable!")
            if not self.available:
                raise KitchenError(E_cito + "into an unavailable container!")
            if self.shut:
                raise KitchenError(E_cito + "into a shut container!")
            if item == self:
                raise KitchenError(E_cito + "into itself!")
            if item._Thing__container:
                raise KitchenError(E_cito + "that's already in a container!")
            if self.fullness + item.volume > self.capacity or (self.itemCapacity <= len(self.__contents)):
                raise KitchenError(E_cito + "where it won't fit!")
            self.__contents.append(item)
            item._Thing__container = self
            return self # Chainable

        def remove(self, item = 0):
            # Take something out.
            if not self.available:
                raise KitchenError(E_crto + "from an unavailable container!")
            if item == self:
                raise KitchenError(E_crto + "from itself!")
            l = len(self.__contents)
            if self.shut:
                raise KitchenError(E_crto + "from a shut container!")
            if not l:
                raise KitchenError(E_crto + "from an empty container!")
            if isinstance(item, Thing):
                try:
                    self.__contents.pop(self.__contents.index(item))
                    item._Thing__container = False
                    return item
                except ValueError:
                    raise KitchenError(E_crto + "from a container it isn't in!")
            elif isinstance(item, int):
                if item < 1:
                    item = self.__contents.pop(l - 1)
                    item._Thing__container = False
                    return item
                else:
                    if --item < l:
                        item = self.__contents.pop(l - item)
                        item._Thing__container = False
                        return item
                    else:
                        raise KitchenError("The container doesn't have " + str(item) + " items, only " + str(l) + "!")
            else:
                raise KitchenError("The value given is of type `" + type(item).__name__ + "` instead of number or Thing!")

        def update(self):
            return self # Chainable

        def __init__(self):
            self.__contents = []

    E_tci = "The container is " # Error shorthand.
    class ContainerApplianceWithDoor(ContainerAppliance):
        # A container appliance with a door.
        __shut = True

        @property
        def shut(self):
            return self.__shut

        @property
        def state(self):
            self.update()
            x = str(len(self.__contents)) + " item"
            if x != "1 item":
                x += "s"
            if self.__shut:
                x += ", shut"
            else:
                x += ", open"
            return x

        def open(self):
            # Attempt to open the door.
            if not self.available:
                raise KitchenError(E_tci + "unavailable!")
            if not self.__shut:
                raise KitchenError(E_tci + "already open!")
            self.__shut = False
            return self # Chainable

        def close(self):
            # Attempt to close the door.
            if not self.available:
                raise KitchenError(E_tci + "unavailable!")
            if self.__shut:
                raise KitchenError(E_tci + "is already shut!")
            self.__shut = True
            return self # Chainable

        def __init__(self):
            self._ContainerAppliance__contents = self.__contents = []

    class MicrowaveOven(ContainerApplianceWithDoor):
        # A microwave oven.
        __state = 0

        # Properties
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

        def press(self, inputs):
            # Press one or more buttons.
            return self # Chainable

        def read(self):
            # Read the text on the screen.
            self.update()
            if self.__state == 0:
                # idle
                return "00:00   " # haven't fully implemented time
            elif self.__state == 1:
                # entering time
                return "00:00   "
            elif self.__state == 2:
                # cooking / timing
                return "00:00   "
            elif self.__state == 3:
                # waiting
                return "RE AD Y "
            return "ER RO R "
    Microwave = MicrowaveOven

    class MiniMicrowaveOven(MicrowaveOven):
        # A wittwe bitty micwowave oven.
        @property
        def capacity(self):
            return 25

        @property
        def volume(self):
            return 30

        @property
        def weight(self):
            return 12500
    MiniMicrowave = MiniMicrowaveOven

initialize()
