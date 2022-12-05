
import os
import datetime as dt
from sql_tool import *
from ftplib import FTP


class clios_log:
    def __init__(self):
        self.data = {
            # 固定資料
            'lot': '',
            'load_start': '',
            'load_end': '',
            'unload_start': '',
            'unload_end': '',
            # 變動資料
            'state': '',
            'defect': '',
            'stripes': '',
            'check_start': '',
            'check_end': '',
            'expect_finish_time': '',
            'error_time': '',
            'error_text': '',
            # txt 使用資料
            "check": [],  # state,start,end,stripes,defect,expect_finish_time
            "error": []
        }
        # set lot
        self.set_lot=''
        self.lot_temp=''
        # 預計結束時間
        self.stripes_time = ''
        # 是否為我要的資料
        self.isdata = False
        # 是否為Warning
        self.warning_ctrl = {}
        # defect upper bound
        self.defect_upper_bound=10000
        # check wait time upper bound
        self.check_wait_time_upper_bound = 15
        #stripe last time
        self.stripes_last_time=''


# 找出資料
def search_state_line_to_data(lines, save_data):
    # 固定一筆資料-----------------------------------------
    # load start
    if '-- Loading Start...' in lines:
        # print('-------------------------------------------------------------------')
        save_data.isdata = True
        save_data.data['state'] = 'Load Start'
        save_data.data['load_start'] = lines[0:19]
        # print('Load Start',lines[0:19])
        pass
    # load end
    elif '-- Loading Complete' in lines or '-- Loading Failed' in lines:
        save_data.isdata = True
        save_data.data['state'] = 'Load End'
        save_data.data['load_end'] = lines[0:19]

        pass
    # Unload Start
    elif '-- Unloading Start' in lines:
        save_data.isdata = True
        save_data.data['state'] = 'Unload Start'
        save_data.data['unload_start'] = lines[0:19]
        if save_data.data['check'] != [] and save_data.data['check'][len(save_data.data['check'])-1][0] != lines[0:19]:
            save_data.data['check'].append(["Unload",lines[0:19],'','','','']) # state,start,end,stripes,defect,P YorN
        else:
            save_data.data['check'].append(["Unload",lines[0:19],'','','',''])
        pass

    # Unload END
    elif '-- Unloading Complete.' in lines:
        save_data.isdata = True
        save_data.data['state'] = 'Unload End'
        save_data.data['unload_end'] = lines[0:19]
        #print(save_data.data['state'], " | ", save_data.data['unload_end'], "...")
        # print('Unload End',lines[0:19])
        try:

            if save_data.data['check'] != [] and save_data.data['check'][len(save_data.data['check']) - 1][2] == '':
                save_data.data['check'][len(save_data.data['check']) - 1][2] = lines[0:19]
        except Exception as e:
            # print(e)
            pass

    # Unload Failed 不一定為取消
    elif '-- Unloading Failed.' in lines:
        save_data.isdata = True
        save_data.data['state'] = 'Unload Failed'
        save_data.data['unload_end'] = lines[0:19]
        #print(save_data.data['state'], " | ", save_data.data['unload_end'], "...")
        try:
            # print(len(data['check']), data['check'][len(data['check']) - 1][1])
            if save_data.data['check'] != [] and save_data.data['check'][len(save_data.data['check']) - 1][1] == '':
                save_data.data['check'][len(save_data.data['check']) - 1][2] = lines[0:19]
        except Exception as e:
            # print(e)
            pass
        pass

    # 多筆變動資料-----------------------------------------

    # Lot get
    elif 'SendData=[LOAD' in lines and '[DBDLL_U2]' in lines:
        save_data.isdata = True

        if lines.find('/data/gds/') != -1 and '/data/gds/' in lines:

            if lines.find('_LOUT') != -1:
                lot = lines[lines.find('/data/gds/') + 10:lines.find('_LOUT')]

            elif lines.find('_SOUT') != -1:
                    lot = lines[lines.find('/data/gds/') + 10:lines.find('_SOUT')]

            else:
                lot = lines[lines.find(',/data/gds/') + 11:lines.find(',/data/gds/') + 20]

        elif lines.find(',/data/') != -1 and ',/data/' in lines:

            if lines.find('_LOUT') != -1:
                lot = lines[lines.find('/data/') + 6:lines.find('_LOUT')]

            elif lines.find('_SOUT') != -1:
                    lot = lines[lines.find('/data/') + 6:lines.find('_SOUT')]

            else:
                lot = lines[lines.find(',/data/') + 6:lines.find(',/data/') + 16]

        save_data.data['state'] = 'SETTING'
        save_data.data['lot'] = lot
        # print('lot  :',save_data.data['lot'])

        pass

    elif 'MaskNameInfo.UserDefines0 is Modified.' in lines:
        a=lines.find('Modified.')+10
        save_data.set_lot=lines[a:a+9]
        save_data.lot_temp = lines
        #print(save_data.set_lot)

        pass


    # Error
    elif 'Local0.Warning' in lines and '[WARNING]' in lines:
        save_data.isdata = True
        save_data.data['state'] = 'Error'
        save_data.data['error_time'] =lines[0:19]
        save_data.data['error_text'] = lines[lines.find('thdID'):].split(')')[1].strip(' ')
        #print(lines[0:19],save_data.data['error_text'])
        #print(lines)


        pass

    # Check Start
    elif 'InspDetectCtrl: 検査開始通知' in lines:

        if save_data.data['lot']==save_data.set_lot:
            # print("same : ",save_data.data['lot'])
            pass
        else:
            # print("not same",save_data.data['lot']," | ",save_data.set_lot)
            # print(save_data.lot_temp)
            # print('/////////////////////////////////////////////////////////////////////////////////////')
            pass
        save_data.isdata = True
        save_data.data['state'] = 'Check Start'
        save_data.stripes_time = ''
        save_data.stripes_last_time=''
        if save_data.data['check_start'] != '' and save_data.data['check_start'] != lines[0:19]:
            save_data.data['check_start'] = lines[0:19]
            save_data.data['stripes'] = ''
            save_data.data['defect'] = ''
            save_data.data['check_end'] = ''
            save_data.data['expect_finish_time']=''
        else:
            save_data.data['check_start'] = lines[0:19]

        if save_data.data['check'] != [] and save_data.data['check'][len(save_data.data['check'])-1][0] != lines[0:19]:
            save_data.data['check'].append(["check",lines[0:19],'','','','']) # state,start,end,stripes,defect,P YorN
        else:
            save_data.data['check'].append(["check",lines[0:19],'','','',''])
        pass

    # Stripes
    elif '[H1]' in lines and 'ScanSeqCtrl::Running ' in lines:

        if 'Loop' in lines or 'otal' in lines:
            #print("例外事件")
            if 'Loop-Start' in lines:
                #print(lines)
                pass
            if 'Loop-End' in lines:
                pass
            pass
        else:
            save_data.isdata = True
            save_data.data['state'] = 'Stripes'
            #print('-----------------------------------')
            #print("Stripes : ", lines[0:19])
            stripes = lines[lines.find(('ScanSeqCtrl::Running')) + 21:].replace('=', '')
            stripes = stripes.replace('\n', '').strip(' ').split('/')
            # print(stripes,' | ',stripes[0]+'/'+stripes[1],'     <<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            if len(stripes) > 1:
                # 計算  預估檢查完成時間
                if stripes[0] > '1' and save_data.stripes_time == '':
                    save_data.stripes_time = dt.datetime.strptime(lines[0:19], "%Y-%m-%d %H:%M:%S")

                elif int(stripes[1]) > int(stripes[0]) and int(
                        stripes[0]) > 1 and save_data.stripes_time != '':
                    stripes_new_time = dt.datetime.strptime(lines[0:19], "%Y-%m-%d %H:%M:%S")
                    delta = ((stripes_new_time - save_data.stripes_time).seconds / (
                            int(stripes[0]) - 1)) * \
                            int(stripes[1])
                    #  估算檢查完成時間
                    D = int(delta / 86400)
                    H = int((delta / 3600) % 24)
                    M = int((delta / 60) % 60)
                    S = int(delta % 60)
                    save_data.data['expect_finish_time'] = save_data.stripes_time + dt.timedelta(days=D, hours=H,
                                                                                             minutes=M, seconds=S)
                    save_data.stripes_last_time = dt.datetime.strptime(lines[0:19], "%Y-%m-%d %H:%M:%S")
                    #print(save_data.stripes_time)
                save_data.data['stripes'] = stripes[0] + '/' + stripes[1]
                try:
                    save_data.data['check'][len(save_data.data['check']) - 1][3] = [stripes[0] + '/' + stripes[1]]
                    save_data.data['check'][len(save_data.data['check']) - 1][5]=save_data.data['expect_finish_time']
                except Exception as e:
                    # print(e)
                    pass
            # print(lines)
            # print(lines[0:20], save_data.data['stripes'])
        pass

    # Defect
    elif 'DefectDetectReceiver::IPC_DefectDetected() defId:' in lines:
        save_data.data['state'] = 'Defect'
        save_data.isdata = True
        if lines[lines.find('defId:') + 7:lines.find('defId:') + 9] == '-1':
            count = '0'
        elif lines.find('] 受信 [') != -1:
            count = lines[lines.find('defId:') + 7:lines.find('] 受信 [')]
        else:
            count = lines[lines.find('defId:') + 7:lines.find('] 完了 [')]
            # info_print(save_data.data.data)
        #print("Defect : ",lines[0:19])

        save_data.data['defect'] = count
        save_data.data['error_time']=''
        save_data.data['error_text']=''
        try:
            save_data.data['check'][len(save_data.data['check']) - 1][4] = count
        except Exception as e:
            # print(e)
            pass
        if int(count) > save_data.defect_upper_bound:
            if 'Defect>'+str(save_data.defect_upper_bound) in save_data.warning_ctrl.keys() and save_data.warning_ctrl['Defect>'+str(save_data.defect_upper_bound)]>0:
                save_data.warning_ctrl['Defect>'+str(save_data.defect_upper_bound)]+=1
            else:
                save_data.warning_ctrl['Defect>'+str(save_data.defect_upper_bound)]=1
            save_data.data['error_time'] = lines[0:19]
            save_data.data['error_text'] = 'Defect > ' +str(save_data.defect_upper_bound)
        if 'Defect>'+str(save_data.defect_upper_bound) in save_data.warning_ctrl.keys() and save_data.warning_ctrl['Defect>'+str(save_data.defect_upper_bound)] == 1 :
            pass
            # print("warning  " + count +"------ttttt------",save_data.data['check_start'])
        pass

    # Check End
    elif 'InspDetectCtrl: 検査終了通知' in lines or ('DetCtrlMain: 検査終了通知') in lines or (
            'InspStatus:' in lines and ('[Aborting]' in lines or 'Aborted' in lines)):

        if save_data.data['check_end'] == '':
            save_data.isdata = True
            save_data.stripes_time = ''  # 存完再清除
            save_data.data['state'] = 'Check End'
            # print(lines)
            save_data.data['check_end'] = lines[0:19]
            save_data.stripes_last_time = ''
            try:
                # print(len(data['check']), data['check'][len(data['check']) - 1][1])
                if save_data.data['check'] != [] and save_data.data['check'][len(save_data.data['check']) - 1][1] == '':
                    save_data.data['check'][len(save_data.data['check']) - 1][2] = lines[0:19]
            except Exception as e:
                # print(e)
                pass
        pass

    return save_data


