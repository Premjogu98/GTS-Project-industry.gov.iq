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
import wx
app = wx.App()

def ChromeDriver():
    chrome_options = Options()
    chrome_options.add_extension('C:\\BrowsecVPN.crx')
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"),chrome_options=chrome_options)
    browser.maximize_window()
    # browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 10 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(15)  # WAIT UNTIL CHANGE THE MANUAL VPN SETtING
    browser.get("http://industry.gov.iq/")
    wx.MessageBox(' -_-  Fill captche first if there -_- ', 'industry.gov.iq', wx.OK | wx.ICON_WARNING)
    time.sleep(2)
    browser.get("http://industry.gov.iq/index.php?name=monaksa")
    time.sleep(2)
    collec_link(browser)


def collec_link(browser):
    tr = 2
    page_count = 10
    a = True
    while a == True:
        try:
            tender_href_list = []
            for publish_date in browser.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[5]/center'):
                publish_date_text = publish_date.get_attribute('innerText').strip()
                datetime_object = datetime.strptime(publish_date_text, '%Y-%m-%d')
                publish_date = datetime_object.strftime("%Y-%m-%d")
                datetime_object_pub = datetime.strptime(publish_date, '%Y-%m-%d')
                User_Selected_date = datetime.strptime(str(Global_var.From_Date), '%Y-%m-%d')
                timedelta_obj = datetime_object_pub - User_Selected_date
                day = timedelta_obj.days
                if day >= 0:
                    for tender_href in browser.find_elements_by_xpath(f'/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[{str(tr)}]/td[8]/div/a'):
                        tender_href = tender_href.get_attribute('href').strip()
                        tender_href_list.append(tender_href)
                        tr += 1
                        break
                else:
                    Scrap_data(browser, tender_href_list)
            browser.get(f"http://industry.gov.iq/index.php?name=monaksa&countpage={str(page_count)}&currenpage=0&all=0")
            time.sleep(2)
            page_count = 20
            tr = 2
            a = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = True
def Scrap_data(browser, tender_href_list):
    a = True
    while a == True:
        try:
            for href in tender_href_list:
                browser.get(href)
                time.sleep(2)
                SegFeild = []
                for data in range(45):
                    SegFeild.append('')

                get_htmlSource = ""
                for outerHTML in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table'):
                    get_htmlSource = outerHTML.get_attribute('outerHTML')
                    get_htmlSource = get_htmlSource.replace('href="upload/', 'href="http://www.industry.gov.iq/upload/')
                    break
                # Purchaser
                Directorate_Name = ''
                for Directorate_Name in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[2]/td[2]'):
                    Directorate_Name = Directorate_Name.get_attribute('innerText').replace('&nbsp;', '').strip()
                    SegFeild[12] = Directorate_Name.strip()
                
                SegFeild[8] = ''
                
                # Title
                for Tender_Subject in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[3]/td[2]'):
                    Tender_Subject = Tender_Subject.get_attribute('innerText').replace('&nbsp;', '').strip()
                    Tender_Subject = string.capwords(str(Tender_Subject)).strip()
                    SegFeild[19] = Tender_Subject
                    break

                # Email
                for Email in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[4]/td[2]/div'):
                    Email = Email.get_attribute('innerText').replace('&nbsp;', '').replace('&nbsp;', '').strip().replace(' ','')
                    if ',' in Email:
                        Email_list = Email.split(',')
                        SegFeild[1] = Email_list[0].strip()
                    else:
                        SegFeild[1] = Email.strip()
                    break

                # tender NO
                for Bid_number in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[8]/td[2]'):
                    Bid_number = Bid_number.get_attribute('innerText').replace('&nbsp;', '').strip()
                    SegFeild[13] = Bid_number.strip()
                    break

                # Release Date
                Release_Date = ""
                for Release_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[6]/td[2]'):
                    Release_Date = Release_Date.get_attribute('innerText').strip()
                    break

                # Extention Date
                Extention_Date = ""
                for Extention_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[8]/td[2]'):
                    Extention_Date = Extention_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                    if Extention_Date == "لايوجد تمديد":
                        Extention_Date = ""
                    break

                # Close Date
                try:
                    for Close_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center/table/tbody/tr[7]/td[2]'):
                        Close_Date = Close_Date.get_attribute('innerText').strip()
                        datetime_object = datetime.strptime(Close_Date, "%Y-%m-%d")
                        mydate = datetime_object.strftime("%Y-%m-%d")
                        SegFeild[24] = mydate
                except:
                    SegFeild[24] = ""

                SegFeild[18] = "موضوع المناقصة: " + str(SegFeild[19]) + "<br>\n""اسم المديرية: " + str(Directorate_Name) + "<br>\n""تاريخ الاصدار: " + str(Release_Date) + "<br>\n""تاريخ تمديد المناقصة: " + str(Extention_Date) + "<br>\n""تاريخ الاغلاق: " + str(SegFeild[24])

                SegFeild[7] = "IQ"

                # notice type
                SegFeild[14] = "2"

                SegFeild[22] = "0"

                SegFeild[26] = "0.0"

                SegFeild[27] = "0"  # Financier

                SegFeild[28] = str(href)

                # Source Name
                SegFeild[31] = 'industry.gov.iq'

                SegFeild[20] = ""
                SegFeild[21] = "" 
                SegFeild[42] = SegFeild[7]
                SegFeild[43] = "" 

                for SegIndex in range(len(SegFeild)):
                    print(SegIndex, end=' ')
                    print(SegFeild[SegIndex])
                    SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                    SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
                if len(SegFeild[19]) >= 200:
                    SegFeild[19] = str(SegFeild[19])[:200]+'...'

                if len(SegFeild[18]) >= 1500:
                    SegFeild[18] = str(SegFeild[18])[:1500]+'...'
                    wx.MessageBox(' Short Desc To Long ','industry.gov.iq', wx.OK | wx.ICON_INFORMATION)

                if SegFeild[19] == '' or SegFeild[29] == '':
                    wx.MessageBox(' Short Desc Blank OR Dealine Blank','industry.gov.iq', wx.OK | wx.ICON_INFORMATION)
                else:
                    check_date(get_htmlSource, SegFeild)

        
                a = False
                print(" Total: " + str(len(tender_href_list)) + " Duplicate: " + str(Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(Global_var.inserted) + " Skipped: " + str(Global_var.skipped) + " Deadline Not given: " + str(Global_var.deadline_Not_given) + " QC Tenders: " + str(Global_var.QC_Tender),"\n")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = True
        ctypes.windll.user32.MessageBoxW(0, "Total: " + str(len(tender_href_list)) + "\n""Duplicate: " + str(Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(Global_var.inserted) + "\n""Skipped: " + str(Global_var.skipped) + "\n""Deadline Not given: " + str(Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(Global_var.QC_Tender) + "","industry.gov.iq", 1)
        Global_var.Process_End()
        browser.quit()
        sys.exit()

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
