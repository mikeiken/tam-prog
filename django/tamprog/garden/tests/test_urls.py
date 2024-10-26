import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_agronomist_url(api_client):
    url = reverse('agronomist-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_supplier_url(api_client):
    url = reverse('supplier-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_worker_url(api_client):
    url = reverse('worker-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_garden_bed_url(api_client):
    url = reverse('gardenbed-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_fertilizer_url(api_client):
    url = reverse('fertilizer-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_url(api_client):
    url = reverse('chel-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_plant_url(api_client):
    url = reverse('plant-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_plot_url(api_client):
    url = reverse('plot-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_order_url(api_client):
    url = reverse('order-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_available_plants_url(api_client):
    url = reverse('availableplants-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK