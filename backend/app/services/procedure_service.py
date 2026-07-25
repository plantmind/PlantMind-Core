class ProcedureService:
    def __init__(self):
        self.procedures = []

    def add_procedure(self, procedure):
        self.procedures.append(procedure)
        return procedure

    def get_all_procedures(self):
        return self.procedures

    def get_procedure(self, procedure_id):
        for procedure in self.procedures:
            if procedure.procedure_id == procedure_id:
                return procedure
        return None
