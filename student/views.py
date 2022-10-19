from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import json

def readFile() -> list:
    f = open('student/student.json', 'r')
    data = json.loads(f.read())
    f.close()
    return data
# Create your views here.
# GET Request
def index(request):
    if(request.method=='GET'):
        data = readFile()
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Invalid Request")

# POST Request
def create(request):
    if(request.method=='POST'):
        data = readFile()
        data.append(json.loads(request.body))
        with open('student/student.json', 'w') as f:
            f.write(json.dumps(data))
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Invalid Request")

# PUT Request
def update(request):
    if(request.method=='PUT'):
        newData = json.loads(request.body)
        data = readFile()
        index = -1
        for i in range(len(data)):
            if(data[i]['id']==newData['id']):
                index = i
                break
        if(index!=-1):
            data[index] = newData
        else:
            data.append(newData)
        with open('student/student.json', 'w') as f:
            f.write(json.dumps(data))
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse('Invalid Request')

# DELETE Request
def remove(request):
    if(request.method=='DELETE'):
        data = readFile()
        id = json.loads(request.body)['id']
        index = -1
        for i in range(len(data)):
            if data[i]['id']==id:
                index = i
                break
        if(index!=-1):
            data.pop(index)
            with open('student/student.json', 'w') as f:
                f.write(json.dumps(data))
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse('Invalid Request')