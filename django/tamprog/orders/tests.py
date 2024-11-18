import pytest
from django.utils import timezone
from .services import OrderService
from orders.models import Order

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
    mocker.patch("user.services.PersonService.update_wallet_balance", return_value=True)
    action = "planting"

    # Проверяем создание заказа для каждой комбинации worker, bed, plant
    for worker, bed, plant in zip(workers, beds, plants):
        order = OrderService.create_order(user, worker, bed, plant, action)
        assert order is not None
        assert order.user == user
        assert order.worker == worker
        assert order.bed == bed
        assert order.plant == plant
        assert order.total_cost == bed.field.price + plant.price + worker.price


@pytest.mark.django_db
def test_create_order_insufficient_funds(user, workers, beds, plants, mocker):
    mocker.patch("user.services.PersonService.update_wallet_balance", return_value=False)
    action = "planting"

    # Проверяем создание заказа для каждой комбинации worker, bed, plant
    for worker, bed, plant in zip(workers, beds, plants):
        order = OrderService.create_order(user, worker, bed, plant, action)
        assert order is None


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

    # Завершаем все заказы
    for order in orders:
        OrderService.complete_order(order)

    completed_orders = OrderService.filter_orders(is_completed=True)

    # Проверяем, что все заказы в completed_orders имеют заполненное поле completed_at
    assert all(order.completed_at is not None for order in completed_orders)
    assert len(completed_orders) == sum(1 for order in orders if order.completed_at is not None)


@pytest.mark.django_db
def test_filter_orders_not_completed(orders):
    not_completed_orders = OrderService.filter_orders(is_completed=False)

    # Проверяем, что все заказы в not_completed_orders не имеют значения в completed_at
    assert all(order.completed_at is None for order in not_completed_orders)
    assert len(not_completed_orders) == sum(1 for order in orders if order.completed_at is None)


@pytest.mark.django_db
def test_filter_orders_all(orders):
    all_orders = OrderService.filter_orders()

    # Проверяем, что все заказы из базы данных получены
    assert len(all_orders) == len(orders)
    for order in all_orders:
        assert order in orders

