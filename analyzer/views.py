from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pdfminer.high_level import extract_text
from .services import extract_unique_skills, analyze_job
from .models import Resume
import json


@csrf_exempt
def upload_resume(request):
    if request.method == "POST":
        try:
            resume_file = request.FILES.get("resume_file")
            experience_years = request.POST.get("experience_years", 0)

            try:
                experience_years = float(experience_years)
            except ValueError:
                experience_years = 0

            if not resume_file:
                return JsonResponse({"error": "Missing resume file"}, status=400)

            if resume_file.size > 2 * 1024 * 1024:
                return JsonResponse({"error": "File too large (max 2MB)"}, status=400)

            resume_text = extract_text(resume_file.file)

            skills = list(extract_unique_skills(resume_text))

            Resume.objects.all().delete()

            Resume.objects.create(
                extracted_skills=skills,
                experience_years=experience_years
            )

            return JsonResponse({
                "status": "success",
                "total_skills_extracted": len(skills)
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def analyze_job_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            job_description = body.get("job_description")

            if not job_description:
                return JsonResponse({"error": "Missing job description"}, status=400)

            resume = Resume.objects.first()

            if not resume:
                return JsonResponse({"error": "No resume uploaded yet"}, status=400)

            result = analyze_job(
                resume.extracted_skills,
                job_description,
                resume.experience_years
            )

            return JsonResponse(result, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)

def resume_exists(request):
    exists = Resume.objects.exists()
    return JsonResponse({"exists": exists})