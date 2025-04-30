from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    # library views
    path('', views.home, name='home'),
    path('items', views.library_item_list, name='item-list'),
    path('items/<int:item_id>/', views.library_item_detail, name='item-detail'),
    path('items/info/<int:item_id>', views.library_item_detail, name='item-detail'),
    path('items/<int:item_id>/rent', views.library_item_rent, name='item-rent'),
    path('items/<int:item_id>/add-comment', views.library_item_add_comment, name='item-add-comment'),
    path('items/add', views.library_item_add, name='item-add'),
    path('search', views.library_item_search, name='item-search'),
    path('account', views.account, name='account'),
    path('items/<str:username>', views.account_items, name='account-items'),
    path('account/info/<int:item_id>', views.account_item_detail, name='account-item-detail'),
    path('account/edit/<int:item_id>', views.account_item_edit, name='account-item-edit'),
    path('account/delete/<int:item_id>', views.account_item_delete, name='account-item-delete'),
]