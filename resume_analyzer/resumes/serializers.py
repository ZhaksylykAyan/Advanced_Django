from rest_framework import serializers
from .models import Resume
from .models import Job

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'parsed_data']
        read_only_fields = ['id', 'uploaded_at', 'parsed_data']



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'created_at']
