#!/usr/bin/env python3
import settings
import logging
from playsound import playsound
from time import sleep, localtime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Chrome

    def __enter__(self) -> webdriver.Chrome:
        logging.info("Open the browser")

        options = webdriver.ChromeOptions() 
        options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Chrome(options=options)

        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        return self._driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Close the browser")
        self._driver.quit()

class AlmanyaVizeRandevuBot:
    def __init__(self):
        self._buffer = 2
        self._no_appointment_warning_text = "Seçtiğiniz tarihte uygun randevu saati bulunmamaktadır."

    @staticmethod
    def enter_start_page(driver: webdriver.Chrome):
        driver.get(settings.BASE_URL)
        driver.implicitly_wait(300)
        logging.info("First page is loaded")
        driver.find_element(By.ID, 'confirmationbtn').click()
        logging.info("Go to the form")

    @staticmethod
    def fill_form(self, driver: webdriver.Chrome):
        logging.info("Start filling the appointment details form")
        s = Select(driver.find_element(By.ID, 'city'))
        s.select_by_value(settings.CITY)
        s = Select(driver.find_element(By.ID, 'office'))
        s.select_by_value(settings.OFFICE)
        s = Select(driver.find_element(By.ID, 'officetype' ))
        s.select_by_value(settings.OFFICE_TYPE)
        s = Select(driver.find_element(By.ID, 'totalPerson' ))
        s.select_by_value(str(len(settings.PERSONS)))
        logging.info("The appointment details form is done")


        driver.execute_script("window.scrollTo(0, 250)")
        driver.find_element(By.ID, 'btnAppCountNext').click()
        logging.info("The appointment details form is submitted")

        logging.info("Starting the personal details form")
        for p_id in range(len(settings.PERSONS)):
            s = driver.find_element(By.ID, "%s%s" % ('name', str(p_id+1)))
            s.send_keys(settings.PERSONS[p_id]['NAME'])
            s = driver.find_element(By.ID, "%s%s" % ('surname', str(p_id+1)))
            s.send_keys(settings.PERSONS[p_id]['SURNAME'])
            s = Select(driver.find_element(By.ID, "%s%s" % ('birthday', str(p_id+1))))
            s.select_by_value(settings.PERSONS[p_id]['BIRTHDAY'])
            s = Select(driver.find_element(By.ID, "%s%s" % ('birthmonth', str(p_id+1))))
            s.select_by_value(settings.PERSONS[p_id]['BIRTHMONTH'])
            s = Select(driver.find_element(By.ID, "%s%s" % ('birthyear', str(p_id+1))))
            s.select_by_value(settings.PERSONS[p_id]['BIRTHYEAR'])
            s = driver.find_element(By.ID, "%s%s" % ('passport', str(p_id+1)))
            s.send_keys(settings.PERSONS[p_id]['PASSPORT'])
            s = driver.find_element(By.ID, "%s%s" % ('phone', str(p_id+1)))
            s.clear()
            s.send_keys(settings.PERSONS[p_id]['PHONE'])
            s = driver.find_element(By.ID, "%s%s" % ('email', str(p_id+1)))
            s.clear()
            s.send_keys(settings.PERSONS[p_id]['EMAIL'])

        logging.info("The personal details form is done")
        
        driver.execute_script("window.scrollTo(0, 750)")
        driver.find_element(By.ID, 'btnAppPersonalNext').click()
        logging.info("The personal details form is submitted")

        driver.execute_script("window.scrollTo(0, 750)")
        driver.find_element(By.ID, 'btnAppPreviewNext').click()
        logging.info("Entered info is approved")

        driver.execute_script("window.scrollTo(0, 750)")
        sleep(self._buffer)

        driver.find_element(By.ID, 'flightDate').click()
        for _ in range(6):
            driver.find_elements(By.CLASS_NAME, "next")[0].click()
        selectable_flight_days = driver.execute_script("return document.querySelectorAll('.day:not(.old.day):not(.disabled.day)')")
        driver.execute_script("document.querySelectorAll('.day:not(.old.day)')[%s].click();" % str(len(selectable_flight_days)-1))
        logging.info("Flight date is selected")

    @staticmethod
    def find_appointment(self, driver: webdriver.Chrome):
        driver.find_element(By.XPATH, "//html").click()
        sleep(self._buffer)
        driver.find_element(By.ID, 'tarihGoster').click()
        driver.find_elements(By.CLASS_NAME, "clear")[0].click()
        sleep(self._buffer)
        driver.find_element(By.ID, 'tarihGoster').click()
        driver.execute_script("document.querySelectorAll('.day:not(.old.day):not(.disabled.day)')[0].click();")
        driver.find_element(By.XPATH, "//html").click()
        logging.info("Appointment date is selected")

    @staticmethod
    def isSuccess(self, driver: webdriver.Chrome):
        driver.execute_script("window.scrollTo(0, 750)")
        dateresult = driver.find_elements(By.CLASS_NAME, "dateresult")[0]
        availableDayInfo = driver.find_element(By.ID, "availableDayInfo")
        if availableDayInfo.text != "":
            return True
        if self._no_appointment_warning_text not in dateresult.text and dateresult.text != "":
            return True
        return False

    @staticmethod
    def play_sound(self):
        playsound("alarm.wav")
        while True:
            pass

    def isWorkingHours():
        return localtime().tm_hour >= settings.WORKING_HOURS_START and localtime().tm_hour < settings.WORKING_HOURS_END

    def run_once(self):
        with WebDriver() as driver:
            self.enter_start_page(driver)
            sleep(self._buffer)
            self.fill_form(self, driver)
            sleep(self._buffer)
            self.find_appointment(self, driver)
            sleep(self._buffer)
            for _ in range(30):
                if self.isSuccess(self, driver):
                    logging.info("SUCCESS!")
                    self.play_sound(self)
                else:
                    logging.info("No appointment yet. Retry submitting the form.")
                    sleep(settings.WAITING_TIME)
                    self.find_appointment(self, driver)

    def start(self):
        while True:
            if self.isWorkingHours:
                try:
                    self.run_once()
                    sleep(settings.WAITING_TIME)
                except Exception as e:
                    logging.info(e)
            logging.info("Not between working hours")
            sleep(settings.WAITING_TIME)

if __name__ == "__main__":
    AlmanyaVizeRandevuBot().start()
