from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import FileCsvForm,SubmissionForm,SubmissionClassForm
from .models import Challenge,UserStudent,Submission,FileCsv,FileCode
from django.urls import reverse
from django.conf import settings
from .machinelearning import get_score
from django.contrib.auth import authenticate, login
from datetime import datetime,timedelta
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('challenges'))
        else:
           return render(request, 'login.html', {'error_message': 'Impossible de vous authentifier'})
    else:
        return render(request, 'login.html')
@login_required(login_url='login')
def show_all_challenges(request):
    challenges= Challenge.objects.all()
    return render(request, 'challengelist.html', {'challenges':  challenges})

def maintenance(request):
    return render(request,'maintenance.html')

@login_required(login_url='login')
def get_leaderboard(request,id_challenge):
    try:
        challenge = Challenge.objects.get(pk=id_challenge)
    except Challenge.DoesNotExist:
        raise Http404("Challenge does not exist")
    # Get the best submissions
    best_sub_pk = []
    for ustudent in UserStudent.objects.all():
        best_submission =  Submission.objects.filter(challenge__pk = id_challenge,submitted_by_id =ustudent.id ).order_by('score')
        if not(best_submission is None):
            if len(best_submission)>0:
                best_sub_pk.append(best_submission[0].pk)
    leaderboard = Submission.objects.filter(challenge__pk = id_challenge,pk__in = best_sub_pk).order_by('score')
    score_user = request.GET.get('score',None)
    return render(request, 'showchallenge.html', {'challenge':  challenge, 'leaderboard':leaderboard, 'training_input_url': challenge.training_input.file_uploaded.url, 'training_output_url': challenge.training_output.file_uploaded.url,'test_input_url':  challenge.test_input.file_uploaded.url,'score_user':score_user})

@login_required(login_url='login')
def upload_file(request,id_challenge):
    try:
        challenge = Challenge.objects.get(pk=id_challenge)
    except Challenge.DoesNotExist:
        raise Http404("Challenge does not exist")
    try: 
        user_submission = UserStudent.objects.get(pk=request.user.id)
    except UserStudent.DoesNotExist:
        return render(request, 'upload.html', {'challenge': challenge, 'error_message'  : 'You are not registered as student, you cannot upload a file to this challenge.' })
    subcount = Submission.objects.filter(submitted_by_id = user_submission.id, challenge=challenge , date_submission__gte = datetime.now().replace(hour=0,minute=0,second=1)).count()
    if subcount >= challenge.number_daily_submission:
        return render(request, 'upload.html', {'challenge': challenge, 'error_message' : 'You have reached the daily limit of '+str(challenge.number_daily_submission)+' submissions to this challenge. You will be able to upload a new prediction tomorrow.' })
    is_classification = challenge.is_classification
    if request.method == 'POST':
        if is_classification:   
            form = SubmissionClassForm(request.POST, request.FILES)
        else:
            form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            filecsv =FileCsv(submitted_by = user_submission,file_uploaded = data['file_submitted'])
            code =FileCode(submitted_by = user_submission,file_uploaded = data['code'])
            new_submission = Submission(submitted_by = user_submission, file_submitted = filecsv,code = code,commentaire = data['commentaire'], challenge = challenge, score = None)
            filecsv.save()
            code.save()
            try:
                score = get_score(settings.MEDIA_ROOT+challenge.reference.file_uploaded.name,settings.MEDIA_ROOT+filecsv.file_uploaded.name,is_classification)
            except ValueError as e:
                return  render(request, 'upload.html', {'form': form, 'challenge': challenge, 'error_message' : "Nous avons rencontré l'erreur suivante lors de la soumission de votre prédiction: \'"+str(e)+"\'. Ce problème est peut-être dû à une mauvaise dimension de votre vecteur de prédiction. Avez-vous vérifié qu'il avait le bon nombre de lignes et de colonnes?" })
            new_submission.score = score          
            new_submission.save()
            if is_classification:
              score_string = "{:12.5f}".format(score)
            else:
              score_string = "{:12.2f}".format(score)
            return HttpResponseRedirect(reverse('leaderboard',args=[id_challenge])+"?score="+score_string)
    else:
        form = SubmissionForm()
    return render(request, 'upload.html', {'form': form, 'challenge': challenge })            
