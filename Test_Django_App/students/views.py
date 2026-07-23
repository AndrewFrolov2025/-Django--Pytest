from rest_framework.viewsets import ModelViewSet
from .models import Course, Student
from .serializers import CourseSerializer, StudentSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    filterset_fields = ('id', 'name')

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    filterset_fields = ('id', 'name')

