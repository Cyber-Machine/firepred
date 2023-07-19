import pytest
from flask import url_for

from firepred.routes.predict import InputException


@pytest.mark.parametrize(
    "data",
    [
        {"Temperature": "50", "Oxygen": "75", "Humidity": "10"},
        {"Temperature": "10", "Oxygen": "15", "Humidity": "12"},
    ],
)
def test_request(flask_app, data):
    response = flask_app.post(
        url_for("predict.predict"),
        data=data,
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "data",
    [
        {"Temperature": "10", "Oxygen": "", "Humidity": "12"},
        {"Temperature": "", "Oxygen": "15", "Humidity": "12"},
        {"Temperature": "10", "Oxygen": "15", "Humidity": ""},
    ],
)
def test_incomplete_input(flask_app, data):
    # with pytest.raises(ValueError):
    response = flask_app.post(
        url_for("predict.predict"),
        data=data,
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "data",
    [
        {"Temperature": "10", "Oxygen": "120", "Humidity": "12"},
        {"Temperature": "112", "Oxygen": "15", "Humidity": "12"},
        {"Temperature": "10", "Oxygen": "15", "Humidity": "-12"},
    ],
)
def test_incorrect_input(flask_app, data):
    response = flask_app.post(
        url_for("predict.predict"),
        data=data,
    )
    assert response.status_code == 400
