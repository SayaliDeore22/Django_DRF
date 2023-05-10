from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import StudentSerializer
from .models import Student


@api_view(["GET", "POST", "PUT", "DELETE"])
def student_api(request):
    if request.method == "GET":
        id = request.data.get("id")
        if id is not None:
            std = Student.objects.get(id=id)
            serializer = StudentSerializer(std)
            return Response(serializer.data)
        std = Student.objects.all()
        serializer = StudentSerializer(std, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created!!"})
        return Response(serializer.errors)

    if request.method == "PUT":
        id = request.data.get("id")
        std = Student.objects.get(id=id)
        serializer = StudentSerializer(std, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Updated"})
        return Response(serializer.errors)

    if request.method == "DELETE":
        id = request.data.get("id")
        std = Student.objects.get(id=id)
        std.delete()
        return Response({"msg": "Data Deleted"})