from django.db import models


class LanguageChoice(models.TextChoices):
    PY = "py", "Python"
    JS = "js", "JavaScript"
    CPP = "cpp", "C++"
    OTHER = "other", "Other"