# --------------------------------------------------------
# Tools

# Make String to select
def make_str_to_select(data , table):
    #print(data)
    data_key = list(data.keys())
    sql_str = "select * from dbo." + table
    temp_str = ''
    index = 0
    count = 0
    for key in data.keys():
        index += 1
        #print(key,"|",data[key])
        if (key == 'state' ) or key == 'defect' or key=='stripes':
            continue
        if data[key]=='':
            continue

        if count == 0:
            temp_str = temp_str + key + " = '" + str(data[key]) + "' "
        else:
            if data[data_key[index-1]] != '':
                temp_str = temp_str+" and " + key + " = '" + str(data[key]) + "'"

        count +=1

    #print(temp_str)
    # print('==========================================')


    return sql_str + " where " + temp_str


# Make String to insert
def make_str_to_insert(data , table):
    data_key = list(data.keys())
    sql_str = "insert into dbo."+table+" ("
    key_value = ''
    insert_value = '('
    for key in data_key:
        if key == data_key[len(data_key) - 1]:
            key_value = key_value + str(key) + ') '
            insert_value = insert_value + " '" + str(data[key]) + "')"
            pass
        else:
            key_value = key_value +  str(key) + ","
            insert_value = insert_value+ " '" + str(data[key]) + "' ,"
    return sql_str + key_value + ' values ' + insert_value


