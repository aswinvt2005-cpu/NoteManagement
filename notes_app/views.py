from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer,NoteSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notes_app.models import NoteDb,TaskDb

# Create your views here.

class RegistrationView(APIView):
    def post(self,request):
        serializer_instance=RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)

class NotesListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes=NoteDb.objects.filter(user=request.user)
        serializer_instance=NoteSerializer(notes,many=True)
        return Response(serializer_instance.data)
    
    def post(self,request):
        serializer_instance=NoteSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class NoteRetriveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self,request,id):
        return get_object_or_404(NoteDb,id=id,user=request.user)


    def put(self,request,id):
        note=self.get_object(request,id)
        serializer=NoteSerializer(note,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request,id):
        note=self.get_object(request,id)
        note.delete()
        return Response({
            "message":"note deleted successfully"
        })
    


class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response(
            {
                "message":"logout success..!"
            }
        )

class TaskListCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        task=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(task,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        serializer_instance=TaskSerializer(data=request.data)

class TaskRetriveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)

    def get(self,request,id):
        task=self.get_task(request,id)
        serializer_instance=TaskSerializer(task)
        return Response(serializer_instance.data)

    def put(self,request,id):
        task=self.get_task(request,id)
        serializer=TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return self.response(serializer.errors)

    def delete(self,request):
        task=self.get_task(request,id)
        task.delete()
        return Response({
            "message":"task deleted successfully"
        })
    