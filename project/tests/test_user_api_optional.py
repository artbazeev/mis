import pytest
from django.urls import NoReverseMatch

from .urlhelper import r

pytestmark = pytest.mark.django_db


def test_me_endpoint_returns_profile(auth, patient_user):
    try:
        url = r(
            ["user-me", "users-me", "api:v1:user-me", "api:v1:users-me"],
            "/api/v1/users/me/",
        )
    except NoReverseMatch:
        pytest.xfail("No 'me' endpoint configured")
    res = auth(patient_user).get(url)
    assert res.status_code == 200
    assert res.data.get("phone") == patient_user.phone
