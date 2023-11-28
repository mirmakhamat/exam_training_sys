from .views import ProductViewSet, LessonViewSet, StatsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product/(?P<product_id>\d+)/lessons', LessonViewSet, basename='lessons')
router.register(r'stats', StatsViewSet, basename='stats')

urlpatterns = router.urls
