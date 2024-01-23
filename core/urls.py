from rest_framework.routers import DefaultRouter

from . import views


app_name = 'core'
router = DefaultRouter()

router.register('management/product', views.ProductManagementViewSet,
                basename='m-product')
router.register('management/product-category', views.ProductCategoryManagement,
                basename='m-product-category')
router.register('management/product-inventory',
                views.ProductInventoryManagement,
                basename='m-product-inventory')
router.register('management/discount', views.DiscountManagement,
                basename='m-discount')
router.register('index', views.IndexViewSet, basename='index')

urlpatterns = router.urls
