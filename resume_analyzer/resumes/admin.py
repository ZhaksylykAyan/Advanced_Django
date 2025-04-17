from django.contrib import admin
from .models import Resume
from .models import Job

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'file')
    readonly_fields = ('parsed_data',)



@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'recruiter__username')