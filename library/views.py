from django.shortcuts import render, redirect
from .models import library_items, regular_user, admin_user


# Create your views here.

# Home page showing users the local highlights
def home(request):
    return render(request,
           "library/index.html",
                  { "items": reversed(library_items) }
                  )

# Item list page
def library_item_list(request):
    return render(request,
           "library/library_item/list.html",
                  { "items": library_items }
                  )

# Item detail page to describe a single item
def library_item_detail(request, item_id):
    for item in library_items:
        if item.id == item_id:
            break
    return render(request,
                  "library/library_item/detail.html",
                  { "item": item }
                  )

# Searches through the list of items and returns the first matching result
def library_item_search(request):
    title = request.GET.get("search-items", "")
    match = 0
    for item in library_items:
        if item.title.lower() == title.lower():
            match = 1
            break

    if match == 0:
        for item in library_items:
            library_words = item.title.split()
            search_words = title.split()
            for library_word in library_words:
                for search_word in search_words:
                    if library_word.lower() == search_word.lower():
                        match = 1
                        break
            if match == 1:
                break

    if match == 0:
        return render(request,
                      "library/library_item/search.html"
                      )
    else:
        return render(request,
                      "library/library_item/detail.html",
                      { "item": item }
                      )

# Creates an item if logged in
def library_item_add(request):
    return render(request,
                  "library/library_item/create.html"
                  )

# Login view to retrieve and save user info
def login(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    if (username == regular_user["username"]) and (pw == regular_user["password"]):
        request.session["username"] = username
        request.session["role"] = "regular"
        return redirect("library:home")
    elif (username == admin_user["username"]) and (pw == admin_user["password"]):
        request.session["username"] = username
        request.session["role"] = "admin"
        return redirect("library:home")
    else:
        return redirect("library:account")

# Logout view to remove the current user
def logout(request):
    del request.session["username"]
    del request.session["role"]
    return redirect("library:home")

# Account details page showing users' personal items
def account(request):
    return render(request,
           "library/account.html",
                  { "items": library_items }
                  )

# Brings up the detail page for a specific item
def account_item_detail(request, item_id):
    for item in library_items:
        if item.id == item_id:
            break
    return render(request,
                  "library/library_item/detail.html",
                  { "item": item }
                  )

# Brings up the editing page for a specific item
def account_item_edit(request, item_id):
    for item in library_items:
        if item.id == item_id:
            break
    return render(request,
                  "library/library_item/edit.html",
                  { "item": item }
                  )

# Deletes an item if provided a "delete" POST call
def account_item_delete(request, item_id):
    if "delete" in request.POST:
        for item in library_items:
            if item.id == item_id:
                temp_item = item
                library_items.remove(item)
                library_items.append(temp_item)
                print("deleting item: " + item.title)
                break
    return render(request,
                  "library/account.html",
                  { "items": library_items }
                  )