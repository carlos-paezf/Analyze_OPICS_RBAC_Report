import warnings

from modules import Analyze_RUGAR, Analyze_RBAC, Compare_Data


warnings.filterwarnings(
    action="ignore",
    category=UserWarning, 
    module="openpyxl"
)


if __name__ == '__main__':
    opics_data = Analyze_RUGAR().users_info

    rbac_data = Analyze_RBAC().rbac_data

    Compare_Data(opics_data, rbac_data).compare_users_in_reports()