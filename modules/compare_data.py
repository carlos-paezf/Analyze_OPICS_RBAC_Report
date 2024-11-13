from utils import measure_run_time


class Compare_Data():
    def __init__(self, opics_data: dict, rbac_data: dict):
        self.opics_data = opics_data
        self.rbac_data = rbac_data


    @measure_run_time
    def compare_users(self):
        pass