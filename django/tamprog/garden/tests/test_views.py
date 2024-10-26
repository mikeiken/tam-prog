import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order, AvailablePlants

import datetime
@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestViewSets:

    @pytest.mark.django_db
    def test_create_agronomist(self, api_client):
        data = {"salary": 60000, "days_work": "Пн-Сб", "work_schedule": "10:00-19:00"}
        response = api_client.post(reverse('agronomist-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Agronomist.objects.count() == 1
        assert Agronomist.objects.get().salary == 60000

    @pytest.mark.django_db
    def test_update_agronomist(self, api_client, agronomist):
        data = {"salary": 65000}
        response = api_client.patch(reverse('agronomist-detail', args=[agronomist.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        agronomist.refresh_from_db()
        assert agronomist.salary == 65000

    @pytest.mark.django_db
    def test_delete_agronomist(self, api_client, agronomist):
        response = api_client.delete(reverse('agronomist-detail', args=[agronomist.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Agronomist.objects.count() == 0

    @pytest.mark.django_db
    def test_create_supplier(self, api_client):
        data = {"email": "new_supplier@example.com", "account_number": "987654321"}
        response = api_client.post(reverse('supplier-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Supplier.objects.count() == 1

    @pytest.mark.django_db
    def test_update_supplier(self, api_client, supplier):
        data = {"email": "updated_supplier@example.com"}
        response = api_client.patch(reverse('supplier-detail', args=[supplier.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        supplier.refresh_from_db()
        assert supplier.email == "updated_supplier@example.com"

    @pytest.mark.django_db
    def test_delete_supplier(self, api_client, supplier):
        response = api_client.delete(reverse('supplier-detail', args=[supplier.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Supplier.objects.count() == 0

    @pytest.mark.django_db
    def test_create_worker(self, api_client):
        data = {"job_title": "Новый рабочий", "salary": 25000, "days_work": "Пн-Пт", "work_schedule": "9:00-18:00"}
        response = api_client.post(reverse('worker-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Worker.objects.count() == 1

    @pytest.mark.django_db
    def test_update_worker(self, api_client, worker):
        data = {"salary": 32000}
        response = api_client.patch(reverse('worker-detail', args=[worker.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        worker.refresh_from_db()
        assert worker.salary == 32000

    @pytest.mark.django_db
    def test_delete_worker(self, api_client, worker):
        response = api_client.delete(reverse('worker-detail', args=[worker.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Worker.objects.count() == 0

    @pytest.mark.django_db
    def test_create_garden_bed(self, api_client):
        data = {"state": "Отличное", "size": 15.0, "price": 10}
        response = api_client.post(reverse('gardenbed-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert GardenBed.objects.count() == 1

    @pytest.mark.django_db
    def test_update_garden_bed(self, api_client, garden_bed):
        data = {"size": 12.0}
        response = api_client.patch(reverse('gardenbed-detail', args=[garden_bed.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        garden_bed.refresh_from_db()
        assert garden_bed.size == 12.0

    @pytest.mark.django_db
    def test_delete_garden_bed(self, api_client, garden_bed):
        response = api_client.delete(reverse('gardenbed-detail', args=[garden_bed.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert GardenBed.objects.count() == 0

    @pytest.mark.django_db
    def test_create_fertilizer(self, api_client):
        data = {"compound": "Калий, Азот","price": 10,"boost" : 4,"name" : "Навоз"}
        response = api_client.post(reverse('fertilizer-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Fertilizer.objects.count() == 1

    @pytest.mark.django_db
    def test_update_fertilizer(self, api_client, fertilizer):
        data = {"compound": "Новый состав"}
        response = api_client.patch(reverse('fertilizer-detail', args=[fertilizer.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        fertilizer.refresh_from_db()
        assert fertilizer.compound == "Новый состав"

    @pytest.mark.django_db
    def test_delete_fertilizer(self, api_client, fertilizer):
        response = api_client.delete(reverse('fertilizer-detail', args=[fertilizer.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Fertilizer.objects.count() == 0

    @pytest.mark.django_db
    def test_create_user(self, api_client, agronomist, worker):
        data = {
            "password": "new_password",
            "login": "new_user",
            "role": "chel",
            "email": "new_user@mail.ru",
            "phone": "+72345678908",
            "agronomist_id": agronomist.id,
            "worker_id": worker.id
        }
        response = api_client.post(reverse('chel-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_update_user(self, api_client, user):
        data = {"email": "updated_user@mail.ru"}
        response = api_client.patch(reverse('chel-detail', args=[user.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.email == "updated_user@mail.ru"

    @pytest.mark.django_db
    def test_delete_user(self, api_client, user):
        response = api_client.delete(reverse('chel-detail', args=[user.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test_create_plant(self, api_client, garden_bed):
        data = {
            "name": "Огурец",
            "growth_time": 24,
            "description": "Великое",
            "garden_id": garden_bed.id,
            "price": 10,
            "landing_data": "2024-09-03"
        }
        response = api_client.post(reverse('plant-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Plant.objects.count() == 1

    @pytest.mark.django_db
    def test_update_plant(self, api_client, plant):
        data = {"name": "Новый огурец"}
        response = api_client.patch(reverse('plant-detail', args=[plant.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        plant.refresh_from_db()
        assert plant.name == "Новый огурец"

    @pytest.mark.django_db
    def test_delete_plant(self, api_client, plant):
        response = api_client.delete(reverse('plant-detail', args=[plant.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Plant.objects.count() == 0

    @pytest.mark.django_db
    def test_create_plot(self, api_client, garden_bed):
        data = {"size": 30.0, "garden_id": garden_bed.id}
        response = api_client.post(reverse('plot-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Plot.objects.count() == 1

    @pytest.mark.django_db
    def test_update_plot(self, api_client, plot):
        data = {"size": 25.0}
        response = api_client.patch(reverse('plot-detail', args=[plot.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        plot.refresh_from_db()
        assert plot.size == 25.0

    @pytest.mark.django_db
    def test_delete_plot(self, api_client, plot):
        response = api_client.delete(reverse('plot-detail', args=[plot.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Plot.objects.count() == 0

    @pytest.mark.django_db
    def test_create_order(self, api_client, garden_bed, plant, worker, fertilizer):
        data = {
            "deadline": "2024-10-19",
            "garden_id": garden_bed.id,
            "plant_id": plant.id,
            "worker_id": worker.id,
            "fertilizer_id": fertilizer.id
        }
        response = api_client.post(reverse('order-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1

    @pytest.mark.django_db
    def test_update_order(self, api_client, order):
        data = {"deadline": "2024-10-20"}
        response = api_client.patch(reverse('order-detail', args=[order.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.deadline == datetime.date(2024, 10, 20)

    @pytest.mark.django_db
    def test_delete_order(self, api_client, order):
        response = api_client.delete(reverse('order-detail', args=[order.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.count() == 0

    @pytest.mark.django_db
    def test_create_available_plant(self,api_client, garden_bed):
        data = {
            "name": "Огурец",
            "price": 20.0,
            "growth_time": 75,
            "description": "Зеленый овощ",
            "landing_data": "2024-05-15",
            "garden_id": garden_bed.id
        }
        response = api_client.post(reverse('availableplants-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert AvailablePlants.objects.count() == 1

    @pytest.mark.django_db
    def test_update_available_plant(self,api_client, available_plants):
        data = {"price": 18.0}
        response = api_client.patch(reverse('availableplants-detail', args=[available_plants.id]), data, format='json')
        assert response.status_code == status.HTTP_200_OK
        available_plants.refresh_from_db()
        assert available_plants.price == 18.0

    @pytest.mark.django_db
    def test_delete_available_plant(self,api_client, available_plants):
        response = api_client.delete(reverse('availableplants-detail', args=[available_plants.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert AvailablePlants.objects.count() == 0