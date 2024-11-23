import pytest
from django.utils import timezone
from .services import OrderService
from orders.models import Order
from rest_framework import status
from rest_framework.response import Response

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
        total_cost = OrderService.calculate_total_cost(bed, plant, worker)
        assert total_cost == bed.field.price + plant.price + worker.price


@pytest.mark.django_db
def test_create_order_success(user, workers, beds, plants, mocker):
    mocker.patch(
        "user.services.PersonService.update_wallet_balance",
        return_value=Response(status=status.HTTP_200_OK)
    )
    action = "planting"
    for worker, bed, plant in zip(workers, beds, plants):
        response = OrderService.create_order(user, bed, plant, action)
        assert response.status_code == status.HTTP_201_CREATED
        order_id = response.data['order_id']
        order = Order.objects.get(id=order_id)
        assert order.user == user
        assert order.worker is not None
        assert order.bed == bed
        assert order.plant == plant
        assert order.total_cost == bed.field.price + plant.price + order.worker.price


@pytest.mark.django_db
def test_create_order_insufficient_funds(user, workers, beds, plants, mocker):
    mocker.patch(
        "user.services.PersonService.update_wallet_balance",
        return_value=Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Insufficient funds"})
    )
    action = "planting"
    for worker, bed, plant in zip(workers, beds, plants):
        response = OrderService.create_order(user, bed, plant, action)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Insufficient funds"


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

    # Проверяем, что все заказы из базы данных получены
    assert len(all_orders) == len(orders)
    for order in all_orders:
        assert order in orders

