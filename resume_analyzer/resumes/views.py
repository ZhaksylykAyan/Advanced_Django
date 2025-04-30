from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume, Job
from .serializers import ResumeUploadSerializer, JobSerializer
from .utils import extract_text, analyze_resume
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class ResumeUploadView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        text = extract_text(resume.file.path)
        parsed_data = analyze_resume(text)
        resume.parsed_data = parsed_data
        resume.save()

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только свои резюме
        return Resume.objects.filter(user=self.request.user)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['get'])
    def match_resumes(self, request, pk=None):
        job = self.get_object()
        resumes = Resume.objects.all()

        matches = []
        for resume in resumes:
            skills = resume.parsed_data.get('skills', []) if resume.parsed_data else []
            match_score = len(set(skills) & set(job.required_skills)) / max(len(job.required_skills), 1)
            matches.append({
                'resume_id': resume.id,
                'username': resume.user.username,
                'score': round(match_score * 100, 2),
                'skills_matched': list(set(skills) & set(job.required_skills)),
            })

        sorted_matches = sorted(matches, key=lambda x: -x['score'])
        return Response(sorted_matches)