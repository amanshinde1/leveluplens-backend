from django.urls import path
from . import views

urlpatterns = [
    path("analyze-job", views.analyze_job_view),
    path("upload-resume", views.upload_resume),
    path("resume-exists", views.resume_exists),
]