import re
from Util.dir_opration import make_current_date_dir, make_current_hour_dir, get_current_time, get_current_date
from Util.excel import *
from Action.keyword_action import *
import traceback
from Util.log import *
import time

from ProjVar.var import test_case_is_executed_flag_col_no


def get_test_case_sheet(test_cases_excel_path):
    test_case_sheet_names = []
    excel_obj = Excel(test_cases_excel_path)
    excel_obj.set_sheet_by_index(1)
    test_case_rows = excel_obj.get_rows_object()[1:]
    for row in test_case_rows:
        if row[3].value=='y':
            print(row[2].value)
            test_case_sheet_names.append((int(row[0].value)+1,row[2].value,row[4].value))
    return test_case_sheet_names


def execute(test_cases_excel_path,row_no,test_case_sheet_name):
    excel_obj = Excel(test_cases_excel_path)
    excel_obj.set_sheet_by_name(test_case_sheet_name)
    test_step_rows =  excel_obj.get_rows_object()[1:]
    start_time = get_current_date()+" "+get_current_time()
    start_time_stamp = time.time()
    test_result_flag = True
    for test_step_row in test_step_rows:
        if test_step_row[6].value=="y":
            test_action =test_step_row[2].value
            locator_method = test_step_row[3].value
            locator_exp = test_step_row[4].value
            test_value = test_step_row[5].value
            #print(test_action,locator_method,locator_exp,test_value)
            if locator_method is None:
                if test_value is None:
                    command = test_action+"()"
                else:
                    command = test_action + "('%s')" %test_value
            else:
                if test_value is None:
                    command = test_action+"('%s','%s')" %(locator_method,locator_exp)
                else:
                    command = test_action + "('%s','%s','%s')" %(locator_method,locator_exp,test_value)
            print (command)
            try:
                info(command)
                eval(command)
                excel_obj.write_cell_value(int(test_step_row[0].value)+1, test_step_result_col_no,"执行成功")
                excel_obj.write_cell_value(int(test_step_row[0].value) + 1, test_step_error_info_col_no, "")
                excel_obj.write_cell_value(int(test_step_row[0].value) + 1, test_step_capture_pic_path_col_no, "")
                info("执行成功")
            except Exception as e:
                test_result_flag = False
                traceback.print_exc()
                error(command+":"+traceback.format_exc())
                excel_obj.write_cell_value(int(test_step_row[0].value) + 1, test_step_result_col_no, "失败","red")
                excel_obj.write_cell_value(int(test_step_row[0].value) + 1, test_step_error_info_col_no,\
                                           command+":"+traceback.format_exc())
                dir_path = make_current_date_dir(ProjDirPath + "\\" + "ScreenCapture\\")
                dir_path = make_current_hour_dir(dir_path + "\\")
                pic_path = os.path.join(dir_path,get_current_time()+".png")
                capture(pic_path)
                excel_obj.write_cell_value(int(test_step_row[0].value) + 1, test_step_capture_pic_path_col_no, pic_path)
    end_time = get_current_date() + " " + get_current_time()
    end_time_stamp = time.time()
    elapsed_time = int(end_time_stamp - start_time_stamp)
    elapsed_minutes = int(elapsed_time//60)
    elapsed_seconds = elapsed_time % 60
    elapsed_time = str(elapsed_minutes)+"分"+str(elapsed_seconds)+"秒"
    if test_result_flag:
        test_case_result ="测试用例执行成功"
    else:
        test_case_result = "测试用例执行失败"
    excel_obj.set_sheet_by_index(1)
    excel_obj.write_cell_value(int(row_no),test_case_start_time_col_no,start_time)
    excel_obj.write_cell_value(int(row_no), test_case_end_time_col_no,end_time)
    excel_obj.write_cell_value(int(row_no), test_case_elapsed_time_col_no, elapsed_time)
    if test_result_flag:
        excel_obj.write_cell_value(int(row_no) , test_case_result_col_no, test_case_result)
    else:
        excel_obj.write_cell_value(int(row_no), test_case_result_col_no, test_case_result,"red")


def execute_hybrid(test_cases_excel_path,row_no,test_case_sheet_name,test_data_sheet_name):
    test_data = get_test_data_from_data_sheet(test_cases_excel_path, test_data_sheet_name)
    excel_obj = Excel(test_cases_excel_path)
    excel_obj.set_sheet_by_name(test_case_sheet_name)
    test_step_rows =  excel_obj.get_rows_object()[1:]

    test_result_flag = True
    s1=time.time()
    start = get_current_date() + " " + get_current_time()
    for data in test_data:
        test_data_result_flag = True
        start_time = get_current_date() + " " + get_current_time()
        start_time_stamp = time.time()
        for test_step_row in test_step_rows:
            if test_step_row[6].value=="y":
                test_action =test_step_row[2].value
                locator_method = test_step_row[3].value
                locator_exp = test_step_row[4].value
                test_value = test_step_row[5].value
                if test_value and re.search(r"\$\{(\d+)\}",str(test_value)):
                    index = re.search(r"\$\{(\d+)\}", str(test_value)).group(1)
                    try:
                        test_value = data[int(index)]
                    except:
                        print(test_value+"中的数字索引在测试数据sheet中不存在对应的列")
                if locator_method is None:
                    if test_value is None:
                        command = test_action+"()"
                    else:
                        command = test_action + "('%s')" %test_value
                else:
                    if test_value is None:
                        command = test_action+"('%s','%s')" %(locator_method,locator_exp)
                    else:
                        command = test_action + "('%s','%s','%s')" %(locator_method,locator_exp,test_value)
                print (command)
                try:
                    info(command)
                    eval(command)
                    excel_obj.set_sheet_by_name(test_data_sheet_name)
                    info("执行成功")
                except Exception as e:
                    test_result_flag = False
                    test_data_result_flag = False
                    traceback.print_exc()
                    error(command+":"+traceback.format_exc())
                    excel_obj.write_cell_value(int(data[0]) + 1, len(data) + 5, "执行失败","red")
                    excel_obj.write_cell_value(int(data[0]) + 1, len(data) + 6, command+":"+traceback.format_exc())
                    dir_path = make_current_date_dir(ProjDirPath + "\\" + "ScreenCapture\\")
                    dir_path = make_current_hour_dir(dir_path + "\\")
                    pic_path = os.path.join(dir_path,get_current_time()+".png")
                    capture(pic_path)
                    excel_obj.write_cell_value(int(data[0]) + 1, len(data) + 7, pic_path)
        end_time = get_current_date() + " " + get_current_time()
        end_time_stamp = time.time()
        elapsed_time = int(end_time_stamp - start_time_stamp)
        elapsed_minutes = int(elapsed_time//60)
        elapsed_seconds = elapsed_time % 60
        elapsed_time = str(elapsed_minutes)+"分"+str(elapsed_seconds)+"秒"
        if test_data_result_flag:
            test_case_result ="测试数据执行成功"
        else:
            test_case_result = "测试数据执行失败"
        excel_obj.write_cell_value(int(data[0])+1,len(data) + 2,start_time)
        excel_obj.write_cell_value(int(data[0])+1,len(data) + 3,end_time)
        excel_obj.write_cell_value(int(data[0])+1,len(data) + 4, elapsed_time)
        if test_result_flag:
            excel_obj.write_cell_value(int(data[0])+1,len(data) +5, test_case_result)
        else:
            excel_obj.write_cell_value(int(data[0]) + 1, len(data) + 5, test_case_result,"red")
    end = get_current_date() + " " + get_current_time()
    s2 = time.time()
    elapsed_time = str(s2-s1)+"秒"

    excel_obj.set_sheet_by_index(1)
    if test_result_flag:
        excel_obj.write_cell_value(row_no,test_case_result_col_no,"成功")
    else:
        excel_obj.write_cell_value(row_no, test_case_result_col_no, "失败","red")
    excel_obj.write_cell_value(row_no, test_case_start_time_col_no, start)
    excel_obj.write_cell_value(row_no, test_case_end_time_col_no, end)
    excel_obj.write_cell_value(row_no, test_case_elapsed_time_col_no, elapsed_time)


def clear_test_data_file_info(test_data_excel_file_path):
    excel_obj = Excel(test_data_excel_file_path)
    excel_obj.set_sheet_by_index(1)
    test_case_rows = excel_obj.get_rows_object()[1:]
    for test_step_row in test_case_rows:
        excel_obj.set_sheet_by_index(1)
        if test_step_row[test_case_is_executed_flag_col_no].value=="y":
            excel_obj.write_cell_value(
                int(test_step_row[test_case_id_col_no].value)+1,test_case_start_time_col_no,"")
            excel_obj.write_cell_value(
                int(test_step_row[test_case_id_col_no].value) +1, test_case_end_time_col_no, "")
            excel_obj.write_cell_value(
                int(test_step_row[test_case_id_col_no].value)+1 , test_case_elapsed_time_col_no, "")
            excel_obj.write_cell_value(
                int(test_step_row[test_case_id_col_no].value)+1 , test_case_result_col_no, "")

            excel_obj.set_sheet_by_name(test_step_row[test_case_sheet_name].value)
            test_step_rows = excel_obj.get_rows_object()[1:]
            for test_step_row in test_step_rows:
                if test_step_row[test_step_id_col_no].value is None:
                    continue
                excel_obj.write_cell_value(
                    int(test_step_row[test_step_id_col_no].value) + 1, test_step_result_col_no, "")
                excel_obj.write_cell_value(
                    int(test_step_row[test_step_id_col_no].value) + 1, test_step_error_info_col_no, "")
                excel_obj.write_cell_value(
                    int(test_step_row[test_step_id_col_no].value) + 1, test_step_capture_pic_path_col_no, "")

#从搜狗测试数据sheet中读取测试数据：[[1, '新狮子王', '搜狗视频'], [3, '钢铁侠', '搜狗百科']]
def get_test_data_from_data_sheet(test_data_excel_file_path,sheet_name):
    test_data = []
    test_data_obj = []
    excel_obj = Excel(test_data_excel_file_path)
    excel_obj.set_sheet_by_name(sheet_name)
    test_case_rows = excel_obj.get_rows_object()[1:]
    for row in test_case_rows:
        print(row)
        if row[-7].value == 'y':
            print(row[-8].value)
            test_data_obj.append(row[:-7])

    for data in test_data_obj:
        temp=[]
        for cell in data:
            temp.append(cell.value)
        test_data.append(temp)
    return test_data


if __name__ == "__main__":
    # clear_test_data_file_info(test_data_excel_file_path)
    # for test_case_sheet in get_test_case_sheet(test_data_excel_file_path):
    #     execute(test_data_excel_file_path,test_case_sheet[0],test_case_sheet[1])
    # from Util.send_mail import *
    # send_mail()
    test_data_excel_file_path = ProjDirPath + "\\TestData\\data.xlsx"
    clear_test_data_file_info(test_data_excel_file_path)
    for testcase in get_test_case_sheet(test_data_excel_file_path):
        if testcase[2] is None:
            print("****")
            execute(test_data_excel_file_path,testcase[0],testcase[1])
        else:
            execute_hybrid(test_data_excel_file_path,testcase[0],testcase[1],testcase[2])

