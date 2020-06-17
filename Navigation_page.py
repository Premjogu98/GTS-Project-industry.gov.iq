from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local,create_filename
import sys, os
import ctypes
import string
import html


def ChromeDriver():
    File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\industry.gov.iq\\Location For Database & Driver.txt", "r")
    TXT_File_AllText = File_Location.read()
    Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    # chrome_options = Options()
    # chrome_options.add_extension('D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\industry.gov.iq\\Browsec-VPN.crx')  # ADD EXTENSION Browsec-VPN
    # browser = webdriver.Chrome(executable_path=str(Chromedriver),
    #                            chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser.get(
        """https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    for Add_Extension in browser.find_elements_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div[2]/div'):
        Add_Extension.click()
        break
    import wx
    app = wx.App()
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(25)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("http://www.industry.gov.iq/index.php?atlas=en")
    browser.set_window_size(1024, 600)
    browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    # time.sleep(2)
    time.sleep(1)
    # time.sleep(20)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    # browser.get('http://www.industry.gov.iq/index.php?atlas=en')
    # browser.set_window_size(1024 , 600)
    # browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])

    for Tender in browser.find_elements_by_xpath('//*[@id="smoothmenu2"]/ul/li[6]/a'):
        Tender.click()
        break
    time.sleep(2)
    for Search in browser.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/center[1]/input'):
        Search.click()
        break
    time.sleep(1.5)
    Scrap_data(browser)


def Scrap_data(browser):
    a = True
    while a == True:
        try:
                for Search_icon in range(2, 20, 1):
                    xpath_date = "/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr["+str(Search_icon)+"]/td[5]/center"
                    for publish_date in browser.find_elements_by_xpath(str(xpath_date)):
                        pubdate = publish_date.get_attribute("innerText").strip()
                        datetime_object = datetime.strptime(pubdate, '%Y-%m-%d')
                        publish_date1 = datetime_object.strftime("%Y-%m-%d")
                        if publish_date1 >= Global_var.From_Date:
                            print("Tender Date Alive")

                            Global_var.Total += 1
                            break
                        else:
                            print("Deadline Date Was Dead")
                            ctypes.windll.user32.MessageBoxW(0, "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(
                                    Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
                                    Global_var.inserted) + "\n""Skipped: " + str(
                                    Global_var.skipped) + "\n""Deadline Not given: " + str(
                                    Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(Global_var.QC_Tender) + "",
                                                                 "industry.gov.iq", 1)
                            Global_var.Process_End()
                            browser.close()
                            sys.exit()

                    Tender_href = ""
                    for search_icon_href in browser.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr['+str(Search_icon)+']/td[8]/div/a'):
                        search_icon_href.click()
                        break
                    time.sleep(2)
                    SegFeild = []
                    for data in range(42):
                        SegFeild.append('')

                    get_htmlSource = ""
                    for outerHTML in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]'):
                        get_htmlSource = outerHTML.get_attribute('outerHTML')
                        get_htmlSource = get_htmlSource.replace('href="/', 'href="http://www.industry.gov.iq/')
                        break

                    # Purchaser
                    Directorate_Name = get_htmlSource.partition("Directorate Name:</td><td>")[2].partition("</td>")[0]
                    SegFeild[12] = Directorate_Name.strip()

                    # Title
                    Subject = get_htmlSource.partition("Subject:</td><td>")[2].partition("</td>")[0]
                    Subject = string.capwords(str(Subject.strip()))
                    SegFeild[19] = Subject


                    # Email
                    Email = get_htmlSource.partition("E-mail:</td><td><div>")[2].partition("</div>")[0]
                    SegFeild[1] = Email.strip()


                    # tender NO
                    tender_NO = get_htmlSource.partition("No:</td><td>")[2].partition("</td>")[0]
                    SegFeild[13] = tender_NO.strip()


                    # Release Date
                    Release_Date = get_htmlSource.partition("Release Date:</td><td>")[2].partition("</td>")[0].strip()

                    # Extention Date
                    Extention_Date = get_htmlSource.partition("Extention Date:</td><td>")[2].partition("</td>")[0].strip()
                    # Document
                    Attachment = get_htmlSource.partition("Attachment:</td><td><a")[2].partition(">")[0].strip().replace('href="', 'href="http://www.industry.gov.iq/').replace("href=\"",'').replace('"',"")
                    SegFeild[5] = Attachment.strip()

                    # Close Date
                    try:
                        Close_Date = get_htmlSource.partition("Close Date:</td><td>")[2].partition("</td>")[0].strip()
                        datetime_object = datetime.strptime(Close_Date, "%Y-%m-%d")
                        mydate = datetime_object.strftime("%Y-%m-%d")
                        SegFeild[24] = mydate
                    except:
                        SegFeild[24] = ""

                    SegFeild[18] = "Subject: " + str(SegFeild[19]) + "<br>\n""Directorate_Name: " + str(SegFeild[12]) + "<br>\n""Release Date: " + str(Release_Date) + "<br>\n""Extention Date: " + str(Extention_Date) + "<br>\n""Close Date: " + str(SegFeild[24])

                    SegFeild[7] = "IQ"

                    # notice type
                    SegFeild[14] = "2"

                    SegFeild[22] = "0"

                    SegFeild[26] = "0.0"

                    SegFeild[27] = "0"  # Financier

                    SegFeild[28] = str(Tender_href)

                    # Source Name
                    SegFeild[31] = 'industry.gov.iq'

                    for SegIndex in range(len(SegFeild)):
                        print(SegIndex, end=' ')
                        print(SegFeild[SegIndex])
                        SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                        SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
                    if SegFeild == "":
                        browser.close()
                        quit()
                    a = False
                    browser.back()
                    check_date(get_htmlSource, SegFeild)
                    print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(
                        Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(
                        Global_var.inserted) + " Skipped: " + str(
                        Global_var.skipped) + " Deadline Not given: " + str(
                        Global_var.deadline_Not_given) + " QC Tenders: " + str(Global_var.QC_Tender), "\n")
                    # create_filename(get_htmlSource , SegFeild)
                for next_page in browser.find_elements_by_xpath(str(next)):
                    next_page = next_page.get_attribute('href')
                    if next_page != "":
                        browser.get(next_page)
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(
                            Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
                            Global_var.inserted) + "\n""Skipped: " + str(
                            Global_var.skipped) + "\n""Deadline Not given: " + str(
                            Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(Global_var.QC_Tender) + "",
                                                         "industry.gov.iq", 1)
                        Global_var.Process_End()
                        browser.quit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = True


def check_date(get_htmlSource, SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date , "%Y-%m-%d")
            currentdate = time.strptime(date2 , "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Tender Expired")
                Global_var.expired += 1
        else:
            print("Deadline was not given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" , exc_tb.tb_lineno)


ChromeDriver()
