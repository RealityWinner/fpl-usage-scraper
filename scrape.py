import secrets
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get('https://www.fpl.com/my-account/residential-dashboard.html#energy-usage-tab')

def closeBrowser():
    driver.close()
import atexit
atexit.register(closeBrowser)


from selenium.webdriver.support.ui import WebDriverWait
def wait(ele_id):
    def f(driver):
        ele = driver.find_element(By.ID, ele_id)
        if ele and ele.is_displayed():
            return ele
    return WebDriverWait(driver, 10).until(f)



# Login page
wait('core_view_form_ValidationTextBox_0').send_keys(secrets.username)
wait('core_view_form_ValidationTextBox_1').send_keys(secrets.password)
wait('core_view_form_Button_0').click()


# Dashboard page
wait('energyCntrHourly')#.click()

# Navigate through all days
wait('navigator_left')#.click()



def scrape_day(day):
    return driver.execute_script(f'''
return $.ajax({{
  url: "https://www.fpl.com/dashboard-api/resources/account/{secrets.account}/energyService/{secrets.account}",
  type: "POST",
  data: JSON.stringify({{"status":2,"channel":"WEB","amrFlag":"Y","accountType":"RESIDENTIAL","revCode":"1","premiseNumber":"{secrets.premise}","meterNo":"{secrets.meter}","projectedBillFlag":false,"billComparisionFlag":false,"monthlyFlag":false,"frequencyType":"Hourly","lastBilledDate":"","applicationPage":"resDashBoard","startDate":"{day}","endDate":""}}),
  contentType: "application/json; charset=utf-8",
  dataType: "json",
  async: false
}}).responseText
''')



import json
from os.path import exists
from datetime import date, timedelta
start_date = date(2020, 1, 1)
end_date = date(2022, 1, 1)
delta = timedelta(days=1)

while start_date <= end_date:
    day_str = start_date.strftime("%m%d%Y")
    day_file = f"{day_str}.json"
    if not exists(day_file):
        print(f"Fetching '{day_str}'")
        data = scrape_day(day_str)
        try:
            parsed = json.loads(data)
        except:
            print(data)
            quit()
        with open(day_file, "w") as f:
            f.write(json.dumps(parsed, indent=4, sort_keys=True))


    start_date += delta
