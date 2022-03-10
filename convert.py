import json
from os.path import exists
from datetime import date, timedelta
start_date = date(2020, 1, 1)
end_date = date(2022, 1, 1)
delta = timedelta(days=1)

import csv
with open('data.csv', 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    w.writerow(["date"] + list(range(1, 25)))

    while start_date <= end_date:
        day_str = start_date.strftime("%m%d%Y")
        day_file = f"{day_str}.json"
        if exists(day_file):
            data = json.loads(open(day_file).read())

            fields = [day_str] + [None] * 24
            for row in data['data']['HourlyUsage']['data']:
                print(row['hour'], row['kwhActual'])
                fields[row['hour']] = row['kwhActual']
            print(fields)
            w.writerow(fields)
            # quit()


        start_date += delta