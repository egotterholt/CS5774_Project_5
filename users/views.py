from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from actions.models import Action
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from users.models import Details

# Create your views here.
def profile(request, username):
    user1 = get_object_or_404(User, username=username)
    actions = Action.objects.all().order_by('-created').filter(Q(user=user1) | Q(target_id=user1.id))
    return render(request,
              "users/user/profile.html",
                  {"user": user1, "actions": actions}
              )

# Registers a user with the input data then logs into their account
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, "The username is already taken: %s" % username)
            return redirect("users:register")
        else:
            # Validate email before continuing
            try:
                validate_email(email)
            except ValidationError:
                messages.add_message(request, messages.WARNING, "Invalid email entry - %s, try again" % email)
                return redirect("users:register")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.details.location = location
            user.details.save()

            messages.add_message(request, messages.SUCCESS, "You have registered with the username: %s" % user.username)

            # Edit user action added into the DB
            action = Action(
                user=user,
                verb="registered a new user",
                target=user
            )
            action.save()

            userLogin = authenticate(username=username, password=password)
            if userLogin is not None:
                user1 = get_object_or_404(User, username=username)
                request.session["username"] = user1.username
                request.session["role"] = user1.details.role
                messages.add_message(request, messages.SUCCESS, "You have logged in successfully.")
            else:
                messages.add_message(request, messages.WARNING, "The username or password is incorrect.")

            return redirect("library:home")
    else:
        return render(request,
                  "users/user/register.html"
                  )

# Login view to retrieve and save user info
def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    print(username, pw)

    user = authenticate(username=username, password=pw)
    if user is not None:
        user1 = get_object_or_404(User, username=username)
        request.session["username"] = user1.username
        request.session["role"] = user1.details.role
        messages.add_message(request, messages.SUCCESS, "You have logged in successfully.")
    else:
        messages.add_message(request, messages.WARNING, "The username or password is incorrect.")

    return redirect("library:home")

# Logout view to remove the current user
def logout_user(request):
    del request.session["username"]
    del request.session["role"]
    return redirect("library:home")

# Pulls up all the items associated with a profile
def profile_items(request, username):
    print("Asking for all items in a profile")
    return redirect("library:account-items", username=username)

# Offers users (and admin) ability to edit their profile
def profile_edit(request, username):

    if request.method == "POST":
        submission = request.POST.get("submit")

        if submission == "Cancel Edits":
            messages.add_message(request, messages.WARNING, "You have cancelled the action.")
            return redirect("users:profile", username=username)

        if submission == "Save Edits":
            print("Editing profile")
            email = request.POST.get('email')
            password = request.POST.get('password')
            location = request.POST.get('location')
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            role = request.POST.get('role')

            user1 = get_object_or_404(User, username=username)
            if email:
                if email != "" and email != user1.email:
                    try:
                        validate_email(email)
                        user1.email = email
                        print("Updated email")
                    except ValidationError:
                        messages.add_message(request, messages.WARNING, "Invalid email entry - %s, try again" % email)
                        return redirect("users:profile", username=username)
            if location:
                if location != "" and location != user1.details.location:
                    user1.details.location = location
                    print("Updated location")
            if first_name:
                if first_name != "" and first_name != user1.first_name:
                    user1.first_name = first_name
                    print("Updated first_name")
            if last_name:
                if last_name != "" and last_name != user1.last_name:
                    user1.last_name = last_name
                    print("Updated last_name")
            if role:
                if role != "" and role != user1.details.role:
                    user1.details.role = role
                    print("Updated role")
            if password:
                if password != "":
                    user1.password = password
                    print("Updated password")

            user1.save()
            user1.details.save()

            # Edit user action added into the DB
            user = User.objects.get(username=request.session.get("username"))
            action = Action(
                user=user,
                verb="edited a user",
                target=user1
            )
            action.save()

            messages.add_message(request, messages.SUCCESS, "You have edited %s's profile" % username)

            return redirect("library:home")

    else:
        print("Method not POST, redirecting to user's profile page.")
        user1 = get_object_or_404(User, username=username)
        return render(request,
                      "users/user/edit.html",
                      {"user": user1}
                      )

# Deletes user profile
def profile_delete(request, username):
    if request.POST.get("delete"):
        users = Details.objects.all()
        for user in users:
            user1 = get_object_or_404(User, username=username)
            if user.user_id == user1.details.user_id:
                print("deleting profile for ", user1.username)
                if user1.username == request.session["username"]:
                    del request.session["username"]
                    del request.session["role"]
                user.delete()
                user1.delete()
                messages.add_message(request, messages.SUCCESS, "You have deleted successfully.")

                # Delete user action added into the DB
                user = User.objects.get(username=request.session.get("username"))
                action = Action(
                    user=user,
                    verb="deleted a user",
                    target=user1
                )
                action.save()

                break

    return redirect("library:home")
