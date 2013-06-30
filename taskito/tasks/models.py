from django.db import models
from django.contrib.auth.models import User
from base.snippets import unique_slugify


class Task(models.Model):
    creator = models.ForeignKey(User, verbose_name="Creator")
    name = models.CharField(max_length=200, verbose_name="Name")
    slug = models.SlugField(blank=True, null=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated = models.DateTimeField(blank=True, null=True, verbose_name="Date updated")
    allow_comments = models.BooleanField(default=True, verbose_name="Allow comments")
    progress = models.PositiveIntegerField(max_length=3, verbose_name="Progress")
    comment_count = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        unique_slugify.unique_slugify(self, self.name)
        super(Task, self).save(*args, **kwargs)


class Comment(models.Model):
    task = models.ForeignKey(Task, verbose_name="Task")
    content = models.TextField(verbose_name="Message")
    user_email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    user_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Username")
    user = models.ForeignKey(User, blank=True, null=True, verbose_name="User")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
