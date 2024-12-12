from measure_run_time import measure_run_time

from utils import array_diff, array_object_diff, RBAC_Keys, OPICS_Keys, RBAC_Profile_Group_Keys
from .analyzer_rbac import Analyze_RBAC
from .analyzer_rugar import Analyze_RUGAR


class Compare_Data():
    def __init__(self, rugar: Analyze_RUGAR, rbac: Analyze_RBAC):
        self.rugar = rugar
        self.rbac = rbac

    @measure_run_time
    def get_updated_data(self):
        """
        The function `get_updated_data` analyzes RBAC and Rugar reports and returns the users'
        information and RBAC data.
        :return: The `get_updated_data` method returns a list containing the `opics_data` and
        `rbac_data`. The `opics_data` is obtained from the `users_info` attribute of the `rugar` object,
        and the `rbac_data` is obtained from the `rbac_data` attribute of the `rbac` object.
        """
        self.rbac.analyze_rbac_report()
        self.rugar.analyze_rugar_report()

        opics_data = self.rugar.users_info
        rbac_data = self.rbac.rbac_data

        return [opics_data, rbac_data]


    def compare_users_in_reports(self) -> tuple[list, list]:
        """
        The function `compare_users_in_reports` compares users between two data sets and returns the
        differences.
        :return: The function `compare_users_in_reports` returns a tuple containing two lists:
        `opics_not_in_rbac` and `rbac_not_in_opics`. The first list contains the differences between the
        `opics_data` and `rbac_data[RBAC_Keys.PROFILES_USERS]` based on the `OPICS_Keys.USER` key. The
        second list contains the differences between the
        """
        [opics_data, rbac_data] = self.get_updated_data()

        opics_not_in_rbac = array_object_diff(opics_data, rbac_data[RBAC_Keys.PROFILES_USERS], OPICS_Keys.USER) 
        rbac_not_in_opics = array_object_diff(rbac_data[RBAC_Keys.PROFILES_USERS], opics_data, RBAC_Keys.USER)

        return opics_not_in_rbac, rbac_not_in_opics
    

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
        [opics_data, rbac_data] = self.get_updated_data()

        opics_users_map = {user[OPICS_Keys.USER]: user for user in opics_data}
        diff = []
        
        for rbac_user in rbac_data[RBAC_Keys.PROFILES_USERS]:
            rbac_user_id = rbac_user[RBAC_Keys.USER]
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
                        "rbac_groups": rbac_groups,
                        "rbac_groups_not_in_opics_groups": rbac_groups_diff,
                        "opics_groups": opics_groups,
                        "opics_groups_not_in_rbac_groups": opics_groups_diff,
                    })

        return diff
    

    def compare_profiles_groups(self):
        [opics_data, rbac_data] = self.get_updated_data()

        diff = []
        profiles_groups = self.rbac.define_profile_groups()

        profiles_map = {
            profile[RBAC_Profile_Group_Keys.PROFILE]: {
                RBAC_Profile_Group_Keys.GROUPS: profile[RBAC_Profile_Group_Keys.GROUPS] 
            }
            for profile in profiles_groups
        }
        
        rbac_users_profiles = rbac_data[RBAC_Keys.PROFILES_USERS]
        print(rbac_users_profiles)

        rbac_profiles = []
        
        for i in rbac_data[RBAC_Keys.PROFILES]:
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