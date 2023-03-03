from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from assets.forms import EditProfileForm
from assets.models import UserProfile
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import RequestInfo


"""This code is a view function called "home" that handles an HTTP request. When the view is called, 
it retrieves all objects in the "ItemInfo" model and stores them in the variable "data". The function then returns a 
rendered template called "assets/home_page.html", along with the data from "ItemInfo" passed as context to the template. """

"""
def item_list(request):
    items = ItemInfo.objects.all()
    context = {
        "items": items
    }
    return render(request, "items.html", context)
    
    def home(request):
    item = ItemData.objects.all()
    context = {
        "item": item
    }
    return render(request, 'assets/home_page.html', context)

"""

"""This code is a view function, named register. It handles user registration in the application. If the 
request method is POST, it means that the form has been submitted, and it validates the data in the form by using the 
SignUpForm. If the form is valid, it saves the user data into the database, authenticates the user, and logs them in. 
If the form is not valid, the user is redirected to the signup page. If the request method is not POST, it means that 
the form has not been submitted yet, and the code will simply render the signup form for the user. """


# sighup
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


"""This code defines a view named "profile", which retrieves information about a user profile from the 
database and displays it on a template. The user profile information is retrieved using the "UserProfile" model and 
the "request.user.id" value, which represents the currently logged-in user. The retrieved information includes the 
student ID, phone number, branch, and year. The information is passed as context to the template 
"assets/profile_page.html" and is rendered in the HTML response that is returned to the user's browser. """


def profile_page(request):
    obj = UserProfile.objects.get(user_id=request.user.id)
    args = {'studentID': obj.id,
            'phone_no': obj.phone_no,
            'branch': obj.branch,
            'year': obj.year}
    return render(request, 'assets/profile_page.html', args)


"""This code implements the functionality for editing a user's profile. The code starts by creating a form using the 
EditProfileForm with either the POST data from the request or the instance of the current user. If the form is valid, 
it saves the changes to the user profile and redirects the user to the profile page. If the form is not valid, 
the code passes the form to the template for rendering in the context and returns a page that allows the user to edit 
their profile information. """


def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('/profile_page')
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'assets/edit_profile.html', context)


"""This code is for changing the password of a user in Django. The PasswordChangeForm class is used to handle the 
form for changing the password. The code checks if the request method is a 'POST' and if the form is valid. If both 
conditions are met, the form data is saved, the user's session authentication hash is updated, and the user is 
redirected to their profile page. The code then renders the change_password.html page, passing the form as context. """


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


"""This code implements a view function for creating a request for a lost item. The function is triggered when a user 
submits a POST request to the endpoint. When the function is triggered, it creates a new RequestInfo object in the 
database with the studentID, Description, and Location information provided in the POST request. Finally, 
the function returns a rendering of the assets/request_item.html template. """

"""
def request_item(request):
    if request.method == 'POST':
        obj = RequestInfo.objects.create(
            id=request.POST.get('id'),
            Item_info=request.POST.get('Item info'),
            Description=request.POST.get('Description'),
            Location=request.POST.get('Location')
        )
    return render(request, 'assets/request_item.html')


"""

"""
def request_item(request):
    if request.method == 'POST':
        item_info = request.POST.get('Item info')
        description = request.POST.get('Description')
        location = request.POST.get('Location')

        item = RequestInfo(Item_info=item_info, Description=description, Location=location)
        item.save()

        return redirect('home_page')

    return render(request, 'assets/request_item.html')
"""

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def request_item(request):
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

    return render(request, 'assets/request_item.html')


def home(request):
    request_info_objects = RequestInfo.objects.all()
    context = {'request_info_objects': request_info_objects}
    return render(request, 'assets/home_page.html', context)


def item_details(request, item_id):
    item = get_object_or_404(RequestInfo, id=item_id)
    context = {'item': item}
    return render(request, 'assets/item_details.html', context)


def delete_item(request, item_id):
    item = get_object_or_404(RequestInfo, id=item_id)
    item.delete()
    return redirect('home_page')










