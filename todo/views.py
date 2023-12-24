# todo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from .forms import *
from .models import Task
from .forms import TaskForm, TaskUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class HomeView(View):
    template_name = 'todo/home.html'
    tasks_per_page = 10 

    def get(self, request, *args, **kwargs):
        # Get all tasks
        all_tasks = Task.objects.filter(user=request.user)

        # Get incomplete tasks
        incomplete_tasks = all_tasks.filter(complete=False)

        # Get completed tasks
        completed_tasks = all_tasks.filter(complete=True)

        page = request.GET.get('page', 1)  # Get the current page number from the request, default to 1
        paginator = Paginator(all_tasks, self.tasks_per_page)

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If the page is not an integer, deliver the first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If the page is out of range (e.g., 9999), deliver the last page.
            tasks = paginator.page(paginator.num_pages)
     
        # Calculate counts for each category
        total_tasks_count = all_tasks.count()
        incomplete_tasks_count = incomplete_tasks.count()
        completed_tasks_count = completed_tasks.count()

        return render(request, self.template_name, {
            'all_tasks': all_tasks,
            'incomplete_tasks': incomplete_tasks,
            'completed_tasks': completed_tasks,
            'total_tasks_count': total_tasks_count,
            'incomplete_tasks_count': incomplete_tasks_count,
            'completed_tasks_count': completed_tasks_count,
            'tasks': tasks,
        })

@login_required
def testing(request):
    user=request.user
    tasks = Task.objects.filter(user=user)
    return render(request, 'todo/testing.html', {'tasks': tasks})



    
def calendar(request):
    return render(request, 'todo/calendar.html')

#def home(request):
#	return render(request, 'home.html')
	

def todo_list(request):
    # Your original view logic without tasks
    return render(request, 'todo/list.html')

@login_required
def todo_list_with_tasks(request):
    user=request.user
    tasks = Task.objects.filter(user=user)
    return render(request, 'todo/home.html', {'tasks': tasks})



# views.py

def update_task(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        # Include the instance and user in the form instantiation
        update_form = TaskUpdateForm(request.POST, instance=task, user=request.user)
        if update_form.is_valid():
            # Update the task with the form data
            update_form.save()

            # Redirect to the task list
            return redirect('testing')

    else:
        # Create the form with initial data from the task and set the user
        update_form = TaskUpdateForm(instance=task, user=request.user)

    return render(request, 'todo/update_task.html', {'update_form': update_form, 'task': task})




def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('testing')

    context = {'item':item}
    return render(request, 'todo/delete.html', context)


def create_task(request):
    user = request.user
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Process the form data, including the selected deadline
            title = form.cleaned_data['title']
            
            # Get the selected deadline from the form or None if not selected
            deadline = form.cleaned_data['deadline']
            
            description = form.cleaned_data['description']
     

            # Check if the deadline is before today
            if deadline and deadline < timezone.now().date():
                form.add_error('deadline', 'Deadline cannot be set before today.')
                return render(request, 'todo/testing.html', {'form': form})

            # Save the task to the database
            task = Task(user=user, title=title, deadline=deadline, description=description)
            task.save()

            # Redirect to a success page or the task list
            return redirect('testing')  # Update with your URL name

    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=user)
    context = {'tasks': tasks, 'form': form}
    return render(request, 'todo/list.html', context)



def task_description(request, task_id):
  
    task = get_object_or_404(Task, pk=task_id)
  
    
    # Pass the task description to the template
    context = {
        'task': task,
     
    }
    task.save()
    return render(request, 'todo/task_description.html', context)