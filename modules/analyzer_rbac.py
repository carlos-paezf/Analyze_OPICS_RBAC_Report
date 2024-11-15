import pandas as pd
from unidecode import unidecode

from utils import RBACKeys, measure_run_time, normalize_str


class Analyze_RBAC():
    def __init__(self):
        self.rbac_path = "./RBAC Plantilla Aplicaciones OPICS.xlsx"

        self.sheet_names = []

        self.rbac_data = {
            RBACKeys.GOVERNMENT: [],
            RBACKeys.GROUP_TRANSACTION: [],
            RBACKeys.GROUPS: [],
            RBACKeys.PROFILES_GROUPS: [],
            RBACKeys.PROFILES_USERS: [],
            RBACKeys.PROFILES: []
        }
        

        self.analyze_rbac_report()

       
    @measure_run_time
    def analyze_rbac_report(self):
        """
        The function `analyze_rbac_report` reads RBAC information, converts sheets to JSON format, and
        likely performs further analysis.
        """
        raw_data = self.read_rbac_info()
        self.convert_sheets_to_json(raw_data)
        self.define_profile_groups()

    
    def read_rbac_info(self) -> pd.ExcelFile:
        """
        This function reads RBAC information from an Excel file specified by the `rbac_path` attribute.
        :return: An instance of `pd.ExcelFile` containing the RBAC information from the file located at
        `self.rbac_path`.
        """
        return pd.ExcelFile(self.rbac_path)
    
    
    def convert_sheets_to_json(self, raw_data: pd.ExcelFile) -> None:
        """
        The function `convert_sheets_to_json` reads data from an Excel file, converts it to JSON format,
        and saves each sheet as a separate JSON file.
        
        :param raw_data: The `raw_data` parameter in the `convert_sheets_to_json` function is expected
        to be an instance of `pd.ExcelFile`, which represents an Excel file. This parameter is used to
        read data from the Excel file and convert it into JSON format
        :type raw_data: pd.ExcelFile
        """
        for sheet in raw_data.sheet_names:
            dataframe = raw_data.parse(sheet)
            json_data = self.dataframe_to_json_compatible(dataframe)
            
            self.rbac_data[normalize_str(sheet)] = json_data
            
    
    def dataframe_to_json_compatible(self, dataframe: pd.DataFrame) -> list[dict]:
        """
        The function `dataframe_to_json_compatible` converts a pandas DataFrame to a list of
        dictionaries with string values normalized and newline characters replaced.
        
        :param dataframe: The `dataframe_to_json_compatible` function takes a pandas DataFrame as input
        and converts it into a list of dictionaries that are compatible with JSON format. The function
        first replaces any NaN values in the DataFrame with `None`. Then, it iterates over each row in
        the DataFrame, converts the keys
        :type dataframe: pd.DataFrame
        :return: The function `dataframe_to_json_compatible` returns a list of dictionaries where each
        dictionary represents a row in the input DataFrame `dataframe`. The keys in the dictionaries are
        normalized (converted to lowercase and spaces replaced with underscores), and the values are
        processed to replace newline characters with spaces if the value is a string. The final output
        is a list of dictionaries that are compatible with JSON serialization.
        """
        dataframe = dataframe.where(pd.notnull(dataframe), None)

        return [
            {
                normalize_str(key): (unidecode(value.replace('\n', ' ')) if isinstance(value, str) else value)
                for key, value in row.items()
            }
            for row in dataframe.to_dict(orient="records")
        ]
    

    def define_profile_groups(self) -> list[dict]:
        """
        This Python function defines profile groups based on input data and returns a list of
        dictionaries representing profiles and their associated groups.
        :return: The function `define_profile_groups` returns a list of dictionaries where each
        dictionary represents a profile and its associated groups.
        """
        raw_profiles_groups = self.rbac_data[RBACKeys.PROFILES_GROUPS]

        profiles_groups = []

        print(len(raw_profiles_groups))
        
        for i in raw_profiles_groups:
            profile = i["perfil"]
            
            profile_exists = next(
                (
                    profile_group 
                    for profile_group in profiles_groups 
                    if profile_group["profile"] == profile
                ), 
                None
            )

            group = i["grupos"]

            if not profile_exists:
                profiles_groups.append({"profile": profile, "groups": [group]})
            else:
                if group not in profile_exists["groups"]:
                    profile_exists["groups"].append(group)

        return profiles_groups