# Make String to Update    --------------------> NO 加了?
def make_str_to_update(data , table):
    data_key = list(data.keys())
    sql_str = "update dbo."+ table + " set "
    value = ''

    for key in data_key:
        if key == data_key[len(data_key) - 1]:
            value = value + key + " = '" + str(data[key]) + "'"
        else:
            value = value + key + " = '" + str(data[key]) + "',"

    if table== "md_main":
        return sql_str + value + " where no = '" + str(data['no']) + "'"
    elif table=="md_check":
        return sql_str + value + " where check_no = '" + str(data['check_no']) + "'"
    elif table=="md_now_state":
        return sql_str + value + " where no = '" + str(data['no']) + "'"


def compare_data(sql_data, data):
    pass

# key plus one
def key_tool_no_add_one(keyno):
    title= keyno[0:10]

    number=int(keyno[keyno.find('_')+1:])+1
    if number < 10:
        return (title+'_0'+str(number))
    else:
        return (title + '_' + str(number))


# insert main and check and error
def data_compare_insert(db):
    now=dt.datetime.now()
    now_t = dt.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
    # save to check table
    check_table = {
        'check_no': '',
        'md_main_no': '',
        'state': db.data['state'],
        'time_start': '',
        'time_end': '',
        'defect': db.data['defect'],
        'stripes': db.data['stripes'],
        'expect_finish_time': db.data['expect_finish_time'],
        'insert_time': ''
    }
    # save to main table
    main_table = {
        'no': '',
        'lot':db.data['lot'],
        'load_start': db.data['load_start'],
        'load_end': db.data['load_end'],
    }
    state = db.data['state']

    # table name
    md_main="md_main"
    md_check="md_check"
    md_error="md_error"
    no = str(db.data['load_start'][0:10].replace("-", ''))
    no = no + str(db.data['load_start'][11:13])

    if state == 'Load Start' :
        # no 格式 yyyymmddhh
        select_str = 'select * from dbo.md_main where no = ' + no
        main_table_select = md_sql().select(select_str)
        if main_table_select == [] :
            main_table['no'] = str(no)
            sql_str = make_str_to_insert(main_table,md_main)
            #print(sql_str)
            md_sql().insert(sql_str)
            pass
        else:
            #print('sql have data')
            pass

    if state == 'Load End' or state == 'SETTING':
        main_table['no'] = str(no)
        select_str = make_str_to_select(main_table,"md_main")
        main_table_select = md_sql().select(select_str)

        if main_table_select == []:
            select_str = 'select * from dbo.md_main where no = ' + no
            main_table_select_no = md_sql().select(select_str)

            if main_table_select_no != []:
                update_str = make_str_to_update(main_table,md_main)
                md_sql().update(update_str)
                #print(update_str)
            pass

        else:
            #print('sql have data')
            pass

    if state == 'Check Start' or state == 'Unload Start':
        check_table['md_main_no'] = no
        if state == 'Check Start':
            check_table['state'] = "Check"
            check_table['time_start'] = db.data['check_start']
        elif state == 'Unload Start':
            check_table['state'] = "Unload"
            check_table['time_start'] = db.data['unload_start']

        # 查詢md check 有無 資料
        select_str = make_str_to_select(check_table , md_check)
        check_select = md_sql().select(select_str)
        if check_select == []:
            select_str = "select top 1 * from dbo.md_check where md_main_no = '" + no +"' order by check_no desc"
            top_select = md_sql().select(select_str)
            if top_select == []:
                check_no = no + "_00"
            else:
                check_no = key_tool_no_add_one(top_select[0][0])
            check_table['check_no']=check_no
            check_table['insert_time']=now_t
            chk_insert = make_str_to_insert(check_table,md_check)
            #print(chk_insert)
            md_sql().insert(chk_insert)

        pass

    if state == 'Check End' or state == 'Unload End' or state =='Unload Failed':
        check_table['md_main_no'] = no
        if state == 'Check End':
            check_table['state'] = "Check"
            check_table['time_start'] = db.data['check_start']
            end_time_temp = db.data['check_end']
        elif state == 'Unload End' or state =='Unload Failed':
            #print(db.data['state']," | ",db.data['unload_end'],"...")
            check_table['state'] = db.data['state']
            check_table['time_start'] = db.data['unload_start']
            end_time_temp = db.data['unload_end']
        check_table['time_end'] = end_time_temp
        select_str = make_str_to_select(check_table, md_check)
        check_select = md_sql().select(select_str)
        if check_select == []:
            check_table['time_end'] = ''
            select_str = "select top 1 * from dbo.md_check where time_start = '" + check_table['time_start'] +"' order by check_no desc"
            top_select = md_sql().select(select_str)
            check_table['time_end'] = end_time_temp
            if top_select == []:
                pass
            else:
                check_no =top_select[0][0]
            check_table['check_no'] = check_no
            check_table['insert_time'] = now_t
            chk_update = make_str_to_update(check_table, md_check)
            md_sql().insert(chk_update)

        pass

    if state == 'Error':
        error_table={
            'error_no' : '',
            'state' : db.data['state'],
            'time' : db.data['error_time'],
            'text' : db.data['error_text'],
            'md_main_no' : no
        }
        select_str = make_str_to_select(error_table , md_error)
        select_result = md_sql().select(select_str)
        if select_result == []:
            select_error_table_top = "select top 1 * from dbo.md_error where md_main_no ='"+str(no)+"' order by error_no desc"
            #print(select_error_table_top)
            select_top_result = md_sql().select(select_error_table_top)
            #print(select_top_result)
            if select_top_result == []:
                error_no = no + "_00"
            else:
                error_no = key_tool_no_add_one(select_top_result[0][0])
            error_table['error_no'] =error_no

            error_insert = make_str_to_insert(error_table , md_error)
            md_sql().insert(error_insert)
        db.data['error_time']=''
        db.data['error_text']=''
        pass

    # Warning : Defect > 10000

    if state == 'Defect':

        if db.warning_ctrl != {} and db.warning_ctrl['Defect>'+str(db.defect_upper_bound)]==1 :
            #print(db.warning_ctrl)
            error_table = {
                'error_no': '',
                'state': 'Warning',
                'time': db.data['error_time'],
                'text': db.data['error_text'],
                'md_main_no': no,
                'check_start': db.data['check_start']
            }
            select_error = make_str_to_select(error_table , md_error)
            #print(select_error)
            select_result = md_sql().select(select_error)
            if select_result == [] :
                select_error_table_top = "select top 1 * from dbo.md_error where md_main_no ='" + str(
                    no) + "' order by error_no desc"
                # print(select_error_table_top)
                select_top_result = md_sql().select(select_error_table_top)
                if select_top_result == []:
                    error_no = no + "_00"
                else:
                    error_no = key_tool_no_add_one(select_top_result[0][0])
                error_table['error_no'] = error_no
                error_insert = make_str_to_insert(error_table, md_error)
                md_sql().insert(error_insert)
                pass

        pass

