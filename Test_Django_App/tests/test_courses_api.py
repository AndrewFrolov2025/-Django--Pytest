import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from students.models import Course, Student

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_get_courses_list(client):
    course_1 = Course.objects.create(name = '1C - programmer')
    course_3 = Course.objects.create(name = 'SQL')
    url = reverse('courses-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    course_name = [course['name'] for course in response.data]
    assert course_1.name in course_name
    assert course_3.name in course_name

@pytest.mark.django_db
def test_filter_course_by_id(client):
    course_1 = Course.objects.create(name = '1C - programmer')
    Course.objects.create(name = 'SQL')

    url = reverse('courses-list')
    response = client.get(url, {'name': course_1.name})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == course_1.id
    assert response.data[0]['name'] == course_1.name

@pytest.mark.django_db
def test_create_course(client):
    url = reverse('courses-list')
    data = {'name': '1C - programmer'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1
    assert Course.objects.first().name == '1C - programmer'

@pytest.mark.django_db
def test_update_course(client):
    course = Course.objects.create(name='1C - programmer')
    url = reverse('courses-detail', args=[course.id])
    data = {'name': '1C'}
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    course.refresh_from_db()
    assert course.name == '1C'

@pytest.mark.django_db
def test_delete_course(client):
    course = Course.objects.create(name='1C - programmer')
    url = reverse('courses-detail', args=[course.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0

