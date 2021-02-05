from django.forms import ModelForm,Form,FileField,CharField,Textarea
from .models import Submission,FileCsv,FileCode
from .validators import validate_file_code,validate_file_csv,validate_file_csv_classif
class SubmissionForm(Form):
    file_submitted = FileField(validators = [validate_file_csv],label="Fichier de prédiction (.csv)")
    code = FileField(validators = [validate_file_code],label="Votre code")
    commentaire = CharField(max_length=2000,widget = Textarea)
class SubmissionClassForm(Form):
    file_submitted = FileField(validators = [validate_file_csv_classif],label="Fichier de prédiction (.csv)")
    code = FileField(validators = [validate_file_code],label="Votre code")
    commentaire = CharField(max_length=2000,widget = Textarea)
class FileCodeForm(ModelForm):
    class Meta:
        model = FileCsv
        fields = ['file_uploaded']   
class FileCsvForm(ModelForm):
    class Meta:
        model = FileCsv
        fields = ['file_uploaded']
