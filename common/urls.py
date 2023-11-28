from .views import ProductViewSet, LessonViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product/(?P<product_id>\d+)/lessons', LessonViewSet, basename='lessons')

urlpatterns = router.urls
