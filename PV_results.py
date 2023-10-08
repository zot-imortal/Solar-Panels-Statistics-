import os
import uuid
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from scipy import signal
from typing import Iterable
import datetime
from data_provider import GetData


class PV:


    def __init__(self):
        self.columns =  ['Time', 
                         'Consumption_1', 'PVProd_1', 'Diff_1', 
                         'Consumption_2', 'PVProd_2', 'Diff_2', 
                         'Consumption_3', 'PVProd_3', 'Diff_3'
                         ]

        self.scales = {
                        '2019':- 0.59,
                        '2023': -1,
                        '2025': -0.59 * 2.5,
                        '2030': -0.59 * 3.87,
                        '2035': -0.59 * 7,
                        '2040': -0.59 * 9.55,
                        }


    def load(self, filename: str):
        # self.df = self._read_file(filename) # uncomment to read a file using _read_file function, comment next line
        self.df = self._read_file_using_data_provider(filename) # uncomment to read a file using _read_file_using_data_provider function, comment previous line


    def _read_file(self, filename) -> pd.DataFrame:
        filename = os.path.join(GetData.get_data_path(), filename)
        require_cols = [x for x in range(10)]
        df = pd.read_excel(filename, sheet_name='Sheet1', usecols=require_cols, skiprows=[0, 2])
        df.columns = self.columns # rename columns
        return df


    def _read_file_using_data_provider(self, filename: str) -> pd.DataFrame:
        dp = GetData()
        df = dp._get_data_photovoltaics()
        df.drop([0, 1], inplace=True) # remove 2 rows
        df.drop('Unnamed: 10', axis=1, inplace=True) # remove column 10 (with year 2019)
        df.columns = self.columns # rename columns
        return df


    def _get_day(self, input_date: datetime.date) -> pd.DataFrame:
        df_filtered = self.df[self.df['Time'].dt.date == input_date]
        return df_filtered
    
    def _get_period_data(self, start_date, end_date) -> pd.DataFrame:
        mask = (self.df['Time'] > start_date) & (self.df['Time'] <= end_date)
        df_filtered = self.df.loc[mask]
        return df_filtered

    def smooth(self, data: pd.DataFrame, column: str, method: str, window_length: int, order: int=5):
        if method == 'savgol':
            data[f'{column}_smoothed'] = signal.savgol_filter(data[column], window_length, order)
        elif method == 'median':
            data[f'{column}_smoothed'] = signal.medfilt(data[column], window_length)
        else:
            raise(Exception(f'No such method \'{method}\'.'))


    def _list_dates(self) -> Iterable:
        dates = pd.to_datetime(self.df['Time']).dt.date.unique()
        return dates


    def get_total(self, data: pd.DataFrame, column: str) -> float:
        values = data[column]
        total = np.sum(values)
        return total


    def scale(self, data: pd.DataFrame, column: str, year: int):
        year = str(year)
        if year not in self.scales:
            raise(Exception(f'No coefficient for year {year}.'))
        
        data[f'{column}_{year}'] = data[f'{column}'] * self.scales[year]


    def plot(self, data: pd.DataFrame, columns: Iterable, yaxis_title: str='kW', title: str='Results'):
        fig = go.Figure()
        for column in columns:
            fig.add_trace(go.Scatter(x=data['Time'], y=data[column],
                    mode='lines',
                    name=column))
        fig.update_layout(
            yaxis_title=yaxis_title,
            title=title,
        )
        fig.show()


if __name__ == '__main__':

    # create a PV object
    pv = PV()

    # file name
    exel_file = '2023-09-05 Extract Aggregation results by SAM 2023-01 to 05.xlsx'

    # load the file
    pv.load(exel_file)

    # list dates
    dates = pv._list_dates()

    # calculate total consumption for every day
    consumptions_1 = [pv.get_total(pv._get_day(d), 'Diff_1') for d in dates]
    production_1 = [pv.get_total(pv._get_day(d), 'PVProd_1') for d in dates]
    # print date and total consumption for this date
    # for d, consumption in zip(dates, consumptions_1):
    #     print(d, consumption)

    # maximum consumption
    max_consumption = np.max(consumptions_1)
    max_production = np.max(production_1)
    # day when consumption was maximum
    max_consumption_date = dates[np.argmax(consumptions_1)]
    max_production_date = dates[np.argmax(production_1)]

    # print max consumption and date
    print(max_consumption_date, max_consumption)
    print(max_production_date, max_production)

    # data for the day when consumption was maximum. A new dataframe is created from a slice of the current dataframe
    max_consumption_data = pv._get_day(max_consumption_date).copy()
    max_production_data = pv._get_day(max_production_date).copy()

    # smoothing values of power produced by PV_1. 
    # 'savgol' method is used. It can give negative values. 'median' method also can be used.
    pv.smooth(max_consumption_data, 'PVProd_1', 'savgol', 30)
    pv.smooth(max_production_data, 'PVProd_1', 'savgol', 30)

    # plotting produced power variations and smoothed values
    #pv.plot(max_consumption_data, ['PVProd_1', 'PVProd_1_smoothed'])

    # smoothing consumption data
    #pv.smooth(max_consumption_data, 'Consumption_1', 'median', 11)

    # plotting consumed power variations and smoothed values 
    #pv.plot(max_consumption_data, ['Consumption_1', 'Consumption_1_smoothed'])

    # scaling produced power for different years
    years = [2019, 2023, 2025, 2030, 2035, 2040]
    for year in years:
        pv.scale(max_production_data, 'PVProd_1_smoothed', year)

    # plotting produced power variations for different years
    pv.plot(max_production_data, ['PVProd_1_smoothed_2019', 
                                   'PVProd_1', 
                                   'PVProd_1_smoothed_2025', 
                                   'PVProd_1_smoothed_2030',
                                   'PVProd_1_smoothed_2035',
                                   'PVProd_1_smoothed_2040'
                                   ])
    # period data
    start_date = '2023-01-19'
    end_date = '2023-01-22'
    period_data = pv._get_period_data(start_date, end_date).copy()
    print(period_data)

    pv.smooth(period_data, 'PVProd_1', 'savgol', 45)
    period_data['PVProd_1_smoothed'] = signal.savgol_filter(period_data['PVProd_1_smoothed'], 12, 1)
    # scaling produced power for different years
    years = [2019, 2023, 2025, 2030, 2035, 2040]
    for year in years:
        pv.scale(period_data, 'PVProd_1_smoothed', year)

    period_data['PV_2023'] = period_data['PVProd_1']*-1
    # plotting produced power variations for different years
    pv.plot(period_data, ['PVProd_1_smoothed_2019', 
                            'PV_2023', 
                            'PVProd_1_smoothed_2025', 
                            'PVProd_1_smoothed_2030',
                            'PVProd_1_smoothed_2035',
                            'PVProd_1_smoothed_2040'
                            ],
                        'kW',
                        'PV Erzeugung')
    pv.plot(period_data, ['Consumption_1' 
                            ],
                        'kW',
                        'title') 
    pv.plot(period_data, ['Diff_1' 
                            ],
                        'kW',
                        'title') 
    

    

    
    