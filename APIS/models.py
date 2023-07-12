from django.db import models

# Create your models here.

from django.db import models
from django.db.models import JSONField

class User(models.Model):
    email = models.EmailField(primary_key=True)
    # Add other fields as needed

    def __str__(self):
        return self.email

class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    # user.queries.all() to get all the queries of a user
    query_text = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.query_text


class WorldMap(models.Model):
    keyword=models.TextField(primary_key=True)
    world_map=models.JSONField()

    def __str__(self):
        return self.keyword

class TopConversations(models.Model):
    keyword=models.TextField(primary_key=True)
    top_conversations=models.JSONField()

    def __str__(self):
        return self.keyword

class WordCloud(models.Model):
    keyword=models.TextField(primary_key=True)
    word_cloud=models.JSONField()

    def __str__(self):
        return self.keyword