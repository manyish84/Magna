import re
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import Scrapping_class

# Initializing Variables
company_report_dict = {}
company_report_table = pd.DataFrame()



url = r'https://www.magna.isa.gov.il/default.aspx#?p='
all_urls = [url + str(i) for i in range(4000)]


# Xpath of all section of the report in the web page
full_report_table = pd.DataFrame.from_csv("data.csv", encoding="windows-1255")
company_name = r"/child::*"
report_subject = r"//following-sibling::*"
report_reference = r"//following-sibling::*" * 3
report_date = r"//following-sibling::*" * 4
report_time = r"//following-sibling::*" * 5
report_http = r"/div[1]/a[1]" # Used later
section_xpath = [company_name, report_subject, report_reference, report_date, report_time]
section_name = ["Company_Name", "Subject", "Reference_Number", "Date", "Time"]

for j in range(len(all_urls)):
    driver = Scrapping_class.open_website(all_urls[j])

    # Loop through all reports in the page
    for i in range(10):
        elements = {}
        report_number_xpath = r'//*[@id="report_result_{}"]' .format(10*(j%3) + i + 1)
        report = [report_number_xpath + s for s in section_xpath]

        # Loop through all section in the report
        for (name, section) in zip(section_name ,report):
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
            for i in range(5,n_elements_in_footer+1):
                file_xpath = report_number_xpath + r"/div[2]/ul/li[{}]/div/a" . format(i)
                try:
                    file_counter += 1
                    file_link = driver.find_element_by_xpath(file_xpath).get_attribute('href')
                    file_number = "File {}" .format(file_counter)
                    elements.update({file_number: file_link})
                except:
                    file_counter += -1
        else:
            pass
        full_report_table = full_report_table.append(elements, ignore_index=True)


    full_report_table.drop_duplicates(inplace=True)
    full_report_table.to_csv("data.csv")
driver.close()

# //*[@id="report_result_1"]/div[2]/ul/li[5]/div/a
# //*[@id="report_result_6"]/div[2]/ul/li[5]/div/a
# //*[@id="report_result_6"]/div[2]/ul/li[7]/div/a

# //*[@id="report_result_1"]/div[2]/ul/li[5]/div/a
# url = r'https://www.magna.isa.gov.il/default.aspx#?p=1'
# driver = Scrapping_class.open_website(url)
#
#
#
# time.sleep(5)
# cube = '#report_result_11 > h3'
#
#
# url = r'https://www.magna.isa.gov.il/default.aspx#?p=2'
# driver = Scrapping_class.open_website(url)
#
#
#
# time.sleep(5)
# cube = '#report_result_21 > h3'
# #result_page_2 > ul:nth-child(1)
# comp_name = driver.find_element_by_css_selector(cube)
# print(comp_name.text)
#
# next_page = '#navigation_next2'
# driver.find_element_by_css_selector(next_page).click()
# time.sleep(5)
# driver.find_element_by_css_selector(next_page).click()
# time.sleep(5)
# comp_name = driver.find_element_by_css_selector(cube)
# print(comp_name.text)

    # # Extract headers of financial table
    # retry = 0
    # while retry < 3:
    #     headers = Scrapping_class.extract_headers(driver)
    #     # Extract the financial table
    #     financial_comp = np.ndarray((0,headers.size))
    #     for row in range(50):
    #         specific_row = np.array([[counter, comp_name]])
    #         for column in range(4):
    #             try:
    #                 table_rows = 'div:nth-child({}) > div.tableCol.col_{}.ng-binding.ng-scope'.format(row + 1, column + 1)
    #                 specific_row = np.append(specific_row, driver.find_element_by_css_selector(table_rows).text)
    #             except:
    #                 try:
    #                     table_rows = 'div:nth-child({}) > div.tableCol.wcol_{}.ng-binding.ng-scope'.format(row + 1,
    #                                                                                                       column + 1)
    #                     specific_row = np.append(specific_row, driver.find_element_by_css_selector(table_rows).text)
    #                 except:
    #                     pass
    #
    #         if specific_row.shape[0] > 1:
    #             financial_comp = np.vstack((financial_comp,specific_row))
    #     if financial_comp.size == 0:
    #         retry += 1
    #         if retry == 3:
    #             fail = np.append(fail,counter)
    #             continue
    #         else:
    #             driver.refresh()
    #             time.sleep(5)
    #     else:
    #         comp_financial_data = pd.DataFrame(data=financial_comp, columns=headers)
    #         full_financial_data = full_financial_data.append(comp_financial_data)
    #         driver.close()
    #         full_financial_data.to_csv('data.csv')
    #         retry = 3
    #         print(full_financial_data.shape)
    #         print(fail, fail.size)
    #
