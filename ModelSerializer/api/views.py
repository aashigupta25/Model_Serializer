from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Person
from .serializers import PersonSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name = 'dispatch')
class PersonAPI(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        # print(request.body)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        # print(pythondata.get('id', None))
        id = pythondata.get('id', None)
        if pythondata.get('id',None):
            per = Person.objects.get(id = id)
            serializer = PersonSerializer(per)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type = 'application/json')
        
        per = Person.objects.all()
        serializer = PersonSerializer(per, many= True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type = 'application/json')

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = PersonSerializer(data= pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'application/json')

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        per = Person.objects.get(id= id)
        serializer = PersonSerializer(per, data= pythondata, partial = True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Updated!!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'application/json') 

    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        per = Person.objects.get(id = id)
        per.delete()
        res = {'msg': 'Data Deleted!!'}
        # json_data = JSONRenderer().render(res)
        # return HttpResponse(json_data, content_type = 'application/json')
        return JsonResponse(res, safe = False)