#最新狀態更新
def now_state(log_data):
    new_data = {
        'no': '0',
        'machine': 'clios',
        'state': log_data.data['state'],
        'lot': log_data.data['lot'],
        'load_start': log_data.data['load_start'],
        'check_start':log_data.data['check_start'],
        'stripes': log_data.data['stripes'],
        'defect': log_data.data['defect'],
        'expect_finish_time': log_data.data['expect_finish_time']
    }
    if log_data.data['state'] == 'Defect' or log_data.data['state'] == 'Stripes':
        new_data['state'] = 'Checking'
        print(log_data.data['stripes'],log_data.data['stripes'].split("/")[0]," | ",log_data.data['stripes']!='',int(log_data.data['stripes'].split("/")[0])>30)

        if log_data.data['stripes']!='' and int(log_data.data['stripes'].split("/")[0])>30 and log_data.stripes_last_time!='':
            now_time = dt.datetime.now()
            if now_time > log_data.stripes_last_time:
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                print(now_time, " | ", log_data.stripes_last_time, type(log_data.stripes_last_time))
                stripes_last_time = now_time - log_data.stripes_last_time
                time_overflow = stripes_last_time.seconds / 60
                print(time_overflow, " | ", log_data.check_wait_time_upper_bound, " | ",
                      int(time_overflow) > int(log_data.check_wait_time_upper_bound))
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                # 確認是否超過 10分鐘 超過 存 錯誤訊息
                # 超過時間上限設定 10 min
                if int(time_overflow) > int(log_data.check_wait_time_upper_bound):
                    no = str(log_data.data['load_start'][0:10].replace("-", ''))
                    no = no + str(log_data.data['load_start'][11:13])
                    new_data['state'] = 'Warning'
                    error_table = {
                        'error_no': '',
                        'state': 'Warning',
                        'time': log_data.stripes_last_time,
                        'text': "Stripes after Waiting more then " + str(log_data.check_wait_time_upper_bound) + " min",
                        'md_main_no': no,
                        'check_start': log_data.data['check_start']
                    }
                    select_str = "select * from dbo.md_error where "
                    index = 0
                    count = 0
                    temp_str = ''
                    datakey = list(error_table.keys())
                    for key in datakey:
                        index += 1
                        if error_table[key] == '':
                            continue
                        if count == 0:
                            temp_str = temp_str + key + " = '" + str(error_table[key]) + "' "
                        else:
                            if error_table[datakey[index - 1]] != '':
                                temp_str = temp_str + " and " + key + " = '" + str(error_table[key]) + "'"
                        count += 1
                    select_result = md_sql().select(select_str + temp_str)
                    if select_result == []:
                        select_str = "select * from dbo.md_error where md_main_no ='" + \
                                     str(no) + "' order by error_no desc"
                        top_result = md_sql().select(select_str)
                        if top_result == []:
                            error_no = no + "_00"
                        else:
                            error_no = key_tool_no_add_one(top_result[0][0])
                        error_table['error_no'] = error_no
                        error_insert = make_str_to_insert(error_table, "md_error")
                        md_sql().insert(error_insert)


    select_str = "select * from dbo.md_now_state where no = 0"
    result = md_sql().select(select_str)
    print(result)
    if result == []:
        md_sql().insert(make_str_to_insert(new_data, "md_now_state"))
    else:
        new_data_list = list(new_data.keys())
        conturl = False
        for i in range(len(result[0])-1):
            if result[0][i] != new_data[new_data_list[i]]:
                print(result[0][i]," | ",new_data[new_data_list[i]])
                conturl = True
        if conturl:
            select_str = make_str_to_update(new_data, "md_now_state")
            print(select_str)
            md_sql().update(select_str)

        pass


