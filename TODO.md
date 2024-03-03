User stories

Core app
As a user:
[o] I want to be able to browse products
[o] I want to be able to check product details
[o] I want products to have a visible discount
[o] I want products to be categorized


Auth app
As a user:
[o] I want to be able to register an account
[o] I want to be able to log in
[o] I want to check my user profile
[ ] I want to be able to reset password
[ ] I want to be able to reset email
[ ] I want to be able to delete my account


Shopping app
As a user:
[o] I want to be able to check order history
[o] I want to be able to add products to my cart
[o] I want to be able to delete products from my cart
[o] I want to be able to delete all products from my cart
[?] I want my cart to not clear itself when i go offline NOTE: it has TTL, perhaps increase it to couple hours - currently 15 min
[?] I want to be able to increase quantity of products in my cart NOTE: by updating the cart
[o] I want to be able to check my cart 
[ ] I want to be able to use shopping without the need of having an account

- Redis shopping cart storage DONE
- add review mean or no reviews to products DONE
TODO Anonymous comments under a product
TODO Filtering and sorting products
TODO Filtering by category etc (fancy)
TODO Order History details, probably after payment is
- User reviews and comments DONE
- Wishlist DONE
TODO User notification when a product from a wishlist is on a discount
TODO User notification when a product will be available
TODO Oauth2


TODO allow passing order in paymentserializer if it's status is not
TODO Update ProductInventory after creating OrderItem
TODO maybe change payment url to checkout/payment/id url
TODO add check if user has stripe_id
TODO check total value from cart to payment\
TODO add update order status

TODO refactor serializers add short versions and long version and put them in correct places
