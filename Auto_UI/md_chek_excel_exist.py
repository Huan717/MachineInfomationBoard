import os
from ftplib import FTP
#from dateutil import parser
import datetime as dt
from shutil import copy
from result import result

#------------------------------------------------------------------------
# MD 資料夾 路徑
class md_folder_path:
    def __init__(self,
                 Machine1_log_server='path',
                 Machine1_log_sava_path='path',
                 md_schedule_path='path',
                 md_schedule_save_path='path'
                 ):
        #Machine1 log server
        self.Machine1_log_server=Machine1_log_server
        # Machine1 log download path
        self.Machine1_log_sava_path=Machine1_log_sava_path
        #  流程表 server 路徑
        self.md_schedule_path=md_schedule_path
        #  預定表 download path
        self.md_schedule_save_path=md_schedule_save_path
#------------------------------------------------------------------------
class md_return_value:
    def __init__(self,update_time=None,md_excel_save_path=None):
        self.update_time=update_time
        self.md_excel_save_path=md_excel_save_path

#       預定表搜尋 與 複製
def find_ex_file(now_time,sever_mdex_update_t):
    year=now_time.year
    month=now_time.month
    #print(year,month)

    fn=md_folder_path().md_schedule_path+str(year)+"/"
    mddir=md_folder_path().md_schedule_save_path
    value_return=result()
    value_return.result = False
    try:
        if os.path.isdir(fn):
            for i in range(month, month-1, -1):
                filelist = os.listdir(fn)
                excelfileNameTemp = "【" + str(year) + "】" + str(i) + "月進度表"
                for listfile in filelist:

                    if excelfileNameTemp in listfile \
                            and "~$" not in listfile \
                            and "複本" not in listfile\
                            and excelfileNameTemp==listfile[0:11]:

                        excelfile = listfile
                        ex_file = fn + excelfile

                if os.path.isfile(ex_file):  # 檔案是否存在
                    exfileupdateT=dt.datetime.fromtimestamp(os.path.getmtime(ex_file)).strftime("%Y-%m-%d %H:%M:%S")
                    if sever_mdex_update_t==False or (sever_mdex_update_t!=False and exfileupdateT>sever_mdex_update_t):
                        value_return.result=md_return_value()
                        copy(ex_file,mddir)
                        value_return.result.update_time=exfileupdateT
                        mddir = md_folder_path().md_schedule_save_path
                        value_return.result.md_excel_save_path = mddir + excelfile
                    else:
                        print("md_schedule is not update in server")
                        value_return.isresult=True
                        value_return.resultText="sucessfuly : md_schedule is not update in server"
                    break

                else:
                    value_return.isresult = True
                    value_return.resultText = "sucessfuly : " + ex_file + " |   不存在"
                    print(ex_file+" |   不存在")
        else:
            value_return.isresult = True
            value_return.resultText = "sucessfuly : " + fn + " |   不存在"
        return value_return
    except Exception as e:
        print(e)
        print("錯誤 : 連線不上server or 其他原因")
        value_return.isresult = True
        value_return.resultText = "Error : 連線不上server or 其他原因 | " + e
        return value_return

#---------------------------------------------------------------------------------------------------------------------
