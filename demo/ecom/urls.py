from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('item_list/', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('order/', views.order_view, name='order_view'),
    path('logout/', LogoutView.as_view(next_page=''), name='logout'),  # Redirect to login after logout

]
