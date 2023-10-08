import numpy as np
from PV_results import PV


if __name__ == '__main__':

    # create a PV object
    pv = PV()

    # file name
    csv_file = 'Lastkurven_Wärmepumpen.csv'

    # load the file
    pv.load(csv_file)

    # list dates
    dates = pv._list_dates()

    # calculate total consumption for every day
    consumptions_1 = [pv.get_total(pv._get_day(d), 'MP071') for d in dates]

    # print date and total consumption for this date
    for d, consumption in zip(dates, consumptions_1):
        print(d, consumption)

