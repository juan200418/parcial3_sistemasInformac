from django.forms import ModelForm
from .models import Task
class TaskForm(ModelForm):
    class meta: 
        model = Task
        fieds = ['title', 'descripcion','image','important ']

