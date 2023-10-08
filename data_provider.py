import uuid
import os
from os.path import isfile, isdir
import pandas as pd

class GetData:


    def __init__(self):
        self._user_info = [
            {'uuid': '40607208359107', 'name': "André",
             'sharepoint': r"C:\Users\JumpStart\Hochschule Luzern\CC BE Docs - Documents\020 - "
                           r"Projects_ongoing\2022.HORIZON.ENFLATE - André Eggli"},
            {'uuid': '224391389380863', 'name': "Emre",
             'sharepoint': r"C:\Users\taavci\Hochschule Luzern\CC BE Docs - Documents\020 - "
                           r"Projects_ongoing\2022.HORIZON.ENFLATE - André Eggli"}
            # Add more users as needed
            # 'uuid': '225235268974597', 'name': "Elena"
        ]
        self.current_uuid = str(uuid.getnode())

    def _get_path(self, rest_of_dir_path):

        for user in self._user_info:
            if self.current_uuid == user['uuid']:
                print(f"UUID match found. Running on {user['name']}'s Laptop.")
                sharepoint = os.path.join(user['sharepoint'], rest_of_dir_path)

                if isdir(sharepoint):
                    print(f"Directory exists on {user['name']}'s Laptop.")
                    return sharepoint
                else:
                    print(f"Directory does not exist on {user['name']}'s Laptop.")
                break
        else:
            print("UUID match not found. This code is intended to run on specific laptops.")
        return None

    def _read_file(self, dir_path, file_name, sheet_name=None, encoding=None, names=None):
        # important: dir_path should be the path
        # after ...2022.HORIZON.ENFLATE - André Eggli

        #path = self._get_path(dir_path) # comment to work with a local file
        path = dir_path  # uncomment to work with a local file
        if path:
            print("Path:", path)
            file_path = os.path.join(path, file_name)
            if isfile(file_path):
                try:
                    if file_name.endswith('.xlsx'):
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                    elif file_name.endswith('.csv'):
                        df = pd.read_csv(file_path, encoding=encoding, names=names)
                    else:
                        print("Unsupported file format.")
                        return None

                    print("File Content:\n", df)
                    return df
                except Exception as e:
                    print("Error reading file:", e)
                    return None
            else:
                print("File not found.")
                return None
        else:
            print("No valid path.")
            return None

    def _get_data_for_contact_bundle_serial_letter(self):
        data = self._read_file(r"250 - Work packages\T4.1 Use case "
                        r"def\Pilotgebiet Komm\Serienbrief",
                        r'2023-08-07 Contact bundle serial letter.xlsx',
                        "Unfiltered")
        return data

    def _get_data_for_Leistung_Warmepunpen(self):

        data = self._read_file(r"250 - Work packages\T4.1 Use case "
                                        r"def\Model Pilotgebiet\Lastgang "
                                        r"Disaggregation\Aliunid Wärmepump",
                                        "Leistung_Wärmepumpen.csv",
                                        None,
                                        'ISO-8859-1')

        return data

    def _get_data_for_Allunid_eMobility(self):

        data = self._read_file( r"250 - Work packages\T4.1 Use case def"
                                        r"\Model Pilotgebiet\Lastgang Disaggregation"
                                        r"\Alunid eMobility",
                                        "Auswertung eMob.xlsx",
                                        "Tabelle1",
                                        'ISO-8859-1')

        return data

    def _get_data_for_LadeLeistung(self):

        data = self._read_file( r"250 - Work packages\T4.1 Use case def"
                                        r"\Model Pilotgebiet\Lastgang Disaggregation"
                                        r"\Alunid eMobility",
                                        "Ladeleistung_eMobility.xlsx",
                                        "Tabelle1",
                                        'ISO-8859-1')

        return data

    def _get_data_for_Schlüssel_HSLU(self):

        data = self._read_file( r"250 - Work packages\T4.1 Use case def"
                                        r"\Model Pilotgebiet\Lastgang Disaggregation"
                                        r"\Alunid eMobility",
                                        "Schlüssel_HSLU_aliunid.xlsx",
                                        "Tabelle1",
                                        'ISO-8859-1')

        return data

    def _get_data_for_anmeldung(self):

        data = self._read_file( r"250 - Work packages\T4.1 Use case "
                                r"def\Pilotgebiet Komm\Anmeldungen",
                                        "Anmeldungen 2023-08 v02.xlsx",
                                        "Sheet1")

        return data

    @staticmethod
    def get_data_path() -> str:
        current_file = os.path.abspath(__file__)
        data_directory = os.path.dirname(current_file)

        # Check if directory exists
        assert os.path.isdir(data_directory), f"Data directory not found at: {data_directory}"

        return data_directory

    def _get_data_photovoltaics(self):

        data = self._read_file( r".",
                                        "2023-09-05 Extract Aggregation results by SAM 2023-01 to 05.xlsx",
                                        "Sheet1")

        return data