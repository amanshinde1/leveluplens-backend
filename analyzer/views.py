from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pdfplumber
from .services import extract_unique_skills, analyze_job
from .models import Resume
import json

print("🔥 NEW VERSION RUNNING")
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

            # =========================
            # ✅ PDF TEXT EXTRACTION
            # =========================
            resume_text = ""

            try:
                with pdfplumber.open(resume_file.file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            resume_text += text + "\n"
            except Exception as e:
                print("PDF READ ERROR:", str(e))
                return JsonResponse({
                    "status": "fail",
                    "error": "Unable to process this file. Please try another PDF."
                }, status=400)

            # Debug (safe for dev, remove later if needed)
            print("=== TEXT PREVIEW ===")
            print(resume_text[:500])
            print("====================")

            # =========================
            # ✅ EXTRACTION QUALITY CHECK
            # =========================
            low_confidence = False

            if len(resume_text.strip()) < 200:
                low_confidence = True

            # =========================
            # ✅ SKILL EXTRACTION
            # =========================
            skills = list(extract_unique_skills(resume_text))

            print("Extracted skills:", skills)

            # Fallback to avoid empty system behavior
            if not skills:
                low_confidence = True
                skills = ["general"]

            # =========================
            # ✅ OPTIONAL DB STORE
            # =========================
            Resume.objects.all().delete()
            Resume.objects.create(
                extracted_skills=skills,
                experience_years=experience_years
            )

            # =========================
            # ✅ RESPONSE (TRUST-SAFE)
            # =========================
            return JsonResponse({
                "status": "success",
                "skills": skills,
                "experience": experience_years,
                "total_skills_extracted": len(skills),
                "confidence": "low" if low_confidence else "high"
            }, status=200)

        except Exception as e:
            print("UPLOAD ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def analyze_job_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            job_description = body.get("job_description")
            resume_skills = body.get("resume_skills", [])
            user_experience = body.get("user_experience", 0)

            if not job_description:
                return JsonResponse({"error": "Missing job description"}, status=400)

            if not resume_skills:
                return JsonResponse({
                    "error": "No resume skills provided"
                }, status=400)

            # ✅ STATELESS ANALYSIS
            result = analyze_job(
                resume_skills,
                job_description,
                user_experience
            )

            return JsonResponse(result, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            print("ANALYZE ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


def resume_exists(request):
    exists = Resume.objects.exists()
    return JsonResponse({"exists": exists})