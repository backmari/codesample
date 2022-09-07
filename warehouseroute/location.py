from abc import ABC, abstractmethod


class Location(ABC):
    '''
    Abstract base class for warehouse locations.

    Locations represent the names of locations in a warehouse
    '''

    @abstractmethod
    def __init__(self, mha: str):
        ''' Constuctor

        Parameters
        ----------
        mha : string, material handling area
        '''
        self.mha = mha

    @abstractmethod
    def __str__(self):
        return "MHA " + self.mha


class AreaLocation(Location):
    '''
    Class to represent area locations

    An area location is identified by the name of the material handling area
    (mha). This can be used e.g. for named inbound areas, or designated floor
    areas where goods are placed temporarily after being unloaded from a truck.
    '''

    def __init__(self, mha: str):
        '''
        Constructor, extends the Location constructor

        Parameters
        ----------
        mha : string, material handling area
        '''
        super().__init__(mha)

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        if isinstance(other, AreaLocation):
            return self.mha == other.mha
        else:
            return False


class RackLocation(Location):
    '''
    Class to represent rack locations.

    A rack location is identified by the material handling area (mha), rack ID,
    horizontal coordinate ID, and vertical coordinate ID. This class can be
    used for locations in storage racks.
    '''

    def __init__(self, mha: str, rack: str, horcoor: str, vercoor: str):
        '''
        Constructor, extends the Location constructor

        Parameters
        ----------
        mha : str, material handling area
        rack: str, rack identifier
        horcoor: str, horizontal coordinate
        vercoor: str, vertical coordinate
        '''
        super().__init__(mha)
        self.rack = rack
        self.horcoor = horcoor
        self.vercoor = vercoor

    def __eq__(self, other):
        if isinstance(other, RackLocation):
            return self.mha == other.mha and \
                self.rack == other.rack and \
                self.horcoor == other.horcoor and \
                self.vercoor == other.vercoor
        else:
            return False

    def __str__(self):
        return "MHA " + self.mha + " rack " + self.rack + \
            " x " + self.horcoor + " y " + self.vercoor


class DeepStackingLocation(Location):
    '''
    Class to represent deep stacking locations.

    A deep stacking location is identified by the material handling area (mha),
    horizontal coordinate ID, and vertical coordinate ID. This class can be
    used for locations in deep stacking areas, where goods are stored in a
    queue either vertically or horizontally and only the last unit can be
    accessed.
    '''

    def __init__(self, mha: str, horcoor: str, vercoor: str):
        '''
        Constructor, extends the Location constructor

        Parameters
        ----------
        mha : str, material handling area
        horcoor: str, horizontal coordinate
        vercoor: str, vertical (depth) coordinate
        '''
        super().__init__(mha)
        self.horcoor = horcoor
        self.vercoor = vercoor

    def __eq__(self, other):
        if isinstance(other, DeepStackingLocation):
            return self.mha == other.mha and \
                self.horcoor == other.horcoor and \
                self.vercoor == other.vercoor
        else:
            return False

    def __str__(self):
        return "MHA " + self.mha + " x " + self.horcoor + \
            " y " + self.vercoor
