from django import forms
from .models import Resume, PersonalData, Education, Experience, Skills

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title']

class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = [
            'first_name', 'last_name', 'patronymic', 
            'birth_date', 'gender', 'email', 'phone', 'city'
        ]

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'faculty', 'specialty', 'end_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'date_from', 'date_to', 'description']

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill', 'level']