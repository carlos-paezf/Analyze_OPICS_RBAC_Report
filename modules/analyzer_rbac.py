import pandas as pd

from unidecode import unidecode
from utils import measure_run_time, recreate_folders, normalize_str, open_csv_file, saves_json_file, CSV_PATH, JSON_PATH


class Analyze_RBAC():
    def __init__(self):
        self.rbac_path = "./RBAC Plantilla Aplicaciones OPICS.xlsx"

        self.sheet_names = []

        self.rbac_data = {
            "profiles_users": {},
            "profiles": {},
            "profiles_groups": {},
            "groups": {},
            "groups_transaction": {},
            "government": {},
        }


        self.analyze_rbac_report()

       
    @measure_run_time
    def analyze_rbac_report(self):
        """
        The function `analyze_rbac_report` recreates folders, reads RBAC information, and converts
        sheets to JSON format.
        """
        recreate_folders()
        raw_data = self.read_rbac_info()
        self.convert_sheets_to_json(raw_data)

    
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
            saves_json_file(f"{JSON_PATH}/{sheet}.json", json_data)
            
    
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
                normalize_str(key): (value.replace('\n', ' ') if isinstance(value, str) else value)
                for key, value in row.items()
            }
            for row in dataframe.to_dict(orient="records")
        ]
