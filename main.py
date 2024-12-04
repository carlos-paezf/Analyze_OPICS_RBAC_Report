import warnings

from modules import Analyze_RBAC, Analyze_RUGAR, App_GUI, Compare_Data

warnings.filterwarnings(
    action="ignore",
    category=UserWarning, 
    module="openpyxl"
)


if __name__ == '__main__':
    rugar = Analyze_RUGAR()
    rbac = Analyze_RBAC()
    compare_data = Compare_Data(rugar, rbac)

    App_GUI(compare_data).mainloop()
