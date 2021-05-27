from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('address', views.PropertyAddressView, basename='address')
router.register('images', views.PropertyImageView, basename='image')
urlpatterns = router.urls