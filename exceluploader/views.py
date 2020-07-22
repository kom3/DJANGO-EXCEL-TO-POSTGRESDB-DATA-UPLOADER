from django.shortcuts import render
from django.http import HttpResponse
import xlrd
import pandas as pd
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
                    return HttpResponse("col_empty_error")
        #check for duplicate entries in columns
        for _col in _cols:
            temp_list = [str(data[_col][i]).strip() for i in data.index]
            print(temp_list)
            for entry in temp_list:
                if temp_list.count(entry) == 1:
                    continue
                else:
                    print("duplicate entry in column '"+ str(_col) +"' at row", temp_list.index(entry)+1)
                    return HttpResponse("duplicate_entry_error")
        for index in (data.index):
            bfr_dump = []
            for _col in _cols:
                bfr_dump.append(data[_col][index])
            print(bfr_dump)
            _save = ExcelData(name = bfr_dump[0],
                contact = bfr_dump[1], email = bfr_dump[2],
                age = bfr_dump[3], position = bfr_dump[4], 
                domain = bfr_dump[5], address= bfr_dump[6], 
                company = bfr_dump[7], unit= bfr_dump[8])
            _save.save()
        return HttpResponse("Success")