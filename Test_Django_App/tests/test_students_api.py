import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from students.models import Student

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_get_student_list(client):
    student_1 = Student.objects.create(name='Жора')
    student_2 = Student.objects.create(name='Петя')
    url = reverse('students-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    student_name = [student['name'] for student in response.data]
    assert student_1.name in student_name
    assert student_2.name in student_name

@pytest.mark.django_db
def test_create_student_list(client):
    student_1 = Student.objects.create(name='Жора')
    student_2 = Student.objects.create(name='Петя')
    url = reverse('students-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    student_names = [student['name'] for student in response.data]
    assert student_1.name in student_names
    assert student_2.name in student_names

@pytest.mark.django_db
def test_create_student_without_courses(client):
    url = reverse('students-list')
    data = {'name': 'Жора', 'courses': []}

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    assert Student.objects.first().name == 'Жора'

@pytest.mark.django_db
def test_update_student(client):
    student = Student.objects.create(name='Жора')
    url = reverse("students-detail", args=[student.id])
    data = {"name": "Жора Сидоров"}
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.name == "Жора Сидоров"

@pytest.mark.django_db
def test_delete_student(client):
    student = Student.objects.create(name="Жора")

    url = reverse("students-detail", args=[student.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Student.objects.count() == 0

@pytest.mark.django_db
def test_get_one_student(client, student_factory):
    student = student_factory(name="Ivan")
    url = reverse("students-detail", args=[student.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == student.id
    assert response.data["name"] == student.name

@pytest.mark.django_db
def test_filter_students_by_id(client, student_factory):
    student_1 = student_factory(name="Жора")
    student_2 = student_factory(name="Петя")
    url = reverse("students-list")
    response = client.get(url, data={"id": student_1.id})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == student_1.id
    assert response.data[0]["name"] == student_1.name
    assert response.data[0]["id"] != student_2.id
