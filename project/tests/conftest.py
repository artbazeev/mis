import datetime as dt

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from .urlhelper import r


@pytest.fixture
def now():
    return timezone.now()


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def superuser(db):
    User = get_user_model()
    return User.objects.create_user(
        email="admin@example.com",
        password="adminpass",
        role="superuser",
        is_staff=True,
        is_superuser=True,
        first_name="Admin",
        last_name="Root",
        phone="+10000000001",
    )


@pytest.fixture
def doctor_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="doc@example.com",
        password="docpass",
        role="doctor",
        first_name="Gregory",
        last_name="House",
        phone="+10000000002",
    )


@pytest.fixture
def patient_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="pat@example.com",
        password="patpass",
        role="patient",
        first_name="John",
        last_name="Doe",
        patronymic="X",
        phone="+10000000003",
    )


@pytest.fixture
def another_patient_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="pat2@example.com",
        password="pat2pass",
        role="patient",
        first_name="Jane",
        last_name="Roe",
        patronymic="Y",
        phone="+10000000004",
    )


@pytest.fixture
def auth(api):
    def _login(user):
        api.force_authenticate(user=user)
        return api

    return _login


@pytest.fixture
def clinic(auth, superuser):
    api = auth(superuser)
    url = r(
        ["clinic-list", "clinics-list", "api:v1:clinic-list", "api:v1:clinics-list"],
        fallback="/api/v1/clinics/",
    )
    payload = {
        "name": "Alpha Clinic",
        "legal_address": "Legal st. 1",
        "physical_address": "Phys st. 2",
    }
    res = api.post(url, payload, format="json")
    if res.status_code not in (200, 201):
        list_res = api.get(url)
        if list_res.status_code == 200 and list_res.data:
            data = list_res.data.get("results", list_res.data)
            if isinstance(data, list) and data:
                return data[0]
            if isinstance(data, dict) and data.get("id"):
                return data
        raise AssertionError(
            f"Cannot create clinic, status {res.status_code}: {res.data}"
        )
    return res.data


@pytest.fixture
def doctor(auth, superuser, doctor_user, clinic):
    api = auth(superuser)
    url = r(
        ["doctor-list", "doctors-list", "api:v1:doctor-list", "api:v1:doctors-list"],
        fallback="/api/v1/doctors/",
    )
    payload = {
        "user": str(doctor_user.id),
        "specialization": "Therapist",
        "clinics": [str(clinic["id"])],
    }
    res = api.post(url, payload, format="json")
    if res.status_code not in (200, 201):
        raise AssertionError(
            f"Cannot create doctor via API: {res.status_code} {res.data}"
        )
    return res.data


@pytest.fixture
def patient(auth, superuser, patient_user):
    api = auth(superuser)
    url = r(
        [
            "patient-list",
            "patients-list",
            "api:v1:patient-list",
            "api:v1:patients-list",
        ],
        fallback="/api/v1/patients/",
    )
    payload = {"user": str(patient_user.id)}
    res = api.post(url, payload, format="json")
    if res.status_code not in (200, 201):
        raise AssertionError(
            f"Cannot create patient via API: {res.status_code} {res.data}"
        )
    return res.data


@pytest.fixture
def another_patient(auth, superuser, another_patient_user):
    api = auth(superuser)
    url = r(
        [
            "patient-list",
            "patients-list",
            "api:v1:patient-list",
            "api:v1:patients-list",
        ],
        fallback="/api/v1/patients/",
    )
    payload = {"user": str(another_patient_user.id)}
    res = api.post(url, payload, format="json")
    if res.status_code not in (200, 201):
        raise AssertionError(
            f"Cannot create patient2 via API: {res.status_code} {res.data}"
        )
    return res.data


@pytest.fixture
def consultation(auth, doctor_user, doctor, patient, now):
    api = auth(doctor_user)
    url = r(
        [
            "consultation-list",
            "consultations-list",
            "api:v1:consultation-list",
            "api:v1:consultations-list",
        ],
        fallback="/api/v1/consultations/",
    )
    payload = {
        "doctor": str(doctor["id"]),
        "patient": str(patient["id"]),
        "status": "waiting",
        "start_time": (now + dt.timedelta(hours=1)).isoformat(),
        "end_time": (now + dt.timedelta(hours=2)).isoformat(),
    }
    res = api.post(url, payload, format="json")
    if res.status_code not in (200, 201):
        raise AssertionError(
            f"Cannot create consultation via API: {res.status_code} {res.data}"
        )
    return res.data
