import re
import pandas as pd
import numpy as np
from selenium import webdriver
import time

def open_website(url):
    try:
        driver = webdriver.Chrome(r'C:\Users\manyi\Downloads\chromedriver_win32\chromedriver.exe')
        driver.get(url)
        time.sleep(5)
        return driver
    except:
        return print ("Fail to load the page: " + url)



def scrape_page(driver, section_xpath, section_name):
    # Loop through all reports in the page
    for i in range(10):
        elements = {}
        report_number_xpath = r'//*[@id="report_result_{}"]'.format(10 * (j % 3) + i + 1)
        report = [report_number_xpath + s for s in section_xpath]

        # Loop through all section in the report
        for (name, section) in zip(section_name, report):
            try:
                element = driver.find_element_by_xpath(section).text
                elements.update({name: element})
            except:
                pass
        # Find the link of the report
        report_link_xpath = report_number_xpath + report_http
        try:
            report_link = driver.find_element_by_xpath(report_link_xpath).get_attribute('href')
            elements.update({"Report_Link": report_link})
        except:
            print(report_number_xpath)
        # Loop through the footer of every report and find the files
        file_counter = 0
        n_elements_in_footer = len(driver.find_elements_by_xpath(report_number_xpath + r"/div[2]/ul/li"))
        if n_elements_in_footer > 4:
            for i in range(5, n_elements_in_footer + 1):
                file_xpath = report_number_xpath + r"/div[2]/ul/li[{}]/div/a".format(i)
                try:
                    file_counter += 1
                    file_link = driver.find_element_by_xpath(file_xpath).get_attribute('href')
                    file_number = "File {}".format(file_counter)
                    elements.update({file_number: file_link})
                except:
                    file_counter += -1
        else:
            pass
        return elements

def download_file(lnk):
    driver = open_website(lnk)
    iframe = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(iframe[0])
    time.sleep(25)
    embed = driver.find_elements_by_tag_name("embed")[0].get_attribute("src")
    print(embed[0])

lnk = r'https://www.magna.isa.gov.il/details.aspx?reference=2019-01-051870&file=3&id=01177#?id=01177&reference=2019-01-051870&file=3'
download_file(lnk)

def extract_headers(driver):
    headers = np.array([['comp_serial_name', 'שם חברה']])
    for column in range(4):
        headers_css = ['div#gridHeader.tableCol.col_{}'.format(column + 1),
                       'div#gridHeader.tableCol.wcol_{}'.format(column + 1)]
        try:
            # headers_css = 'div#gridHeader.tableCol.col_{}'.format(column + 1)
            headers = np.append(headers, driver.find_element_by_css_selector(headers_css[0]).text)
        except:
            try:
                # headers_css = 'div#gridHeader.tableCol.wcol_{}'.format(column + 1)
                headers = np.append(headers, driver.find_element_by_css_selector(headers_css[1]).text)
            except:
                pass
    return headers

class web_scrap():
    def __init__(self, link):
        link = self.link
