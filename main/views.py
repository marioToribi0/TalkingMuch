from urllib import response
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
from django.core.files import File
from django.core.files.storage import FileSystemStorage

# Tempory files
import tempfile
import os

from .forms import ReaderForm, DataForm

# Imaginary function to handle an uploaded file.
from .lectorWhatsapp import Archivo

def index(response):
    return render(response, 'main/index.html')

def forms(response):
    if response.method == 'POST':
        form = DataForm(response.POST)
        if form.is_valid():
            result = []
            size = int(form.cleaned_data.get('size'))
            redirect_file = False
            for option in range(size):
                actual_option = form.cleaned_data.get(f'options_{option+1}')
                option_result = {}
                option_result['option'] = actual_option
                
                if (actual_option=='2'):
                    option_result['words'] = form.cleaned_data.get('words')
                    option_result['letters'] = form.cleaned_data.get('letters')
                elif (actual_option=='3'):
                    option_result['date'] = form.cleaned_data.get('date')
                    option_result['cant'] = form.cleaned_data.get('cant')
                elif (actual_option=='4'):
                    option_result['phrase'] = form.cleaned_data.get('phrase')
                elif (actual_option=='1'):
                    ## Redirect to show file
                    redirect_file = True
                
                result.append(option_result)
            
            response.session['redirect_file'] = redirect_file
            response.session['data'] = result
                
        return redirect('upload')
    else:
        form = DataForm()
    
    return render(response, 'main/forms.html', {'form': form})

def upload(response):
    
    # Redirect if not exist the data
    data = response.session.get('data', None)
    if data==None:
        return redirect('forms')
    redirect_file = response.session.get('redirect_file', None)
    
    if response.method == 'POST':
        form = ReaderForm(response.POST, response.FILES)
        if form.is_valid():
            file = form.cleaned_data.get('file')
            obj = form.save(commit=False)
            obj.file = file
            obj.save()

            file = Archivo(obj.file.path)
            
            content = []
            
            # Analize data
            for i,action in enumerate(data):
                if int(action['option']) == 1:
                    
                    # Tempory file
                    tmp = tempfile.NamedTemporaryFile()
                    
                    fd, path = tempfile.mkstemp()
                    try:
                        with os.fdopen(fd, 'w+') as tmp:
                            # do stuff with temp file
                            file.generateFile(tmp)
                            tmp.seek(0)
                            content.append((1,tmp.read()))
                    finally:                        
                        os.remove(path)      

                elif int(action['option']) == 2:
                    words = data[i].get('words')
                    letters = data[i].get('letters')
                    results = file.bestWords(int(words), int(letters))
                    
                    content.append((2,results))
                                      
                    
                elif int(action['option']) == 3:
                    periods = ["day", "month", "year", "hour"]
                    date = periods[int(data[i].get("date"))-1]
                    cant = data[i].get("cant")
                    
                    results = file.frequencyPeriod(tuple=(date,int(cant)))
                    
                    content.append((3,results))     
                    
                elif int(action['option']) == 4:
                    phrase = data[i].get('phrase')
                    
                    results = file.countPhrases(phrase)

                    content.append((4,results))          
                    
                elif int(action['option']) == 5:
                    results = file.mostTalked()
                    
                    content.append((5,results))            
                    
                elif int(action['option']) == 6:
                    results = file.returnTupleWordPeople(10)
                    
                    content.append((6,results))            
                    
                elif int(action['option']) == 7:
                    results = file.messageDelete()
                    
                    content.append((7,results))            
            del file
            os.remove(obj.file.path)
            
            response.session['results'] = content;
            return redirect('results')
            
    else:
        form = ReaderForm()
    return render(response, 'main/upload.html', {'form': form, 'redirect_file': redirect_file})

def results(response):
    
    # Redirect if not exist the data
    redirect_file = response.session.get('redirect_file', None)
    
    results = response.session.get('results', None)
    if results==None:
        return redirect('forms')
    
    send_dict = {'results': results, 'check': False}
    
    
    if redirect!=None:
        send_dict['redirect'] = redirect
        send_dict['check'] = True
    
    return render(response, 'main/results.html', send_dict)

def file_result(response):
    data = response.session.get('results')
    if data==None:
        return redirect('forms')
    
    content = None
    for i in range(len(data)):
        if (int(data[i][0])==1):
            content = data[i][1]
    
    if content==None:
        return redirect('forms')
     
    return HttpResponse(content, content_type="text/plain")