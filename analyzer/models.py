from django.db import models


class Resume(models.Model):

    extracted_skills = models.JSONField()

    experience_years = models.FloatField(default=0)

    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume updated at {self.uploaded_at}"