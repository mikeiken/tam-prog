import pytest
from .services import FieldService,BedService
from .models import Field,Bed
from mixer.backend.django import mixer

@pytest.mark.django_db
def test_sort_fields(api_client, user, fields):
    api_client.force_authenticate(user=user)
    assert len(fields) == 5
    url = '/api/v1/field/'
    response = api_client.get(url, {'sort': 'price', 'asc': 'true'})
    assert response.status_code == 200
    assert response.data
    # Создаем поля с уникальными ценами
    fields = [mixer.blend(Field, price=30), mixer.blend(Field, price=31), mixer.blend(Field, price=32),
              mixer.blend(Field, price=33), mixer.blend(Field, price=34)]
    sorted_fields = sorted(fields, key=lambda x: x.price)
    response_prices = [field['price'] for field in response.data]
    expected_prices = [field.price for field in sorted_fields]
    assert response_prices == expected_prices



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
def test_rent_bed_success(bed, person):
    result = BedService.rent_bed(bed_id=bed.id, person=person)
    bed.refresh_from_db()
    assert result is True
    assert bed.is_rented is True
    assert bed.rented_by == person
    assert bed.field.count_beds == 4

@pytest.mark.django_db
def test_rent_bed_already_rented(bed, person):
    bed.is_rented = True
    bed.save()
    result = BedService.rent_bed(bed_id=bed.id, person=person)
    assert result is False

@pytest.mark.django_db
def test_release_bed_success(bed, person):
    bed.is_rented = True
    bed.rented_by = person
    bed.save()
    result = BedService.release_bed(bed_id=bed.id)
    bed.refresh_from_db()
    assert result is True
    assert bed.is_rented is False
    assert bed.rented_by is None
    assert bed.field.count_beds == 6

@pytest.mark.django_db
def test_release_bed_not_rented(bed):
    result = BedService.release_bed(bed_id=bed.id)
    assert result is False

@pytest.mark.django_db
def test_get_user_beds(bed, person):
    bed.rented_by = person
    bed.is_rented = True
    bed.save()
    user_beds = BedService.get_user_beds(user=person)
    assert len(user_beds) == 1
    assert user_beds[0] == bed

@pytest.mark.django_db
def test_filter_beds_is_rented(bed):
    bed.is_rented = True
    bed.save()
    rented_beds = BedService.filter_beds(is_rented=True)
    assert rented_beds.count() == 1
    assert rented_beds.first() == bed

@pytest.mark.django_db
def test_filter_beds_not_rented(bed):
    not_rented_beds = BedService.filter_beds(is_rented=False)
    assert not_rented_beds.count() == 1
    assert not_rented_beds.first() == bed


@pytest.mark.django_db
def test_get_sorted_fields_by_price():
    fields = FieldService.get_sorted_fields(sort_by='price', ascending=True)
    assert [field['price'] for field in fields] == [30, 31, 32, 33, 34]


@pytest.mark.django_db
def test_get_sorted_fields_by_beds():
    fields = FieldService.get_sorted_fields(sort_by='count_beds', ascending=True)
    assert [field['count_beds'] for field in fields] == [10, 11, 12, 13, 14]


