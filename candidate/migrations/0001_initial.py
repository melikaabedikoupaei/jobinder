# Generated by Django 5.0.6 on 2024-06-08 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "candidate_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "candidate_family_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        default="candidate/default.jpg", upload_to="candidate"
                    ),
                ),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=100)),
                ("job_title", models.CharField(blank=True, max_length=255, null=True)),
                ("about_me", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Student", "Student"),
                            ("Graduate", "Graduate"),
                            ("Working", "Working"),
                            ("Not working", "Not working"),
                            ("Other", "Other"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                ("salary_expectation", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=12, null=True),
                ),
                ("linkedin_profile", models.URLField(blank=True)),
                ("github_profile", models.URLField(blank=True)),
                ("visible", models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("language_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Degree",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "degree_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("major", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "institution",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("graduation_year", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="candidate.candidate",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="candidate",
            name="language",
            field=models.ManyToManyField(to="candidate.language"),
        ),
        migrations.CreateModel(
            name="ProfessionalSkills",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skill_detail", models.TextField(blank=True, null=True)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="candidate.candidate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkExperience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=100)),
                ("job_title", models.CharField(max_length=100)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("responsibilities", models.TextField(blank=True, null=True)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="candidate.candidate",
                    ),
                ),
            ],
        ),
    ]
