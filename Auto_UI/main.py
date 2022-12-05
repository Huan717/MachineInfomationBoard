from MDUI import MD_UI
import sys
import time
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from md_chek_excel_exist import *
from get_insert_md_excel import *
from clios_log_data_insert import *

class set_ui(MD_UI):
    def __init__(self):
        super(set_ui,self).__init__()
        self.btn_start.clicked.connect(self.time_to_start)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_stop.clicked.connect(self.stop)
        self.md_excel_update_time = False
        self.timer2 = QtCore.QTimer(self)  # 呼叫 QTimer
        self.timer2.timeout.connect(self.start)
#-------------------------------------------------------------------------------
# 啟動
    def time_to_start(self):
        self.ft_log_run_time = 4 * 60
        self.start()
        self.timer2.start(240000)
    def start(self):
        now_t = dt.datetime.now()
        now_tstr = now_t.strftime("%Y-%m-%d %H:%M:%S")
        self.msg.insertPlainText("Start to Run\n")
        self.msg.insertPlainText("Now Time : "+str(now_tstr)+"\n")
        self.msg.insertPlainText("run func : clios_log_get_main()\n")
        result_clios_data = clios_log_get_main()
        if result_clios_data:
            self.msg.insertPlainText("clios_log_get_main()  DONE\n")
        else:
            self.msg.insertPlainText("clios_log_get_main()  false\n")
            self.msg.insertPlainText("Error Message : "+ str(result_clios_data) +"\n")

        self.msg.insertPlainText("run func : find_ex_file()\n")
        path = find_ex_file(now_t, self.md_excel_update_time)
        self.msg.insertPlainText("find_ex_file()  DONE\n")
        if path.result != False:
            self.msg.insertPlainText(path.result.update_time + "\n")
            self.msg.insertPlainText(path.result.md_excel_save_path + "\n")
            print("Update_time = ", path.result.update_time)
            print("%-14s" % ("MD EX Path  = "), path.result.md_excel_save_path)
            self.md_excel_update_time = path.result.update_time
            md_ex_data = get_ex_data(now_t, path.result.md_excel_save_path)
            if md_ex_data != None:
                for data in md_ex_data:
                    print("%-7s | %-10s | %-3s | %-12s | %-12s | %-40s " % (
                        data['masktype'], data['lot'], data['pornot'], data['size'], data['customer'], data['maskid']))
                    print("%-6s | %-2s | %-18s | %-18s | %-6s - %-6s" % (
                        data['Machine'], data['status'], data['start_time'], data['end_time'], data['data_start'],
                        data['data_end']))
                    # print(data.machine," | ",data.lot," | ",data.maskid," | ",data.customer," | ",data.size)
                    # print(data.masktype," | ",data.start_time," | ",data.end_time,)

                    print("--------------------------------------------------------------------------")
                ex_data_upload(md_ex_data)
            else:
                self.msg.insertPlainText(path.resultText)
        self.msg.insertPlainText("--------------------------------------------\n")
# 停止

    def stop (self):
        self.timer2.stop()
        self.msg.clear()
        self.md_excel_update_time = False
# 清除

    def clear_text( self ):
        self.msg.clear()
        pass
#-------------------------------------------------------------------------------




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = set_ui()
    ui.show()
    sys.exit(app.exec_())


