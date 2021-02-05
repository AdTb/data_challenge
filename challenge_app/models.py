from .validators import validate_file_csv,validate_file_code
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserStudent(User):
#    slug_id = models.SlugField(max_length=50)
    def __str__(self):
        return self.first_name+' '+self.last_name
    class Meta:
        verbose_name = "Utilisateur"


class FileCode(models.Model):
    submitted_by         = models.ForeignKey(to=UserStudent,on_delete=models.SET_NULL,null=True)
    date_upload          = models.DateTimeField("Date du téléversement",auto_now_add=True)
    file_uploaded        = models.FileField(upload_to= 'uploads/%Y/%m/%d/',validators = [validate_file_code])
    def __str__(self):
        return str(self.file_uploaded)
    class Meta:
        verbose_name = "Fichier de code"
        verbose_name_plural = "Fichiers de code"

class AbstractFileCsv(models.Model):
    submitted_by         = models.ForeignKey(to=UserStudent,on_delete=models.SET_NULL,null=True)
    date_upload          = models.DateTimeField("Date du téléversement",auto_now_add=True)
    file_uploaded        = models.FileField(upload_to= 'uploads/%Y/%m/%d/',validators = [validate_file_csv])
    def __str__(self):
        return str(self.file_uploaded)
    class Meta:
        abstract = True        
        verbose_name = "Fichier csv"

class FileCsv(AbstractFileCsv):
    class Meta:
        verbose_name = "Fichier csv non téléchargeable"
        verbose_name_plural = "Fichiers csv non téléchargeables"
class FileCsvOpenUpload(AbstractFileCsv):
    file_uploaded        = models.FileField(upload_to= 'uploads_storage/%Y/%m/%d/',validators = [validate_file_csv])
    class Meta:
        verbose_name = "Fichier téléchargeable"
        verbose_name_plural = "Fichiers csv téléchargeables"
"""
A given data challenge
"""
class Challenge(models.Model):
    reference               = models.OneToOneField(FileCsv,on_delete=models.CASCADE,verbose_name="Prediction de référence",related_name = 'challenge_ref')
    training_input          = models.OneToOneField(FileCsvOpenUpload,on_delete=models.CASCADE,verbose_name="Variables explicatives d'apprentissage",related_name = 'challenge_input_train')
    training_output         = models.OneToOneField(FileCsvOpenUpload,on_delete=models.CASCADE,verbose_name="Variable à expliquer d'apprentissage",related_name = 'challenge_output_train')
    test_input              = models.OneToOneField(FileCsvOpenUpload,on_delete=models.CASCADE,verbose_name="Variable explicative de test",related_name = 'challenge_input_test')
    #leaderboard             = models.ManyToManyField(Submission, through = "RankSubmission", through_fields= ('Challenge','Submission') )
    number_daily_submission = models.PositiveIntegerField(verbose_name="Nombre de soumissions quotidienne max")
    name                    = models.CharField(max_length=200,verbose_name="Titre")
    description             = models.CharField(max_length=2000)
    is_classification       = models.BooleanField(default=False)
    tuto_python             = models.CharField(max_length=200,verbose_name="Tuto python",null=True,blank=True,default= None)
    tuto_r                  = models.CharField(max_length=200,verbose_name="Tuto R",null=True,blank=True,default= None)
    def __str__(self):
        return self.name

"""
A subimssion of a result sheet in CSV for a particlar data challenge
"""
class Submission(models.Model):
    class Meta:
        order_with_respect_to = 'challenge'
        verbose_name = "Soumission"
    file_submitted       = models.OneToOneField(FileCsv,on_delete=models.CASCADE,verbose_name="Fichier de prédiction (csv)")
    date_submission      = models.DateTimeField(verbose_name="Date de la soumission",auto_now_add=True)
    submitted_by         = models.ForeignKey(to=UserStudent,on_delete=models.SET_NULL,null=True,verbose_name="Soumis par")
    score                = models.FloatField(null=True)
    challenge            = models.ForeignKey(to=Challenge,on_delete=models.SET_NULL,null=True)
    code                 = models.OneToOneField(FileCode,on_delete=models.CASCADE)
    commentaire          = models.CharField(max_length=2000)
    def __str__(self):
        return 'Sub:'+self.challenge.name+'-'+self.submitted_by.__str__()+'-' +str(self.score)
        
"""
Number of submission by an UserStudent in a particular Challenge
"""
class SubmissionCount(models.Model):
    class Meta:
        constraints = [
                        models.UniqueConstraint(fields=['UserStudent', 'Challenge'], name="assoc"),
                        ]
        verbose_name = "Compteur de soumissions"
        verbose_name_plural = "Compteurs de soumissions"
    UserStudent       = models.ForeignKey(UserStudent,on_delete=models.CASCADE,related_name="student")
    Challenge         = models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name="challengecounted")
    count_daily       = models.PositiveIntegerField(verbose_name="Nombre de soumissions du jour")
    count_total       = models.PositiveIntegerField(verbose_name="Nombre de soumissions totales")
