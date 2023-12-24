# models.py
from django.db import models
from django.contrib.auth import get_user_model




class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(null=True)
   

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.complete:
            self.subtasks.all().update(complete=True)

        print("Task saved.")
        
            


