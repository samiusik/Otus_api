"""API-Tests for https://api.openbrewerydb.org/breweries"""
import requests
import pytest


@pytest.mark.parametrize("param, value", [('city', 'miami'),
                                          ('state', 'new york'),
                                          ('name', 'mood')])
def test_get_breweries_by_param(base_url, param, value):
    response = requests.get(url=base_url,
                            params={'by_' + param: value})

    assert response.status_code == 200

    print(response.json())
    breweries = response.json()
    for i in range(len(breweries)):
        assert value in breweries[i][param].lower()


@pytest.mark.parametrize("postal_code", ["44107", "44107", "44107-2441", "44107%2D2441", "44107_2441", "44107%5F2441"])
def test_get_breweries_by_postal(base_url, postal_code):
    response = requests.get(base_url + "?by_postal=" + postal_code)
    assert response.status_code == 200

    breweries = response.json()
    for i in range(len(breweries)):
        assert "44107" in breweries[i]['postal_code'].lower()


@pytest.mark.parametrize("brewery_id", ['5128df48-79fc-4f0f-8b52-d06be54d0cec', '9c5a66c8-cc13-416f-a5d9-0a769c87d318'])
def test_get_brewery_by_id(base_url, brewery_id):
    response = requests.get(base_url + '/' + str(brewery_id))

    assert response.status_code == 200
    assert response.json().get("id") == brewery_id


def test_search_brewery(base_url):
    test_word = 92530
    search_word = str(test_word)

    response = requests.get(url=base_url + "/search",
                            params={"query": search_word})

    assert response.status_code == 200
    assert search_word in response.json()[0].get("postal_code")


@pytest.mark.parametrize("name", ["dog", "cat", "bear"])
def test_use_autocomplete(base_url, name):
    response = requests.get(url=base_url + "/autocomplete",
                            params={"query": name})

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.parametrize("method, status", [('post', 404), ('get', 200), ('put', 404), ('delete', 404)])
def test_methods_for_brewery_api(base_url, method, status):
    request = getattr(requests, method)
    response = request(url=base_url)

    assert response.status_code == status
