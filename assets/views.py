from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from assets.forms import SignUpForm, EditProfileForm
from assets.models import UserProfile, ItemInfo, RequestInfo, ClaimInfo
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages

"""
The claim view handles a claim request made by a user. 
The view retrieves an ItemInfo object from the database using the id argument passed in the URL. 
If the request method is not a POST request, the view returns a render response that displays the 
assets/claim.html template with the item object passed as context. If the request method is a POST
 request, the view retrieves the location claimed by the user and the actual location of the item 
 from the request.POST data. Then, the view checks if the claimed location is contained in the actual 
 location or if the actual location is contained in the claimed location, and sets the claim_success 
 flag accordingly. If the claim is successful, the view creates a new ClaimInfo object with the 
 user ID, the claimed location, and the item ID, and saves it to the database. 
 Finally, the view returns a render response that displays the assets/claim.html template with the 
 item, status, and post values passed as context.
"""


def claim(request, id):
    item = get_object_or_404(ItemInfo, pk=id)

    if request.method != 'POST':
        return render(request, 'assets/claim.html', {'item': item})

    location_claim = request.POST.get('Location').lower()
    item_info = ItemInfo.objects.get(pk=request.POST.get('ItemID'))
    location_actual = item_info.Location.lower()
    claim_success = location_actual in location_claim or location_claim in location_actual

    if claim_success:
        ClaimInfo.objects.create(
            UserID=request.user,
            Location=location_claim,
            ItemID=item_info,
        )

    return render(request, 'assets/claim.html',
                  {'item': item, 'status': claim_success, 'post': True})


"""This code is a view function called "home" that handles an HTTP request. When the view is called, 
it retrieves all objects in the "ItemInfo" model and stores them in the variable "data". The function then returns a 
rendered template called "assets/home_page.html", along with the data from "ItemInfo" passed as context to the template. """


def home(request):
    items = ItemInfo.objects.all()
    context = {
        "items": items
    }
    return render(request, 'assets/home_page.html', context)


"""
def item_list(request):
    items = ItemInfo.objects.all()
    context = {
        "items": items
    }
    return render(request, "items.html", context)

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


def request_item(request):
    if request.method == 'POST':
        obj = RequestInfo.objects.create(
            id=request.POST.get('id'),
            Description=request.POST.get('Description'),
            Location=request.POST.get('Location')
        )
    return render(request, 'assets/request_item.html')
