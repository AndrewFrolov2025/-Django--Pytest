from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, StudentViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')
router.register('students', StudentViewSet, basename='students')
urlpatterns = router.urls