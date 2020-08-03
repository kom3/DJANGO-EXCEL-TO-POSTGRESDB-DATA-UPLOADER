import xlrd
import pandas as pd
import os
import sys
from django.shortcuts import render
from django.http import HttpResponse
from .models import ExcelData
from .forms import ExceldataForm


# Create your views here.

def index(request):
    return  render(request, 'index.html')


def uploadFile(request):
    try:
        data = pd.read_excel(request.FILES['excel_file'])
        
    except Exception as err:
        print("error is", err)
        return HttpResponse("Failed")
    else:
        # df = pd.DataFrame(data, columns= ['Name'])
        req_cols = ['Name', 'Contact No', 'Email', 'Age', 'Position',
         'Domain', 'Address', 'Company', 'Unit']
        input_cols = [icol.upper().strip() for icol in data.columns]
        #Chek for all columns
        for col in req_cols:
            if col.upper() in input_cols:
                continue
            else:
                return HttpResponse("col_miss_error")
        _cols = data.columns
        # print(_cols)
        # print(data.index)
        #Check for empty entries in columns
        for _col in _cols:
            for idx in data.index:
                print(data[_col][idx])
                if str(data[_col][idx]) != 'nan':
                    continue
                else:
                    err_msg = "in row " + idx + ", in column " + _col
                    return HttpResponse("col_empty_error" + str(err_msg))
        #check for duplicate entries in columns
        for _col in _cols:
            temp_list = [str(data[_col][i]).strip() for i in data.index]
            print(temp_list)
            for entry in temp_list:
                if temp_list.count(entry) == 1:
                    continue
                else:
                    err_msg = "duplicate entry in row '"+ str(temp_list.index(entry)+1) +"', in column", str(_col) 
                    return HttpResponse("duplicate_entry_error: "+ str(err_msg))
        for index in (data.index):
            bfr_dump = []
            for _col in _cols:
                bfr_dump.append(data[_col][index])
            print(bfr_dump)
            #check entry not there in db
            if not ExcelData.objects.filter(name = bfr_dump[0]):
                _save = ExcelData(name = bfr_dump[0],
                    contact = bfr_dump[1], email = bfr_dump[2],
                    age = bfr_dump[3], position = bfr_dump[4], 
                    domain = bfr_dump[5], address= bfr_dump[6], 
                    company = bfr_dump[7], unit= bfr_dump[8])
                _save.save()
        return HttpResponse("Success")

def downloadfile(request):
    data_from_db = ExcelData.objects.all()
    file_path = os.path.join(os.path.dirname("__file__"), "exceluploader", "data_sheet.csv")
    ExcelData.objects.to_csv(file_path)
    with open(file_path, 'rb') as fl:
        response = HttpResponse(fl.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response