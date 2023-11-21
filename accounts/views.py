from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from django.contrib.auth import login , authenticate
from django.urls import reverse
from .models import Profile
from .forms import UserForm , ProfileForm
from django.contrib.auth.decorators import login_required
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect('accounts:profile')

    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request , 'registration/signup.html' , context)


@login_required(login_url='/accounts/login/')
def profile(request):
    profile1 = Profile.objects.all()
    profile = Profile.objects.get(user=request.user)
    return render(request,'accounts/profile.html',{'profile': profile, 'profile1':profile1})


def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method=='POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse('accounts:profile'))

    else :
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'accounts/profile_edit.html',{'userform':userform , 'profileform':profileform})