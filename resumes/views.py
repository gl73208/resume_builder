from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Resume, PersonalData, Education, Experience, Skills
from .forms import ResumeForm, PersonalDataForm, EducationForm, ExperienceForm, SkillsForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

def home(request):
    return render(request, 'base.html')  

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'login.html') 
    
    return render(request, 'login.html')

@login_required
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes})

@login_required
def resume_create(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        personal_data_form = PersonalDataForm(request.POST)

        if resume_form.is_valid() and personal_data_form.is_valid():
            # Сохраняем резюме
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()

            # Сохраняем персональные данные
            personal_data = personal_data_form.save(commit=False)
            personal_data.resume = resume
            personal_data.save()

            # Обработка полей образования
            education_count = 0
            while f"institution_{education_count}" in request.POST:
                institution = request.POST.get(f"institution_{education_count}")
                faculty = request.POST.get(f"faculty_{education_count}")
                specialty = request.POST.get(f"specialty_{education_count}")
                end_year = request.POST.get(f"end_year_{education_count}")

                if institution or faculty or specialty or end_year:
                    Education.objects.create(
                        resume=resume,
                        institution=institution,
                        faculty=faculty,
                        specialty=specialty,
                        end_year=end_year
                    )
                education_count += 1

            # Обработка полей опыта работы
            experience_count = 0
            while f"company_{experience_count}" in request.POST:
                company = request.POST.get(f"company_{experience_count}")
                position = request.POST.get(f"position_{experience_count}")
                date_from = request.POST.get(f"date_from_{experience_count}")
                date_to = request.POST.get(f"date_to_{experience_count}")
                description = request.POST.get(f"description_{experience_count}")

                if company or position or date_from or date_to or description:
                    Experience.objects.create(
                        resume=resume,
                        company=company,
                        position=position,
                        date_from=date_from,
                        date_to=date_to,
                        description=description
                    )
                experience_count += 1

            # Обработка полей навыков
            skills_count = 0
            while f"skill_{skills_count}" in request.POST:
                skill = request.POST.get(f"skill_{skills_count}")
                level = request.POST.get(f"level_{skills_count}")

                if skill and level:
                    Skills.objects.create(
                        resume=resume,
                        skill=skill,
                        level=level
                    )
                skills_count += 1

            return redirect('my_resumes')
    else:
        resume_form = ResumeForm()
        personal_data_form = PersonalDataForm()

    return render(request, 'resumes/create_resume.html', {
        'resume_form': resume_form,
        'personal_data_form': personal_data_form
    })

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    personal_data = resume.personal_data
    education_entries = resume.education_entries.all()
    experience_entries = resume.experience_entries.all()
    skills_entries = resume.skills_entries.all() 
    
    return render(request, 'resumes/resume_detail.html', {
        'resume': resume,
        'personal_data': personal_data,
        'education_entries': education_entries,
        'experience_entries': experience_entries,
        'skills_entries': skills_entries, 
    })

@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    personal_data = resume.personal_data
    education_entries = resume.education_entries.all()
    experience_entries = resume.experience_entries.all()
    skills_entries = resume.skills_entries.all()  

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, instance=resume)
        personal_data_form = PersonalDataForm(request.POST, instance=personal_data)

        if resume_form.is_valid() and personal_data_form.is_valid():
            resume_form.save()
            personal_data_form.save()

            # Обработка существующих записей об образовании
            for education in education_entries:
                delete_key = f"delete_education_{education.pk}"
                if delete_key in request.POST:
                    education.delete()
                else:
                    education.institution = request.POST.get(f"institution_{education.pk}")
                    education.faculty = request.POST.get(f"faculty_{education.pk}")
                    education.specialty = request.POST.get(f"specialty_{education.pk}")
                    education.end_year = request.POST.get(f"end_year_{education.pk}")
                    education.save()

            # Обработка новых записей об образовании
            education_count = education_entries.count()
            while True:
                institution = request.POST.get(f"institution_{education_count}")
                faculty = request.POST.get(f"faculty_{education_count}")
                specialty = request.POST.get(f"specialty_{education_count}")
                end_year = request.POST.get(f"end_year_{education_count}")

                if not (institution or faculty or specialty or end_year):
                    break

                Education.objects.create(
                    resume=resume,
                    institution=institution,
                    faculty=faculty,
                    specialty=specialty,
                    end_year=end_year
                )
                education_count += 1

            # Обработка существующих записей об опыте работы
            for experience in experience_entries:
                delete_key = f"delete_experience_{experience.pk}"
                if delete_key in request.POST:
                    experience.delete()
                else:
                    experience.company = request.POST.get(f"company_{experience.pk}")
                    experience.position = request.POST.get(f"position_{experience.pk}")
                    experience.date_from = request.POST.get(f"date_from_{experience.pk}")
                    experience.date_to = request.POST.get(f"date_to_{experience.pk}")
                    experience.description = request.POST.get(f"description_{experience.pk}")
                    experience.save()

            # Обработка новых записей об опыте работы
            experience_count = experience_entries.count()
            while True:
                company = request.POST.get(f"company_{experience_count}")
                position = request.POST.get(f"position_{experience_count}")
                date_from = request.POST.get(f"date_from_{experience_count}")
                date_to = request.POST.get(f"date_to_{experience_count}")
                description = request.POST.get(f"description_{experience_count}")

                if not (company or position or date_from or date_to or description):
                    break

                Experience.objects.create(
                    resume=resume,
                    company=company,
                    position=position,
                    date_from=date_from,
                    date_to=date_to,
                    description=description
                )
                experience_count += 1

            # Обработка существующих записей о навыках
            for skill in skills_entries:
                delete_key = f"delete_skill_{skill.pk}"
                if delete_key in request.POST:
                    skill.delete()
                else:
                    skill.skill = request.POST.get(f"skill_{skill.pk}")
                    skill.level = request.POST.get(f"level_{skill.pk}")
                    skill.save()

            # Обработка новых записей о навыках
            skills_count = skills_entries.count()
            while True:
                skill = request.POST.get(f"skill_{skills_count}")
                level = request.POST.get(f"level_{skills_count}")

                if not (skill and level):
                    break

                Skills.objects.create(
                    resume=resume,
                    skill=skill,
                    level=level
                )
                skills_count += 1

            return redirect('my_resumes')
    else:
        resume_form = ResumeForm(instance=resume)
        personal_data_form = PersonalDataForm(instance=personal_data)

    return render(request, 'resumes/edit_resume.html', {
        'resume_form': resume_form,
        'personal_data_form': personal_data_form,
        'education_entries': education_entries,
        'experience_entries': experience_entries,
        'skills_entries': skills_entries,  
        'resume': resume,
    })
    
@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('my_resumes')
    return render(request, 'resumes/delete_resume.html', {'resume': resume})
    
@login_required
def resume_export_pdf(request, pk):
    # Получаем резюме и связанные данные
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    personal_data = resume.personal_data
    education_entries = resume.education_entries.all()
    experience_entries = resume.experience_entries.all()
    skills_entries = resume.skills_entries.all()

    # Рендерим HTML-шаблон с данными резюме
    html_string = render_to_string('resumes/resume_pdf.html', {
        'resume': resume,
        'personal_data': personal_data,
        'education_entries': education_entries,
        'experience_entries': experience_entries,
        'skills_entries': skills_entries,
    })

    # Конвертируем HTML в PDF с помощью WeasyPrint
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()

    # Возвращаем PDF как HTTP-ответ
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume.pk}.pdf"'
    return response