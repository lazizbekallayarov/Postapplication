from django.db import models
from django.contrib.auth import get_user_model
from Postapplication.model import BaseModel

User = get_user_model()

class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Post'

    def __str__(self):
        return self.title
