import pytest

from .urlhelper import r

pytestmark = pytest.mark.django_db


def test_doctor_list_visible_for_admin_and_doctor(auth, doctor_user, superuser, doctor):
    url = r(
        ["doctor-list", "doctors-list", "api:v1:doctor-list", "api:v1:doctors-list"],
        "/api/v1/doctors/",
    )
    assert auth(doctor_user).get(url).status_code == 200
    assert auth(superuser).get(url).status_code == 200


def test_patient_cannot_create_doctor_profile(auth, patient_user, clinic):
    url = r(
        ["doctor-list", "doctors-list", "api:v1:doctor-list", "api:v1:doctors-list"],
        "/api/v1/doctors/",
    )
    payload = {"user": None, "specialization": "Cardio", "clinics": [str(clinic["id"])]}
    res = auth(patient_user).post(url, payload, format="json")
    assert res.status_code in (403, 401)
