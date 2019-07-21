from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=150, default="Без названия.")
    home = models.CharField(max_length=50, default="Вне домика")
    text = models.TextField()
    solved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,  related_name='liked')
    curator = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name='curatored')
    date = models.DateField(("Date"), default=datetime.date.today)
    progress = models.BooleanField(default=False)

    def countlikes(self):
        return self.likes.count()