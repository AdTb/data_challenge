import os
from django.core.exceptions import ValidationError


def validate_size(value,limit):
    if value.size > limit:
        raise ValidationError('Le fichier est trop gros. La taille ne devrait pas dépasser %(size)s MiB.', params = {'size': str(value.size)})
def validate_extension(value,extensionList):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in extensionList:
       raise ValidationError('Veuillez téléverser votre fichier dans l\'un des formats suivants '+ str(extensionList))

def validate_file_code(value):
    size_limit_MB = 1
    size_limit = size_limit_MB * 1024*1024
    validate_size(value,size_limit)
    valid_extensions = ['.rmd','.r','.py','.ipynb']
    validate_extension(value,valid_extensions)
def validate_file_csv(value):
    valid_extensions = ['.csv']
    size_mb = 5
    limit = size_mb * 1024 * 1024
    validate_size(value,limit)
    validate_extension(value,valid_extensions)
    filecsv = value.open("br")
    numberline = 0
    lines = filecsv.read().decode('utf-8-sig').splitlines()
    isok=True
    for index,line in enumerate(lines):
        numberline = numberline+1
        dotencountered = False
        if(not ( line[0].isdigit() or (line[0] == '-' and line[1].isdigit()) )):
            isok=False
            break
        for charac in line[1:-1]:
            if( not (charac.isdigit() or charac == '.' or charac == ',' or charac == ' ' or charac=='-' or charac=='e') ):
                isok=False
                break
        if not isok:
            break
        #line = value.readline().decode('UTF-8')
    if not isok:
        raise ValidationError(('Le fichier n\' est pas au bon format (vérifiez au niveau de la ligne %(line)s).'),params={'line': str(numberline)},  )    

def validate_file_csv_classif(value):
    valid_extensions = ['.csv']
    size_mb = 5
    limit = size_mb * 1024 * 1024
    validate_size(value,limit)
    validate_extension(value,valid_extensions)
    filecsv = value.open("br")
    numberline = 0
    lines = filecsv.read().decode('utf-8-sig').splitlines()
    isok=True
    for index,line in enumerate(lines):
        numberline = numberline+1
        dotencountered = False
        if(not ( line[0] == '1' or (line[0] == '-' and line[1] == '1' ) )):
            isok=False
            raise ValidationError(('Le fichier n\' est pas au bon format, vous devez ne renvoyer que les valeurs \'1\' ou \'-1\', sans points. (Vérifiez au niveau de la ligne %(line)s).'),params={'line': str(numberline)},  )        
            break
        for charac in line[1:-1]:
            if( not (charac == ' ')):
                isok=False
                break
        if not isok:
            break
        #line = value.readline().decode('UTF-8')
    if not isok:
        raise ValidationError(('Le fichier n\' est pas au bon format (vérifiez au niveau de la ligne %(line)s).'),params={'line': str(numberline)},  )        
