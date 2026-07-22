from django.db import models
from datetime import datetime


class School(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    subdomain = models.SlugField(unique=True, help_text="Subdomain for the school (e.g., 'school1')")
    database_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    website = models.URLField(blank=True, null=True)
    google_map_embed_url = models.TextField(blank=True, null=True, help_text="Google Maps iframe src URL")
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    about_description = models.TextField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)

    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    slider_image_1 = models.ImageField(upload_to='school_sliders/', blank=True, null=True)
    slider_image_2 = models.ImageField(upload_to='school_sliders/', blank=True, null=True)
    slider_image_3 = models.ImageField(upload_to='school_sliders/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.subdomain:
            self.subdomain = self.slug
        if not self.database_name:
            self.database_name = f"school_{self.subdomain.replace('-', '_')}"

        using = kwargs.pop('using', None)
        if using and using != 'default':
            super().save(using=using, *args, **kwargs)
            return

        super().save(*args, **kwargs)

        # Sync this School record into the tenant database so FK constraints work
        if self.database_name:
            from django.db import connections
            from django.conf import settings
            db_name = self.database_name
            if db_name not in connections:
                new_config = connections.databases['default'].copy()
                new_config['NAME'] = db_name
                connections.databases[db_name] = new_config
                settings.DATABASES[db_name] = new_config
            super().save(using=db_name, force_insert=False)

    def __str__(self):
        return self.name

    @property
    def years_since_established(self):
        if self.established_year:
            return datetime.now().year - self.established_year
        return None

    @property
    def student_count(self):
        return self.students.count()

    @property
    def teacher_count(self):
        return self.teachers.count()


class SchoolEvent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='school_events/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Event #{self.pk}"

    class Meta:
        ordering = ['-event_date']
