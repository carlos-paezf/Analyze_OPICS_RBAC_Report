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

    opics_data = rugar.users_info
    rbac_data = rbac.rbac_data

    compare_data = Compare_Data(opics_data, rbac_data)
    [opics_not_in_rbac, rbac_not_in_opics] = compare_data.compare_users_in_reports()
    reports_diff = compare_data.compare_users_profiles()

    print("opics_not_in_rbac: ", opics_not_in_rbac)
    print("rbac_not_in_opics: ", rbac_not_in_opics)
    print("reports_diff: ", reports_diff)