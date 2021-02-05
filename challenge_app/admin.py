from django.contrib import admin
from django import forms
from django.db import models
from .models import Challenge,Submission,UserStudent,FileCsv,SubmissionCount,FileCsvOpenUpload,FileCode

class MyAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()


class UserStudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
class FileCsvAdmin(admin.ModelAdmin):
    list_display = ('file_uploaded',)
class FileCsvOpenAdmin(admin.ModelAdmin):
    list_display = ('file_uploaded',)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_by','challenge','score','date_submission')
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = MyAdminForm
class SubmissionCountAdmin(admin.ModelAdmin):
    list_display = ('UserStudent','Challenge','count_daily','count_total')
class FileCodeAdmin(admin.ModelAdmin):
    list_display = ('file_uploaded',)
admin.site.register(UserStudent,UserStudentAdmin)
admin.site.register(FileCsv,FileCsvAdmin)
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Challenge,ChallengeAdmin)
admin.site.register(FileCsvOpenUpload,FileCsvAdmin)
admin.site.register(SubmissionCount,SubmissionCountAdmin)
admin.site.register(FileCode,FileCodeAdmin)
# Register your models here.
