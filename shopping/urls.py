from django.urls import path


from shopping.views import CartItemView, ShoppingSessionView


app_name = 'shopping'
urlpatterns = [
    path('cart/', ShoppingSessionView.as_view(), name='cart'),
    path('cart/items', CartItemView.as_view(), name='cart-items')
]