# 要下載的txt名稱
def set_logname_to_donwload(file,data_list):

    now_t=dt.datetime.now()
    start_dload_t=dt.datetime.strptime(file[0:10]+' '+file[11:13]+':00:00',"%Y-%m-%d %H:00:00")

    while(start_dload_t<now_t):
        #print(str(start_dload_t)[0:10] + '_' + str(start_dload_t)[11:13] + '.txt')
        data_list.append(str(start_dload_t)[0:10] + '_' + str(start_dload_t)[11:13] + '.txt')
        start_dload_t=start_dload_t+dt.timedelta(hours=+1)

    return data_list
    pass


#---------------------------------------------------------------------------------------------------------------------
# FTP download log
def download_log(all_log_name):
    try:
        print(all_log_name)
        ftp = FTP()
        ftp.connect("127.0.0.1")
        ftp.login("user", "passwd")
        # print(ftp.getwelcome())
        ftp.cwd('path (dowload txt on this path)')
        list = ftp.nlst()
        nodownload=[]
        for name in all_log_name:
            if name in list:
                print('Dowload Start')
                print('Downlaod file : ', name)
                localfile = open('save to path' + name, 'wb')
                ftp.retrbinary('RETR ' + name, localfile.write)
                ftp.set_debuglevel(0)
                localfile.close()
                print('Dowload End')
            else:
                print(name,' is no data in server')
                nodownload.append(name)
                all_log_name.remove(name)
        ftp.quit()
        return [all_log_name,nodownload]
    except Exception as e:
        print('download Error or FTP error')
        print("Error message : ",e)
        return [all_log_name,['error']]




