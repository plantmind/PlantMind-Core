from app.models.equipment import Equipment


class EquipmentService:
    def __init__(self):
        self.equipment = []

    def add_equipment(self, equipment: Equipment):
        self.equipment.append(equipment)
        return equipment

    def get_all_equipment(self):
        return self.equipment

    def get_equipment(self, tag: str):
        for equipment in self.equipment:
            if equipment.tag == tag:
                return equipment
        return None
