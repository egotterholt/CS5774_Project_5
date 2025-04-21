from django.shortcuts import render, redirect
from django.contrib import messages
from .models import regular_user, admin_user, LibraryItem
from django.http import JsonResponse

# Create your views here.

# Home page showing users the local highlights
def home(request):
    library_items = LibraryItem.objects.all()
    return render(request,
           "library/index.html",
                  { "items": reversed(library_items) }
                  )

# Item list page
def library_item_list(request):
    sort = request.GET.get('sort', None)
    owner_rating_filter = request.GET.get('owner_rating')
    product_rating_filter = request.GET.get('product_rating')

    library_items = LibraryItem.objects.all()

    # Sort by cost or rating
    if sort == "cost_low":
        library_items = library_items.order_by('cost')
    elif sort == "cost_high":
        library_items = library_items.order_by('-cost')
    elif sort == "rating_low":
        library_items = library_items.order_by('product_rating')
    elif sort == "rating_high":
        library_items = library_items.order_by('-product_rating')

    # Filter by owner or product rating
    if owner_rating_filter:
        library_items = library_items.filter(owner_rating__gte=owner_rating_filter)
    if product_rating_filter:
        library_items = library_items.filter(product_rating__gte=product_rating_filter)

    return render(request,
           "library/library_item/list.html",
                  { "items": library_items }
                  )

# Item detail page to describe a single item
def library_item_detail(request, item_id):
    library_items = LibraryItem.objects.all()
    username = request.session.get("username")
    if username:
        username = username.lower()
    owner_return = False
    print(username)

    for item in library_items:
        if item.id == item_id:
            if username:
                if username == item.owner.lower():
                    print("You are the owner of this item.")
                    owner_return = True
                else:
                    print("You are not the owner of this item.")
            break
    return render(request,
                  "library/library_item/detail.html",
                  { "item": item, "owner": owner_return }
                  )

# Searches through the list of items and returns the first matching result
def library_item_search(request):
    library_items = LibraryItem.objects.all()
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
    if not request.session.get("username", False):
        return redirect("library:account")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("categories")
        # photo = request.POST.get("add-item-image")
        owner = request.session.get("username")
        cost = request.POST.get("cost")
        period = request.POST.get("days")
        item = LibraryItem(
            title=title,
            category=category,
            period=period,
            cost=cost,
            description=description,
            owner=owner
        )
        item.save()
        messages.add_message(request, messages.SUCCESS, "You have created a new item: %s" % item.title)

        return redirect("library:item-detail", item.id)
    else:
        return render(request,
                      "library/library_item/create.html"
                      )

def library_item_rent(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        username = request.session.get("username")
        # item_id = request.POST.get("item_id")
        try:
            item = LibraryItem.objects.get(pk=item_id)
            item.rented_by = username
            item.save()
            return JsonResponse({'success': 'success', 'rented_by': item.rented_by}, status=200)
        except LibraryItem.DoesNotExist:
            return JsonResponse({'error': 'No item found with that ID'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)

# Login view to retrieve and save user info
def login(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    if (username == regular_user["username"]) and (pw == regular_user["password"]):
        request.session["username"] = username
        request.session["role"] = "regular"
        return redirect("library:account")
    elif (username == admin_user["username"]) and (pw == admin_user["password"]):
        request.session["username"] = username
        request.session["role"] = "admin"
        return redirect("library:account")
    else:
        return redirect("library:home")

# Logout view to remove the current user
def logout(request):
    del request.session["username"]
    del request.session["role"]
    return redirect("library:home")

# Account details page showing users' personal items
def account(request):
    library_items = LibraryItem.objects.all()
    username = request.session.get("username")
    print(username)

    if username:
        if request.session["role"] == "admin":
            return render(request,
                   "library/account.html",
                          { "items": library_items }
                          )

        elif request.session["role"] == "regular":
            library_items = library_items.filter(owner__iexact=username)
            return render(request,
                   "library/account.html",
                          { "items": library_items }
                          )
    return render(request,
           "library/account.html",
                  )

# Brings up the detail page for a specific item
def account_item_detail(request, item_id):
    library_items = LibraryItem.objects.all()
    for item in library_items:
        if item.id == item_id:
            break
    return render(request,
                  "library/library_item/detail.html",
                  { "item": item, "owner": True }
                  )

# Brings up the editing page for a specific item
def account_item_edit(request, item_id):
    if not request.session.get("username", False):
        return redirect("library:home")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("categories")
        owner = request.session.get("username")
        cost = request.POST.get("cost")
        period = request.POST.get("days")

        library_items = LibraryItem.objects.all()
        for item in library_items:
            if item.id == item_id:
                break
        print("Editing item ", item_id, ": ", item.title)

        item.title=title
        item.category=category
        item.period=period
        item.cost=cost
        item.description=description
        item.owner=owner
        item.save()
        print("Editing item ", item.id, ": ", item.title)
        messages.add_message(request, messages.INFO, "You have edited an item: %s" % item.title)

        return redirect("library:item-detail", item.id)
    else:
        library_items = LibraryItem.objects.all()
        for item in library_items:
            if item.id == item_id:
                break
        return render(request,
                      "library/library_item/edit.html",
                      { "item": item }
                      )

# Deletes an item if provided a "delete" POST call
def account_item_delete(request, item_id):
    library_items = LibraryItem.objects.all()
    username = request.session.get("username")

    if request.POST.get("delete"):
        for item in library_items:
            if item.id == item_id:
                print("deleting item ", item.id, ": ", item.title)
                item.delete()
                messages.add_message(request, messages.WARNING, "You have deleted an item: %s" % item.title)

                break

    if request.session["role"] == "admin":
        library_items = LibraryItem.objects.all()
        return render(request,
                      "library/account.html",
                      {"items": library_items}
                      )
    elif request.session["role"] == "regular":
        library_items = LibraryItem.objects.all().filter(owner__iexact=username)
        return render(request,
                      "library/account.html",
                      {"items": library_items}
                      )
    else:
        return redirect("library:home")