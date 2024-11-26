from measure_run_time import measure_run_time

from utils import array_diff, RBAC_Keys, OPICS_Keys, RBAC_Profile_Group_Keys
from .analyzer_rbac import Analyze_RBAC
from .analyzer_rugar import Analyze_RUGAR


class Compare_Data():
    def __init__(self, rugar: Analyze_RUGAR, rbac: Analyze_RBAC):
        self.rugar = rugar
        self.rbac = rbac
        self.opics_data = self.rugar.users_info
        self.rbac_data = self.rbac.rbac_data


    @measure_run_time
    def compare_users_in_reports(self) -> tuple[list, list]:
        """
        This function compares users in two reports and returns lists of users that are present in one
        report but not in the other.
        :return: The function `compare_users_in_reports` returns a tuple containing two lists. The first
        list contains users from the OPICS data that are not present in the RBAC data, and the second
        list contains users from the RBAC data that are not present in the OPICS data.
        """
        opics_users = [i[OPICS_Keys.USER] for i in self.opics_data]
        rbac_users = [i["usuario_opics"] for i in self.rbac_data[RBAC_Keys.PROFILES_USERS]]

        opics_not_in_rbac = array_diff(sorted(opics_users), sorted(rbac_users))
        rbac_not_in_opics = array_diff(sorted(rbac_users), sorted(opics_users))

        return opics_not_in_rbac, rbac_not_in_opics
    

    @measure_run_time
    def compare_users_groups(self):
        """
        The function `compare_users_groups` compares user profiles between two datasets and identifies
        any differences in group memberships.
        :return: The `compare_users_groups` method returns a list of dictionaries, where each
        dictionary represents the differences between user profiles in the `rbac_data` and `opics_data`.
        Each dictionary contains the following keys:
        - "rbac_user": the user ID from the RBAC data
        - "opics_user": the user ID from the Opics data
        - "rbac_profile": the profile
        """
        opics_users_map = {user["usuario_opics"]: user for user in self.opics_data}
        diff = []
        
        for rbac_user in self.rbac_data[RBAC_Keys.PROFILES_USERS]:
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
                        "opics_user": opics_user[OPICS_Keys.USER],
                        "rbac_profile": rbac_user["perfil"],
                        "rbac_groups_not_in_opics_groups": rbac_groups_diff,
                        "opics_groups_not_in_rbac_groups": opics_groups_diff
                    })

        return diff
    

    def compare_profiles_groups(self):
        diff = []
        profiles_groups = self.rbac.define_profile_groups()

        profiles_map = {
            profile[RBAC_Profile_Group_Keys.PROFILE]: {
                RBAC_Profile_Group_Keys.GROUPS: profile[RBAC_Profile_Group_Keys.GROUPS] 
            }
            for profile in profiles_groups
        }
        
        rbac_users_profiles = self.rbac_data[RBAC_Keys.PROFILES_USERS]

        rbac_profiles = []
        
        for i in self.rbac_data[RBAC_Keys.PROFILES]:
            profile = i[RBAC_Profile_Group_Keys.PROFILE]

            profile_groups = profiles_map.get(profile)

            if not profile_groups:
                print(f"El perfil '{profile}' no tiene grupos asignados")
                continue
            
            users = []

            # for j in 

            rbac_profiles.append({
                RBAC_Profile_Group_Keys.PROFILE: profile,
                RBAC_Profile_Group_Keys.GROUPS: profile_groups
            })
        # for rbac_user in self.rbac_data[RBACKeys.PROFILES_GROUPS]: