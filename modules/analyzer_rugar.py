import re

from pathlib import Path
from utils import measure_run_time



class Analyze_RUGAR():
    def __init__(self):
        self.phrases_to_discard = [
            '*', 'Users Group Access Report', 'System date', 
            'Branch processing date', 'Alternate Oper ID', 
            'Department', 'Transaction Authority'
        ]

        self.report_date = ""
        # self.report_path = f"R:\\SSETPI\\Proyectos_SSETPI\\Perfiles OPICS\\Reportes OPICS\\"
        self.report_path = f".\\"
        
        self.users_info = {}

        self.analyze_rugar_report()


    
    def get_users_info(self) -> dict:
        """
        This function returns the users' information stored in the object.
        :return: The method `get_users_info` is returning the `users_info` attribute of the object.
        """
        return self.users_info


    @measure_run_time
    def analyze_rugar_report(self) -> None:
        """
        The `analyze_report` function processes a report by setting the date and path, extracting and
        cleaning lines, depuring data, and printing user information.
        """
        self.set_report_date()
        self.set_report_path()

        original_lines = self.extract_lines()
        clean_lines = self.clean_unnecessary_lines(original_lines)

        self.depure_data(clean_lines)


    def set_report_date(self) -> None:
        """
        The function `set_report_date` sets the report date attribute to a specific value.
        """
        # self.report_date = input("Por favor, ingrese la fecha del reporte a validar: ").strip()
        self.report_date = "20241030"

    
    def set_report_path(self) -> None:
        """
        The function `set_report_path` appends a specific string and the report date to the existing
        report path.
        """
        self.report_path = self.report_path + "R01RUGAR_" + self.report_date + ".rpt"

    
    def extract_lines(self) -> list[str]:
        """
        This Python function extracts lines from a specified file and returns them as a list of strings.
        :return: The `extract_lines` method returns a list of strings, which are the lines read from a
        file specified by the `report_path` attribute of the object.
        """
        report = Path(self.report_path)

        if not report.exists():
            raise Exception("Archivo no encontrado") 

        with report.open('r', encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    

    def check_phrase_in_specific_string(self, specific_string) -> list[str]:
        """
        The function `check_phrase_in_specific_string` returns a list of phrases from a given list that
        are found in a specific string.
        
        :param specific_string: The `check_phrase_in_specific_string` method takes a specific string as
        input and checks if any phrases from the `phrases_to_discard` list are present in that specific
        string. It then returns a list of all the phrases that are found in the specific string
        :return: A list of phrases from `self.phrases_to_discard` that are found in the
        `specific_string`.
        """
        return [s for s in self.phrases_to_discard if s in specific_string]
    

    def clean_unnecessary_lines(self, original_lines: list[str]) -> list[str]:
        """
        The function `clean_unnecessary_lines` processes a list of strings, removing unnecessary lines
        and modifying specific phrases before returning the cleaned lines.
        
        :param original_lines: The `clean_unnecessary_lines` method takes a list of strings
        `original_lines` as input and processes each line based on certain conditions. It removes any
        leading or trailing whitespaces from each line and then checks if a specific phrase is present
        in the line using the `check_phrase_in_specific_string`
        :type original_lines: list[str]
        :return: The function `clean_unnecessary_lines` returns a list of cleaned lines after processing
        the original lines based on certain conditions.
        """
        clean_lines = []

        for line in original_lines:
            line = line.strip()

            if not self.check_phrase_in_specific_string(line):
                if "(IAUD)" in line:
                    line = re.sub(r'\s+', '-', line)
                elif "Phone" in line:
                    line = "Groups:"
                
                clean_lines.append(f"{line} ")

        return clean_lines
    

    def depure_data(self, clean_lines: list[str]) -> None:
        """
        The function `depure_data` processes a list of clean lines to extract user data and then calls
        another method to define user information.
        
        :param clean_lines: The `clean_lines` parameter in the `depure_data` method is a list of strings
        that contain the data to be processed. The method processes these lines to extract user
        information
        :type clean_lines: list[str]
        """
        data_string = re.sub(r'[\n\x0c]', ' ', ''.join(clean_lines))
        users_data_raw = data_string.split('OperatorID: ')[1::]

        for user in users_data_raw:
            self.define_user_info(user)
    
    def define_user_info(self, data: str) -> None:
        """
        This Python function extracts and stores user information from a given string data.
        
        :param data: The `define_user_info` function takes a string `data` as input. This string is
        expected to contain information about an operator, including their ID, name, and groups they
        belong to
        :type data: str
        """
        operator_id = data[0:4]
        operator_name = data.split("Operator Name: ")[1].strip().split("Groups:")[0].strip()
        groups = (
            data.split("Groups:")[1].strip().split(' ') 
            if data.split("Groups:")[1].strip() != "" 
            else []
        )

        if not operator_id in self.users_info:
            self.users_info[operator_id] = { "Nombre": "", "Grupos": []}

        self.users_info[operator_id]["Nombre"] = operator_name
        self.users_info[operator_id]["Grupos"] = self.users_info[operator_id]["Grupos"] + groups
