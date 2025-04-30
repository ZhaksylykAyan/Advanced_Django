from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ResumeUploadView, JobViewSet

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resumes')
router.register(r'jobs', JobViewSet, basename='jobs')

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('', include(router.urls)),
]