from django.urls import path

from knox import views as knox_views

from . import views


app_name = 'users'
urlpatterns = [
    path('create', views.CreateUserView.as_view(), name="create"),

    path('profile', views.ManageUserView.as_view(), name='profile'),
    path('profile/history', views.OrderHistoryView.as_view(), name='history'),
    path('profile/wishlist', views.WishlistView.as_view(), name='wishlist'),
    path('profile/wishlist/<str:pk>',
         views.WishlistView.as_view(),
         name='wishlist-delete'),

    path('login', views.LoginView.as_view(), name='knox_login'),
    path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),  # noqa

    path('product/review', views.ReviewView.as_view(), name='review'),
]
