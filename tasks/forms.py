from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS styling to widgets dynamically
        for field_name, field in self.fields.items():
            base_classes = (
                "w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-xl text-slate-100 "
                "placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                "focus:border-transparent transition-all duration-200"
            )
            # Use specific styles if necessary, otherwise apply default base classes
            field.widget.attrs['class'] = base_classes
            field.widget.attrs['placeholder'] = f"Enter {field.label.lower()}..."
            
            # Make due date optional label clear
            if field_name == 'due_date':
                field.required = False
