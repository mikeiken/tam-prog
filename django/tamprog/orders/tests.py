import pytest
from django.utils import timezone
from .services import OrderService
from orders.models import Order
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal

@pytest.mark.django_db
def test_filter_orders(api_client, user, orders):
    api_client.force_authenticate(user=user)
    url = '/api/v1/order/'
    response = api_client.get(url, {'is_completed': 'true'})
    assert response.status_code == 200
    response_data = response.data
    assert all(order['completed_at'] is not None for order in response_data)
    assert len(response_data) == sum(1 for order in orders if order.completed_at is not None)
    response_incomplete = api_client.get(url, {'is_completed': 'false'})
    assert response_incomplete.status_code == 200
    response_data_incomplete = response_incomplete.data
    assert all(order['completed_at'] is None for order in response_data_incomplete)
    assert len(response_data_incomplete) == sum(1 for order in orders if order.completed_at is None)


@pytest.mark.django_db
def test_calculate_total_cost(beds, plants, workers):
    for bed, plant, worker in zip(beds, plants, workers):
        beds_count = 1
        total_cost = OrderService.calculate_total_cost(bed.field, plant, worker, beds_count)
        assert total_cost == (bed.field.price * beds_count) + (plant.price * beds_count) + worker.price





@pytest.mark.django_db
def test_create_order_success(user, workers, beds, plants, mocker):
    user.wallet_balance = 100000.00
    user.save()
    mocker.patch(
        "user.services.PersonService.update_wallet_balance",
        return_value=Response(status=status.HTTP_200_OK)
    )
    mocker.patch(
        "garden.services.BedService.rent_bed",
        return_value=Response(status=status.HTTP_200_OK)
    )
    mocker.patch(
        "plants.services.BedPlantService.plant_in_bed",
        return_value=Response(status=status.HTTP_201_CREATED)
    )
    action = "planting"
    for bed, plant in zip(beds, plants):
        response = OrderService.create_order(user, bed, plant, action)
        assert response.status_code == status.HTTP_201_CREATED, f"Unexpected status code: {response.status_code}"
        order_id = response.data['order_id']
        order = Order.objects.get(id=order_id)
        assert order.user == user
        assert order.worker is not None
        assert order.bed == bed
        assert order.plant == plant
        total_cost = bed.field.price + plant.price + order.worker.price
        assert order.total_cost == total_cost

@pytest.mark.django_db
def test_create_order_via_url(api_client, user, workers, beds, plants, mocker):
    mocker.patch(
        "user.services.PersonService.update_wallet_balance",
        return_value=Response(status=status.HTTP_200_OK)
    )
    mocker.patch(
        "garden.services.BedService.rent_bed",
        return_value=Response(status=status.HTTP_200_OK)
    )
    mocker.patch(
        "plants.services.BedPlantService.plant_in_bed",
        return_value=Response(status=status.HTTP_201_CREATED)
    )
    initial_balance = 1500.0
    user.wallet_balance = initial_balance
    user.save()
    api_client.force_authenticate(user=user)
    url = '/api/v1/order/'
    data = {
        "bed": beds[0].id,
        "plant": plants[0].id,
        "worker": workers[0].id,
        "comments": "planting"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED, f"Unexpected status code: {response.status_code}"
    order = Order.objects.get(bed=beds[0], plant=plants[0], comments="planting")
    assert order.user == user
    assert order.worker == workers[0]
    assert order.bed == beds[0]
    assert order.plant == plants[0]
    total_cost = beds[0].field.price + plants[0].price + workers[0].price
    assert order.total_cost == total_cost
    user.refresh_from_db()
    expected_balance = initial_balance - total_cost
    assert user.wallet_balance == expected_balance



@pytest.mark.django_db
def test_create_order_insufficient_funds(user, workers, beds, plants, mocker):
    # Мокинг внешних зависимостей
    mocker.patch(
        "user.services.PersonService.update_wallet_balance",
        return_value=Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Insufficient funds"})
    )
    mocker.patch(
        "garden.services.BedService.rent_bed",
        return_value=Response(status=status.HTTP_200_OK)
    )
    mocker.patch(
        "plants.services.BedPlantService.plant_in_bed",
        return_value=Response(status=status.HTTP_200_OK)
    )
    action = "planting"
    for bed, plant in zip(beds, plants):
        response = OrderService.create_order(user, bed, plant, action)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Insufficient funds", f"Unexpected error: {response.data['error']}"



@pytest.mark.django_db
def test_complete_order(orders):
    for order in orders:
        completed_order = OrderService.complete_order(order)
        assert completed_order.completed_at is not None
        assert completed_order.completed_at <= timezone.now()



@pytest.mark.django_db
def test_filter_orders_completed(orders, mocker):
    mock_time = timezone.now()
    mocker.patch("django.utils.timezone.now", return_value=mock_time)
    for order in orders:
        OrderService.complete_order(order)
    completed_orders = OrderService.filter_orders(is_completed=True)
    assert all(order.completed_at is not None for order in completed_orders)
    assert len(completed_orders) == sum(1 for order in orders if order.completed_at is not None)


@pytest.mark.django_db
def test_filter_orders_not_completed(orders):
    not_completed_orders = OrderService.filter_orders(is_completed=False)
    assert all(order.completed_at is None for order in not_completed_orders)
    assert len(not_completed_orders) == sum(1 for order in orders if order.completed_at is None)


@pytest.mark.django_db
def test_filter_orders_all(orders):
    all_orders = OrderService.filter_orders()
    assert len(all_orders) == len(orders)
    for order in all_orders:
        assert order in orders

@pytest.mark.django_db
def test_filter_orders_completed_url(api_client, superuser, orders):
    api_client.force_authenticate(user=superuser)
    url = '/api/v1/order/'
    response = api_client.get(url, {'is_completed': 'true'})
    assert response.status_code == 200
    response_data = response.data
    assert all(order['completed_at'] is not None for order in response_data)
    assert len(response_data) == sum(1 for order in orders if order.completed_at is not None)

@pytest.mark.django_db
def test_filter_orders_not_completed_url(api_client, superuser, orders):
    api_client.force_authenticate(user=superuser)
    url = '/api/v1/order/'
    response = api_client.get(url, {'is_completed': 'false'})
    assert response.status_code == 200
    response_data = response.data
    assert all(order['completed_at'] is None for order in response_data)
    assert len(response_data) == sum(1 for order in orders if order.completed_at is None)

@pytest.mark.django_db
def test_filter_orders_all_url(api_client, superuser, orders):
    api_client.force_authenticate(user=superuser)
    url = '/api/v1/order/'
    response = api_client.get(url)
    assert response.status_code == 200
    response_data = response.data
    assert len(response_data) == len(orders)
    for order in response_data:
        assert order['id'] in [o.id for o in orders]


