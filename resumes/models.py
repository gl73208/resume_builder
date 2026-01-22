from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Название резюме", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return f"{self.user.username}'s Resume #{self.id}"

class PersonalData(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_data')
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения")
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    email = models.EmailField(verbose_name="Электронная почта")
    phone = models.CharField(max_length=16, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, verbose_name="Город проживания")

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education_entries')
    institution = models.CharField(max_length=255, verbose_name="Учебное заведение", blank=True, null=True)
    faculty = models.CharField(max_length=255, verbose_name="Факультет", blank=True, null=True)
    specialty = models.CharField(max_length=255, verbose_name="Специальность", blank=True, null=True)
    end_year = models.PositiveIntegerField(verbose_name="Год окончания", blank=True, null=True)
    
class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience_entries')
    company = models.CharField(max_length=255, verbose_name="Компания")
    position = models.CharField(max_length=255, verbose_name="Должность")
    date_from = models.DateField(verbose_name="Дата начала работы")
    date_to = models.DateField(verbose_name="Дата окончания работы", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)    

class Skills(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills_entries')
    skill = models.CharField(max_length=100, verbose_name="Навык")
    LEVEL_CHOICES = [
        ('B', 'Базовый'),
        ('I', 'Средний'),
        ('A', 'Продвинутый'),
    ]
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name="Уровень")