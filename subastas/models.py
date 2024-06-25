from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario propietario de la tarea
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)  # Campo para la imagen de la tarea

    def __str__(self):
        return self.title
