from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from assets.forms import EditProfileForm, RequestInfoForm
from assets.models import UserProfile
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from .forms import RequestInfo
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClaimItemForm
from .models import Claim


# allows a user to register for an account and create a profile associated with their account
def register(request):
    print('Hello')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('Hello')
        if form.is_valid():
            objuser = form.save()
            print(objuser.id)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(request.user.id)
            objt = UserProfile(user=objuser, studentID=request.POST.get('studentID'), branch=request.POST.get('branch'),
                               year=request.POST.get('year'), phone_no=request.POST.get('phone_no'))
            print(objt)
            objt.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile_page')

    else:
        form = SignUpForm()

    print('Hello')
    return render(request, 'assets/signup.html', {'form': form})


# displays the user's profile information on a dedicated page
def profile_page(request):
    obj = UserProfile.objects.get(user_id=request.user.id)
    args = {'studentID': obj.id,
            'phone_no': obj.phone_no,
            'branch': obj.branch,
            'year': obj.year}
    return render(request, 'assets/profile_page.html', args)


# allows the user to edit their profile information
def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('/profile_page')
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'assets/edit_profile.html', context)


# allows the user to change their account password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile_page.html')
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}
    return render(request, 'assets/change_password.html', context)


# allows the user to submit a report for a found item
def report_item(request):
    if request.method == 'POST':
        item_info = request.POST.get('Item info')
        description = request.POST.get('Description')
        location = request.POST.get('Location')
        image = request.FILES.get('image')

        if image:
            # save the file to the default storage location
            file_name = default_storage.save(image.name, ContentFile(image.read()))
            file_url = default_storage.url(file_name)
        else:
            file_url = ''

        item = RequestInfo(Item_info=item_info, Description=description, Location=location, image=file_url)
        item.save()

        return redirect('home_page')

    return render(request, 'assets/report_item.html')


# displays a list of all lost and found items on the home page
def home(request):
    request_info_objects = RequestInfo.objects.all()
    context = {'request_info_objects': request_info_objects}
    return render(request, 'assets/home_page.html', context)


# displays details about a specific lost or found item
def item_details(request, item_id):
    item = get_object_or_404(RequestInfo, id=item_id)
    context = {'item': item}
    return render(request, 'assets/item_details.html', context)


# allows the user to delete a found item
def delete_item(request, item_id):
    item = get_object_or_404(RequestInfo, id=item_id)
    item.delete()
    return redirect('home_page')


# allows the user to update the details of a found item
def update_item(request, item_id):
    item = RequestInfo.objects.get(id=item_id)
    if request.method == 'POST':
        form = RequestInfoForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/home_page')
    else:
        form = RequestInfoForm(instance=item)
    return render(request, 'assets/item_update.html', {'form': form, 'item': item})


# allows the user to submit a claim for a specific found item
def claim_item(request, item_id):
    item = get_object_or_404(RequestInfo, pk=item_id)
    if request.method == 'POST':
        form = ClaimItemForm(request.POST)
        if form.is_valid():
            # create a new claim object
            claim = Claim(item=item, name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                          phone=form.cleaned_data['phone'], message=form.cleaned_data['message'])
            claim.save()  # save the claim to the database

            return redirect('item_details', item_id=item_id)
    else:
        form = ClaimItemForm()
    return render(request, 'assets/claim_item.html', {'form': form, 'item': item})


# displays a list of all claims that have been submitted for found items.
def view_claims(request):
    claims = Claim.objects.all()
    return render(request, 'assets/claims.html', {'claims': claims})
