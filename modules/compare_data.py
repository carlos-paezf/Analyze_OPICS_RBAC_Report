from utils import measure_run_time, array_diff, RBACKeys


class Compare_Data():
    def __init__(self, opics_data: dict, rbac_data: dict):
        self.opics_data = opics_data
        self.rbac_data = rbac_data


    @measure_run_time
    def compare_users_in_reports(self) -> tuple[list, list]:
        """
        This function compares users in two reports and returns lists of users that are present in one
        report but not in the other.
        :return: The function `compare_users_in_reports` returns a tuple containing two lists. The first
        list contains users from the OPICS data that are not present in the RBAC data, and the second
        list contains users from the RBAC data that are not present in the OPICS data.
        """
        opics_users = [i["usuario_opics"] for i in self.opics_data]
        rbac_users = [i["usuario_opics"] for i in self.rbac_data[RBACKeys.PROFILES_USERS]]

        opics_not_in_rbac = array_diff(sorted(opics_users), sorted(rbac_users))
        rbac_not_in_opics = array_diff(sorted(rbac_users), sorted(opics_users))

        return opics_not_in_rbac, rbac_not_in_opics
