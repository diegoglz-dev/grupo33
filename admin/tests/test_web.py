from tests import client


def test_web():
    response = client.get("/")
    assert b"Hola" in response.data
