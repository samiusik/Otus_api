"""API-Tests for https://dog.ceo/api"""
import requests
import pytest


# base_url = "https://dog.ceo/api"
# тесты на получения списка пород

@pytest.mark.parametrize("endpoint, status_code, status",
                         [("/breeds", 404, "error"),
                          ("/breeds/list", 200, "success"),
                          ("/breeds/list/", 200, "success"),
                          ("/breeds/list/all", 200, "success")])
def test_get_all_list(base_url, endpoint, status_code, status):
    response = requests.get(base_url + endpoint)

    assert response.status_code == status_code
    assert response.json().get("status") == status


# тесты на получение рандомной кратинки собаки
def test_get_random_image(base_url):
    response = requests.get(base_url + "/breeds/image/random")

    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert "https://images.dog.ceo/breeds" in response.json().get("message")


# тесты на получение рандомной кратинки определенной породы
@pytest.mark.parametrize("breed, quantity",
                         [('basenji', 3),
                          ('beagle', 3)],
                         ids=['basenji',
                              'beagle'])
def test_get_random_image_by_breed(base_url, breed, quantity):
    response = requests.get(base_url + "/breed/" + breed + "/images/random/3")

    assert response.status_code == 200
    assert response.json().get("status") == "success"

    data = response.json().get("message")
    assert len(data) == quantity


# получение произвольного числа картинок
@pytest.mark.parametrize("actual_quantity, exp_quantity",
                         [(1, 1), (0, 1), (13213230, 126), (126, 126), (127, 126), (0.232, 1)])
def test_get_random_quantity_of_image(base_url, actual_quantity, exp_quantity):
    response = requests.get(base_url + "/breed/groenendael/images/random/" + str(actual_quantity))

    assert response.status_code == 200
    assert response.json().get("status") == "success"

    data = response.json().get("message")
    assert len(data) == exp_quantity


# получение подпород сообак
def test_get_sub_breed_list(base_url):
    response = requests.get(base_url + "/breeds/list/all")
    breeds_list = response.json().get("message")

    for breed in breeds_list:
        response = requests.get(base_url + "/breed/" + breed + "/list")
        sub_breed_list = response.json().get("message")

        assert sub_breed_list == breeds_list[breed]
