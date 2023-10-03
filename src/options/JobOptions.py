
class JobOptions:

    def __init__(self, clearance_height: float = 10, lead_in: float = 0.25):
        if clearance_height <= 0:
            raise ValueError('Clearance height must be greater than zero')
        if lead_in < 0:
            raise ValueError('Lead-in must be positive or zero')

        self._clearance_height = clearance_height
        self._lead_in = lead_in

    clearance_height = property(fget=lambda self: self._clearance_height)
    lead_in = property(fget=lambda self: self._lead_in)
