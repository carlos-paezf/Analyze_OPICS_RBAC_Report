import warnings

from modules import Analyze_RUGAR, Analyze_RBAC, Compare_Data


warnings.filterwarnings(
    action="ignore",
    category=UserWarning, 
    module="openpyxl"
)


if __name__ == '__main__':
    rugar = Analyze_RUGAR()
    rbac = Analyze_RBAC()
    compare_data = Compare_Data(rugar, rbac)

    [opics_not_in_rbac, rbac_not_in_opics] = compare_data.compare_users_in_reports()
    reports_diff = compare_data.compare_users_groups()
    compare_data.compare_profiles_groups()

    # print("opics_not_in_rbac: ", opics_not_in_rbac)
    # print("rbac_not_in_opics: ", rbac_not_in_opics)
    # print("reports_diff: ", reports_diff)
