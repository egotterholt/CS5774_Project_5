from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from library.models import LibraryItem
from actions.models import Action

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
            actions = (Action.objects.all().order_by('-created').filter(verb__in=[
                    "commented on library item",
                    "edited a comment on library item"
                ], target_id=item.id))
            if username:
                if username == item.owner.lower():
                    print("You are the owner of this item.")
                    owner_return = True
                else:
                    print("You are not the owner of this item.")
            return render(request,
                          "library/library_item/detail.html",
                          { "item": item, "owner": owner_return, "actions": actions }
                          )

    messages.add_message(request, messages.WARNING, "The item you were looking for does not exist.")
    return redirect("library:home")

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
    # Redirect if not logged in
    if not request.session.get("username", False):
        return redirect("users:register")

    if request.method == "POST":
        # Process the form inputs
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("categories")
        cost = request.POST.get("cost")
        period = request.POST.get("days")
        user = User.objects.get(username=request.session.get("username"))
        item = LibraryItem(
            title=title,
            category=category,
            period=period,
            cost=cost,
            description=description,
            owner=user.first_name,
            user=user
        )
        item.save()

        # Save the action into the DB
        action = Action(
            user=user,
            verb="created new library item",
            target=item
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "You have created a new item: %s" % item.title)

        return redirect("library:item-detail", item.id)
    else:
        return render(request,
                      "library/library_item/create.html"
                      )

# Works with comments on an item if logged in (or admin)
def library_item_add_comment(request, item_id):
    # Redirect if not logged in
    if not request.session.get("username", False):
        return redirect("users:register")

    if request.method == "POST":
        try:
            item = LibraryItem.objects.get(pk=item_id)
        except LibraryItem.DoesNotExist:
            return JsonResponse({'error': 'No item found with that ID'}, status=200)

        # Process the form inputs
        user = User.objects.get(username=request.session.get("username"))

        comment_action = request.POST.get("comment-button")

        if comment_action == "Add Comment":
            comment = request.POST.get("item-comment-description")
            print(comment)

            # Comment action added into the DB
            action = Action(
                user=user,
                verb="commented on library item",
                target=item,
                comment=comment
            )
            action.save()
            messages.add_message(request, messages.SUCCESS, "You have commented on item: %s" % item.title)

        if comment_action == "Edit Comment":
            action_id = request.POST.get("action-id")
            actions = (Action.objects.all().order_by('-created').filter(verb__in=[
                    "commented on library item",
                    "edited a comment on library item"
                ], target_id=item.id))

            for action in actions:
                print(action.id)
                if action.id == action_id:
                    print("Hooray action id matches for action", action.id)
            print("Editing comment for action", action_id)

            return render(request,
                  "library/library_item/detail.html",
                  { "item": item, "actions": actions, "action_id": int(action_id) }
                  )

        if comment_action == "Save Edited Comment":
            action_id = request.POST.get("action-id")
            print("Saving edits on comment for action", action_id)
            try:
                action = Action.objects.get(pk=action_id)
                new_comment = request.POST.get("item-comment-description")
                action.comment = new_comment
                print(new_comment)
                action.verb = "edited a comment on library item"
                action.save()
                messages.add_message(request, messages.SUCCESS, "You have edited a comment on item: %s" % item.title)
            except Action.DoesNotExist:
                messages.add_message(request, messages.WARNING, "Comment could not be found.")

        if comment_action == "Cancel Edit":
            redirect("library:item-detail", item.id)

        if comment_action == "Delete Comment":
            action_id = request.POST.get("action-id")
            print("Attempting to delete", action_id)

            try:
                action = Action.objects.get(pk=action_id)
                action.delete()
                messages.add_message(request, messages.SUCCESS, "You have deleted a comment on item: %s" % item.title)
            except Action.DoesNotExist:
                messages.add_message(request, messages.WARNING, "Comment could not be found.")

    return redirect("library:item-detail", item_id)

# Updates who is renting an item when the user selects it in the details page7
def library_item_rent(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        username = request.session.get("username")
        try:
            item = LibraryItem.objects.get(pk=item_id)
            item.rented_by = username
            item.save()

            # Added the user's rental action into the DB
            user = User.objects.get(username=request.session.get("username"))
            action = Action(
                user=user,
                verb="rented library item",
                target=item
            )
            action.save()

            return JsonResponse({'success': 'success', 'rented_by': item.rented_by}, status=200)
        except LibraryItem.DoesNotExist:
            return JsonResponse({'error': 'No item found with that ID'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)

# Account details page showing users' personal items
def account(request):
    if not request.session.get("username", False):
        return redirect("users:register")

    library_items = LibraryItem.objects.all()
    username = request.session.get("username")
    print(username)

    if username:
        user1 = get_object_or_404(User, username=username)
        items = library_items.filter(user=user1)
        actions = Action.objects.all().order_by('-created').filter(target_id__in=items)

        if user1.details.role == "admin":
            return render(request,
                   "library/account.html",
                          { "items": library_items, "user": user1, "actions": actions }
                          )

        elif user1.details.role == "regular":
            print(user1.details.user_id)
            library_items = library_items.filter(user_id__exact=user1.details.user_id)
            print(library_items.count())
            return render(request,
                   "library/account.html",
                          { "items": library_items, "user": user1, "actions": actions }
                          )
    return render(request,
           "library/account.html"
                  )

# Returns list of user's items they have posted
def account_items(request, username):
    library_items = LibraryItem.objects.all()
    user1 = get_object_or_404(User, username=username)
    print(user1.details.user_id)
    library_items = library_items.filter(user_id__exact=user1.details.user_id)
    print(library_items.count())
    return render(request,
           "library/account.html",
                  { "items": library_items, "user": user1 }
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
        print(category)
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

        # Edit item action added into the DB
        user = User.objects.get(username=request.session.get("username"))
        action = Action(
            user=user,
            verb="edited library item",
            target=item
        )
        action.save()

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

                # Delete item action added into the DB
                user = User.objects.get(username=username)
                action = Action(
                    user=user,
                    verb="deleted library item"
                )
                action.save()

                messages.add_message(request, messages.WARNING, "You have deleted an item: %s" % item.title)

                break

    return redirect("library:account")