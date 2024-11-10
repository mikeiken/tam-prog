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
def test_calculate_total_cost(bed1, plant, worker):
    total_cost = OrderService.calculate_total_cost(bed1, plant, worker)
    assert total_cost == bed1.field.price + plant.price + worker.price


@pytest.mark.django_db
def test_create_order_success(user1, worker, bed1, plant, mocker):
    # Мокаем метод обновления баланса в PersonService
    mocker.patch("user.services.PersonService.update_wallet_balance", return_value=True)

    action = "planting"
    order = OrderService.create_order(user1, worker, bed1, plant, action)

    assert order is not None
    assert order.user == user1
    assert order.worker == worker
    assert order.bed == bed1
    assert order.plant == plant
    assert order.total_cost == bed1.field.price + plant.price + worker.price


@pytest.mark.django_db
def test_create_order_insufficient_funds(user1, worker, bed1, plant, mocker):
    # Если баланс недостаточный, метод вернет None
    mocker.patch("user.services.PersonService.update_wallet_balance", return_value=False)

    action = "planting"
    order = OrderService.create_order(user1, worker, bed1, plant, action)

    assert order is None


@pytest.mark.django_db
def test_complete_order(order):
    completed_order = OrderService.complete_order(order)

    assert completed_order.completed_at is not None
    assert completed_order.completed_at <= timezone.now()


@pytest.mark.django_db
def test_filter_orders_completed(order, mocker):
    # Мокаем `timezone.now()` для предсказуемого времени завершения
    mock_time = timezone.now()
    mocker.patch("django.utils.timezone.now", return_value=mock_time)

    # Завершаем заказ
    OrderService.complete_order(order)

    completed_orders = OrderService.filter_orders(is_completed=True)
    assert completed_orders.count() == 1
    assert completed_orders.first() == order


@pytest.mark.django_db
def test_filter_orders_not_completed(order):
    not_completed_orders = OrderService.filter_orders(is_completed=False)
    assert not_completed_orders.count() == 1
    assert not_completed_orders.first() == order


@pytest.mark.django_db
def test_filter_orders_all(order):
    orders = OrderService.filter_orders()
    assert orders.count() == 1
    assert orders.first() == order
