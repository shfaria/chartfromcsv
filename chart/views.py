from multiprocessing import context
from typing import Counter
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from numpy import row_stack
import pandas as pd

def home(request):
    
    global attribute1
    context= {}
    if request.method == 'POST':
        # the id in the form
        uploaded_file = request.FILES['document']
        attribute1 = request.POST.get('attributeid')
        # print(uploaded_file)
        # print(attribute1)

        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            # whre to save files
            d = os.getcwd()
            file_directory = d + '/media/' + name
            readfile(file_directory)
            return redirect(results)
        else:
            messages.warning(request, 'cant upload file. please use csv format')

    return render(request, 'chart/index.html')


def readfile(filename):
    global rows, columns, data, afile, missingvalues
    afile= pd.read_csv(filename, sep='[:;,_|]', engine='python')
    print(afile)
    data = pd.DataFrame(data= afile, index=None)
    print(data)
    
    # rows and colums
    rows = len(data.axes[0])
    columns = len(data.axes[1])

    # find mssing
    missingsigns = ['?', '0', '--', ' ']
    nulldata = data[data.isnull().any(axis=1)]
    
    missingvalues = len(nulldata)
    print(missingvalues)
    


def results(request):
    message = 'there are ' + str(rows) + ' rows and ' + str(columns)+ ' columns and missing data are ' + str(missingvalues)

    messages.warning(request, message)

    # splitting data into keys and values based on attributes
    dashboard = []

    for x in data[attribute1]:
        dashboard.append(x)

    dashboard1 = dict(Counter(dashboard))
    print("my dashboard ", dashboard1)

    keys =  dashboard1.keys()
    values = dashboard1.values()

    print(keys)
    print(values)

    listkeys = list(keys)
    listvalues = list(values)
    print(listkeys)
    print(listvalues)

    context = {
        'listkeys': listkeys,
        'listvalues': listvalues,
    }


    return render(request, 'chart/results.html', context)
