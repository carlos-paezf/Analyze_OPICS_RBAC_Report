import pandas as pd

from utils import measure_run_time, create_folders, normalize_str, open_csv_file, saves_json_file, CSV_PATH, JSON_PATH


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
        create_folders()
        data = self.read_rbac_info()
        self.convert_to_json(data)

    
    def read_rbac_info(self) -> pd.ExcelFile:
        data = pd.ExcelFile(self.rbac_path)
        self.sheet_names = data.sheet_names
        return data

    
    def convert_to_json(self, data: pd.ExcelFile) -> None:
        for sheet in self.sheet_names:
            dataframe = data.parse(sheet)
            dataframe.to_csv(f"{CSV_PATH}/{sheet}.csv", index=False)

            file, csv_reader = open_csv_file(f"{CSV_PATH}/{sheet}.csv")

            data = [
                {
                    normalize_str(key): value
                    for key, value in row.items()
                }
                for row in csv_reader
            ]

            file.close()

            saves_json_file(f"{JSON_PATH}/{sheet}.json", data)
