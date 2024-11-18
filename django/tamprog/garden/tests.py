import pytest
from .services import FieldService,BedService
from .models import Field,Bed
from mixer.backend.django import mixer
from celery.result import AsyncResult
from unittest.mock import patch

def test_get_sorted_fields_success(celery_settings, mocker):
    mocked_task = mocker.patch('garden.services.get_sorted_fields_task.delay')
    mocked_task.return_value = AsyncResult('fake-task-id')
    mocker.patch.object(AsyncResult, 'get', return_value=[{'id': 1, 'price': 100}])
    result = FieldService.get_sorted_fields(sort_by='price', ascending=True)
    mocked_task.assert_called_once_with('price', True)
    assert result == [{'id': 1, 'price': 100}]

def test_get_sorted_fields_timeout(celery_settings, mocker):
    mocked_task = mocker.patch('garden.services.get_sorted_fields_task.delay')
    mocked_task.return_value = AsyncResult('fake-task-id')
    mocker.patch.object(AsyncResult, 'get', side_effect=Exception('Timeout'))
    with pytest.raises(Exception, match='Timeout'):
        FieldService.get_sorted_fields(sort_by='price', ascending=True)

@pytest.mark.django_db
def test_filter_beds(api_client, user, beds):
    api_client.force_authenticate(user=user)
    url = '/api/v1/bed/'
    response = api_client.get(url, {'is_rented': 'true'})
    assert response.status_code == 200

    rented_beds = [bed for bed in beds if bed.is_rented]
    response_rented_status = [bed['is_rented'] for bed in response.data]
    assert all(response_rented_status)
    assert len(response_rented_status) == len(rented_beds)

@pytest.mark.django_db
def test_rent_bed_already_rented(beds, person):
    for bed in beds:
        bed.is_rented = True
        bed.save()
        result = BedService.rent_bed(bed_id=bed.id, person=person)
        assert result.status_code == 400


@pytest.mark.django_db
def test_rent_bed_success(beds, person):
    bed = next(b for b in beds if not b.is_rented)
    initial_count = bed.field.count_beds
    result = BedService.rent_bed(bed_id=bed.id, person=person)
    bed.refresh_from_db()
    assert result.status_code == 200
    assert bed.is_rented is True
    assert bed.rented_by == person
    assert bed.field.count_beds == initial_count - 1


@pytest.mark.django_db
def test_release_bed_success(beds, person):
    bed = beds[0]
    bed.is_rented = True
    bed.rented_by = person
    bed.save()
    initial_count = bed.field.count_beds
    result = BedService.release_bed(bed_id=bed.id)
    bed.refresh_from_db()
    assert result.status_code == 200
    assert bed.is_rented is False
    assert bed.rented_by is None
    assert bed.field.count_beds == initial_count + 1


@pytest.mark.django_db
def test_release_bed_not_rented(beds):
    for bed in beds:
        bed.is_rented = False
        bed.save()
        result = BedService.release_bed(bed_id=bed.id)
        assert result.status_code == 400

@pytest.mark.django_db
def test_get_user_beds(beds, person):
    for bed in beds:
        bed.rented_by = person
        bed.is_rented = True
        bed.save()
    user_beds = BedService.get_user_beds(user=person)
    assert len(user_beds) == len(beds)
    for bed in user_beds:
        assert bed.rented_by == person
        assert bed.is_rented is True


@pytest.mark.django_db
def test_filter_beds_is_rented(beds):
    for bed in beds:
        bed.is_rented = True
        bed.save()
    rented_beds = BedService.filter_beds(is_rented=True)
    assert rented_beds.count() == len(beds)
    for bed in rented_beds:
        assert bed.is_rented is True


@pytest.mark.django_db
def test_filter_beds_not_rented(beds):
    for bed in beds:
        bed.is_rented = False
        bed.save()
    not_rented_beds = BedService.filter_beds(is_rented=False)
    assert not_rented_beds.count() == len(beds)
    for bed in not_rented_beds:
        assert bed.is_rented is False


@pytest.mark.django_db
def test_get_sorted_fields_by_price(celery_settings, mocker,fields):
    mocker.patch('garden.services.get_sorted_fields_task.delay')
    mocker.patch.object(AsyncResult, 'get',
                        return_value=[{'price': 30},
                                      {'price': 31},
                                      {'price': 32},
                                      {'price': 33},
                                      {'price': 34}])

    fields = FieldService.get_sorted_fields(sort_by='price', ascending=True)
    assert [field['price'] for field in fields] == [30, 31, 32, 33, 34]


@pytest.mark.django_db
def test_get_sorted_fields_by_beds(celery_settings, mocker):
    mocker.patch('garden.services.get_sorted_fields_task.delay')
    mocker.patch.object(AsyncResult, 'get',
                        return_value=[{'count_beds': 10},
                                      {'count_beds': 11},
                                      {'count_beds': 12},
                                      {'count_beds': 13},
                                      {'count_beds': 14}])
    fields = FieldService.get_sorted_fields(sort_by='count_beds', ascending=True)
    assert [field['count_beds'] for field in fields] == [10, 11, 12, 13, 14]



