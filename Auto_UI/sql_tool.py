import pymssql as mssql
class md_sql():

    def __init__(self):
        self.ms_sql = mssql.connect(
            host='127.0.0.1',
            user='user',
            password='password',
            database='database'
        )
        self.cursor = self.ms_sql.cursor()
    


    # 查詢
    def select(self, s_str):
        #print(s_str)
        cursor = self.ms_sql.cursor()
        cursor.execute(str(s_str))
        result=cursor.fetchall()
        #print(result)
        return result

    # 修改資料
    def update(self, sql_str):
        self.cursor.execute(str(sql_str))
        self.close()

    # 新增
    def insert(self, sql_str):
        self.cursor.execute(str(sql_str))
        self.close()
    # 關閉資料庫
    def close(self):
        self.ms_sql.commit()
        self.ms_sql.close()

    #   新增MASK 基本資料_______________OK...04/15
    def lot_insert(self, data):
        #print("SELECT * FROM [dbo].[web_MDKB_lot_info] where lot = " + data['lot'] + ";")
        self.cursor.execute("SELECT * FROM [dbo].[web_MDKB_lot_info] where lot = " + data['lot'] + ";")
        result = self.cursor.fetchone()
        # print(result)
        if result == None:
            key_arr = ['lot', 'maskid', 'customer', 'size', 'masktype','pornot']
            table = ""
            value = ""
            for key in key_arr:
                if key == key_arr[len(key_arr) - 1]:
                    value = value + "'" + data[key] + "'"
                    table = table + "[" + key + "]"
                else:
                    value = value + "'" + data[key] + "',"
                    table = table + "[" + key + "],"
            inser_str = "INSERT INTO [dbo].[web_MDKB_lot_info] (" + table + ") VALUES (" + value + ");"
            #print(inser_str)
            self.cursor.execute(inser_str)
            # print(data['lot'], ':sql inser finsh')
            self.close()
            # print(data['lot'], data['maskid'], data['customer'], data['size'], '|', data['masktype'], data['spec'])
            return 'successful'
        else:
            # print(data['lot'], 'sql have data')
            return data['lot'], 'mssql have data'

    #   新增 進度表時間   _______________OK...04/15
    def ex_insert(self, data):
        key_arr = ['lot', 'Machine', 'status', 'start_time', 'end_time']
        table = ""
        value = ""
        for key in key_arr:
            if key == key_arr[len(key_arr) - 1]:
                value = value + "'" + data[key] + "'"
                table = table + key
            else:
                value = value + "'" + data[key] + "',"
                table = table  + key + ","
        inser_str = "INSERT INTO [dbo].[web_MDKB_No_of_inspect]  (" + table + ") VALUES (" + value + ");"
        #print(inser_str)
        self.cursor.execute(inser_str)
        #print(data['lot'], ':time insert finsh')
        self.close()
    def del_all(self):
        sql_str = "DELETE FROM [dbo].[web_MDKB_No_of_inspect] WHERE (lot = '%*%');"
        self.cursor.execute(sql_str)
        self.ms_sql.commit()
        self.close()

    # 刪除 狀態 N  R  Y 的資料
    def del_nrf(self):
        sql_str = "SELECT lot FROM [dbo].[web_MDKB_No_of_inspect] where status='N' or status='R' or status='F';"
        print(sql_str)

        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        self.ms_sql.commit()
        print(result)
        if result != []:
            for i in result:
                # print(i[0])
                sql_str = "DELETE FROM [dbo].[web_MDKB_No_of_inspect] WHERE (lot = '" + i[0] + "');"
                self.cursor.execute(sql_str)
                self.ms_sql.commit()
        else:
            print("data 無R&N的資料")
        self.close()

    def del_y(self):
        sql_str = "SELECT lot FROM [dbo].[web_MDKB_No_of_inspect] where Update_temp='Y';"
        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        self.ms_sql.commit()
        if result != []:
            for db in result:
                sql_str = "UPDATE [dbo].[web_MDKB_No_of_inspect] SET [Update_temp] = null WHERE (lot = '" + db[0] + "');"
                self.cursor.execute(sql_str)
                self.ms_sql.commit()
        self.close()


    #Machine1即時狀態
    def log_select(self,sql_str):
        cursor = self.ms_sql.cursor()
        cursor.execute(sql_str)
        #print('sql ',cursor.fetchall())
        return cursor.fetchall()
        self.close()

    def Machine1_log_upload(self,data):
        print("------------------------------------",data['now_t'])
        key_db=list(data.keys())

        table = ""
        value = ""
        for key in key_db:
            if key == key_db[len(key_db) - 1]:
                value = value + "'" + data[key] + "'"
                table = table + key
            else:
                value = value + "'" + data[key] + "',"
                table = table + key + ","

        inser_str = "INSERT INTO [dbo].[web_Machine1_log]  (" + table + ") VALUES (" + value + ");"
        print(inser_str)
        self.cursor.execute(inser_str)
        self.close()

        return ("insert")

    def log_update(self, data):
        print("update")
        str ="UPDATE [dbo].[web_Machine1_log] SET defect='"+data['defect']+"', stripes='"+data['stripes']+"' ,check_end='"+data['check_end']+"' ,expect_finish_time='"+data['expect_finish_time']+"' WHERE ([NO] = "+data['NO']+");"

        print(str)
        self.cursor.execute(str)
        self.ms_sql.commit()
        self.close()


    def Machine1_log_insert_t(self,data):
        print("------------------------------------",data['now_t'])
        key_db=list(data.keys())

        table = ""
        value = ""
        for key in key_db:
            if key == key_db[len(key_db) - 1]:
                value = value + "'" + str(data[key]) + "'"
                table = table + key
            else:
                value = value + "'" + str(data[key]) + "',"
                table = table + key + ","

        inser_str = "INSERT INTO [dbo].[web_Machine1_log_text]  (" + table + ") VALUES (" + value + ");"
        print(inser_str)
        self.cursor.execute(inser_str)
        self.close()

        return ("insert")

    def log_update_chk_t(self, sql_str):
        #print(sql_str)
        self.cursor.execute(sql_str)
        self.ms_sql.commit()
        self.close()

    def log_update_load_t(self, data):

        if data['state']=='load_end':
            sql_str="SELECT * FROM [dbo].[web_Machine1_log_text] WHERE load_start='"+data['load_start']+"'"
            temp = self.log_select(sql_str)
            if temp!=[]:
                data['NO']=temp[0][0]
                sql_str="UPDATEUPDATE [dbo].[web_Machine1_log_text] SET load_end='"+data['load_end']+"' WHERE ([NO] = "+str(data['NO'])+")"
                print(sql_str)
                self.cursor.execute(sql_str)
                self.ms_sql.commit()
                self.close()
            else:
                print('can\'t find data')
        #str ="UPDATE [dbo].[web_Machine1_log_text] SET defect='"+data['defect']+"', stripes='"+data['stripes']+"' ,check_end='"+data['check_end']+"' ,expect_finish_time='"+data['expect_finish_time']+"' WHERE ([NO] = "+data['NO']+");"

        #print(str)
        #self.cursor.execute(str)
        #self.ms_sql.commit()
        #self.close()






