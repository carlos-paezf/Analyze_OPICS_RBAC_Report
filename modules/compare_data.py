from measure_run_time import measure_run_time

from utils import RBACKeys, array_diff


class Compare_Data():
    def __init__(self, opics_data: list[dict], rbac_data: dict):
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
    

    @measure_run_time
    def compare_users_profiles(self):
        opics_users_map = {user["usuario_opics"]: user for user in self.opics_data}
        diff = []
        
        for rbac_user in self.rbac_data[RBACKeys.PROFILES_USERS]:
            rbac_user_id = rbac_user["usuario_opics"]
            opics_user = opics_users_map.get(rbac_user_id)

            if opics_user:
                rbac_groups = sorted(rbac_user["grupos"])
                opics_groups = sorted(opics_user["grupos"])

                rbac_groups_diff = array_diff(rbac_groups, opics_groups)
                opics_groups_diff = array_diff(opics_groups, rbac_groups)

                if rbac_groups_diff or opics_groups_diff:
                    diff.append({
                        "rbac_user": rbac_user_id,
                        "opics_user": opics_user["usuario_opics"],
                        "rbac_profile": rbac_user["perfil"],
                        "rbac_groups_not_in_opics_groups": rbac_groups_diff,
                        "opics_groups_not_in_rbac_groups": opics_groups_diff
                    })
        
        return diff