# 下載資料
def file_dload(temp_dload_list , clios_log_path):
    log_path_file_data = os.listdir(clios_log_path)
    download_list = []
    # print(temp_dload_list)
    for i, t_exist in enumerate(temp_dload_list):

        if t_exist in log_path_file_data and \
                t_exist != log_path_file_data[len(log_path_file_data) - 1] and \
                t_exist != log_path_file_data[len(log_path_file_data) - 2] and \
                t_exist != str(dt.datetime.now())[0:10] + '_' + str(dt.datetime.now())[11:13] + '.txt' \
                :
            pass
        else:
            download_list.append(t_exist)
    #print(download_list)
    '''         下載資料    '''
    # dload_list=[]
    if download_list != []:
        download_log(download_list)
        download_list.clear()
        pass
    else:
        print('func : download is not do')

#if __name__ == '__main__':
def clios_log_get_main():
    # New Time
    #NT = dt.datetime.now()
    # path

    machine_log_path = 'path'

    # ----------------------------------------------------------------------------------------------------------------
    #

    # log_path_file_data=[]
    # 保底有4天資料可以讀

    three_day_before = str(dt.datetime.now() - dt.timedelta(days=+2))[0:10] + '_00.txt'

    # sql 查詢  data : [ 檔名 , 行數 , txt資料 , [最後的讀取資料]]
    # last_txt_on_sql=['2021-12-04_14.txt',0,'','']
    last_txt_on_sql = []
    try :
        if last_txt_on_sql != [] and type(last_txt_on_sql[0] == str):
            temp_t = dt.datetime.strptime(last_txt_on_sql[0][0:10] + ' '
                                          + last_txt_on_sql[0][11:13] + ':00:00', "%Y-%m-%d %H:00:00")
            if dt.datetime.strftime(temp_t, '%Y-%m-%d %H:00:00"') < three_day_before:
                dload_list = set_logname_to_donwload(last_txt_on_sql[0], [])
                r_list = dload_list
            else:
                dload_list = set_logname_to_donwload(three_day_before, [])
                r_list = set_logname_to_donwload([last_txt_on_sql[0]], [])

        else:
            dload_list = set_logname_to_donwload(three_day_before, [])
            r_list = dload_list
    except Exception as e:
        return e

    file_dload(dload_list, clios_log_path)

    log_data = None
    for filename in r_list:
        if os.path.isfile(clios_log_path + filename):
            text = open(clios_log_path + filename, "r", encoding="shift_jis")
            for line in text:
                if '-- Loading Start...' in line:

                    if log_data != None and log_data.data['load_start'] != '':
                        # print(log_data.data['check'])
                        # print("Error", log_data.data['error'])
                        pass
                    log_data = clios_log()
                if log_data != None:
                    db = search_state_line_to_data(line, log_data)
                    if db.isdata:
                        state = db.data['state']
                        if state == 'Stripes':
                            pass
                        else:
                            if state == "Error":
                                pass
                            data_compare_insert(db)
                            pass
                        db.isdata = False

    # compare now data and sql data
    # print(log_data.data)
    now_state(log_data)

    return True



