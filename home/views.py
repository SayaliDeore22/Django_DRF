import io
from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


def student_deatils(request, pk):
    std = Student.objects.get(id=pk)
    serializer = StudentSerializer(std)
    json_data = JSONRenderer(). render(serializer.data)
    return HttpResponse(json_data, content_type="application/json")


def student_list(request):
    std = Student.objects.all()
    serializer = StudentSerializer(std, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def student_create(request):
    if request.method == "GET":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get("id", None)
        if id is not None:
            std = Student.objects.get(id=id)
            serializer = StudentSerializer(std.data)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type="application/json")
        std = Student.objects.all()
        serializer = StudentSerializer(std, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")

    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=python_data)

        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data created!!"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json")

    if request.method == "PUT":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get("id")
        std = Student.objects.get(id=id)
        serializer = StudentSerializer(std, data=python_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data Updated"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json")

    if request.method == "DELETE":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get("id")
        std = Student.objects.get(id=id)
        std.delete()
        res = {"msg": "Data Deleted"}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type="application/json")
