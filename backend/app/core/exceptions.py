class PlantMindException(Exception):
    """Base exception for PlantMind."""
    pass


class EquipmentNotFoundException(PlantMindException):
    pass


class PITagNotFoundException(PlantMindException):
    pass


class ProcedureNotFoundException(PlantMindException):
    pass
