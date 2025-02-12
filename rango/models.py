from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)  # Added views field
    likes = models.IntegerField(default=0)  # Added likes field
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=Category.NAME_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=1)

    def __str__(self):
        return self.title


# Create your models here.
