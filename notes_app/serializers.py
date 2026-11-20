from rest_framework import serializers
from django.contrib.auth.models import User

from notes_app.models import NoteDb,TaskDb


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id","username","password","email"]

    def create(self, validated_data):
        user= User.objects.create_user(
           username=validated_data['username'],
           password=validated_data['password'],
           email=validated_data['email'] 
        )
        return user

class NoteSerializer(serializers.Serializer):
    class Meta:
        model= NoteDb
        fields="__all__"
        read_only_fields=["id","user","created_at"]

class TaskSerializer(serializers.Serializer):
    class Meta:
        model=TaskDb
        fields="__all__"
        read_only_fields=["id","user","created_date"]