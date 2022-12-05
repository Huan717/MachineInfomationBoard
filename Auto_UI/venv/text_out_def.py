import datetime as dt

now_data = {
        'no' : '0',
        'machine' : 'clios',
        'state' : '',
        'lot' : '',
        'load_start' : '',
        'stripes' : '',
        'defect' :'',
        'expect_finish_time' : ''
    }
select_str = "select * from dbo.md_now_state where "
print(now_data.keys())
for key in now_data.keys():
    if key == list(now_data.keys())[len(now_data.keys())-1]:
        select_str = select_str + key +"='" + now_data[key] +"'"
        continue
    select_str = select_str + key + "='" + now_data[key] + "' and "
now_time = dt.datetime.now()
test = dt.datetime.strptime('2022-06-27 11:20:09', "%Y-%m-%d %H:%M:%S")
temp = now_time- test

print(temp.seconds/60)
error_table = {
                'error_no': '',
                'state': 'Warning',
                'time': 'stripes_last_time',
                'text': 'Stripes after Waiting more then 10 min',
                'md_main_no': 'no',
                'check_start': '32123'
            }
select_str = "select * from dbo.md_error where "
index = 0
count = 0
temp_str=''
datakey= list(error_table.keys())
#print(error_table)

'''
data_key = list(data.keys())
    sql_str = "select * from dbo." + table
    temp_str = ''
    index = 0
    count = 0
    for key in data.keys():
        index += 1  
        #print(key,"|",data[key])
        if data[key]=='':
            continue

        if count == 0:
            temp_str = temp_str + key + " = '" + str(data[key]) + "' "
        else:
            if data[data_key[index-1]] != '':
                temp_str = temp_str+" and " + key + " = '" + str(data[key]) + "'"

        count +=1
'''