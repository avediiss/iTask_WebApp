from django import forms
from django.utils import timezone
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete', 'deadline', 'description']  # Include the deadline field in the form

    subtasks = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        help_text="Enter subtasks (up to 5) separated by a new line."
    )

    def __init__(self, *args, user=None, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.user = user  # Store the user information in the form

    def save(self, commit=True):
        instance = super(TaskForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the Task instance
        if commit:
            instance.save()

        # Process and save subtasks
        subtasks_text = self.cleaned_data['subtasks']
        self.process_and_save_subtasks(instance, subtasks_text)

        return instance

    

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()

        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be set before today.")

        return deadline


class TaskUpdateForm(TaskForm):
    class Meta:
        model = Task
        fields = ['title', 'complete', 'deadline', 'description']

    def __init__(self, *args, user=None, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.user = user  # Store the user information in the form

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()

        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be set before today.")

        return deadline

    def save(self, commit=True):
        instance = super(TaskUpdateForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the Task instance
        if commit:
            instance.save()
        return instance

