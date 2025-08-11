import datetime as dt

import pytest

from .urlhelper import r, r_action, r_detail

pytestmark = pytest.mark.django_db


def test_doctor_can_create_consultation(auth, doctor_user, doctor, patient, now):
    url = r(
        [
            "consultation-list",
            "consultations-list",
            "api:v1:consultation-list",
            "api:v1:consultations-list",
        ],
        "/api/v1/consultations/",
    )
    payload = {
        "doctor": str(doctor["id"]),
        "patient": str(patient["id"]),
        "start_time": (now + dt.timedelta(hours=3)).isoformat(),
        "end_time": (now + dt.timedelta(hours=4)).isoformat(),
        "status": "waiting",
    }
    res = auth(doctor_user).post(url, payload, format="json")
    assert res.status_code in (201, 200)
    assert res.data["status"] == "waiting"


def test_patient_cannot_create_consultation(auth, patient_user, doctor, patient, now):
    url = r(
        [
            "consultation-list",
            "consultations-list",
            "api:v1:consultation-list",
            "api:v1:consultations-list",
        ],
        "/api/v1/consultations/",
    )
    payload = {
        "doctor": str(doctor["id"]),
        "patient": str(patient["id"]),
        "start_time": (now + dt.timedelta(hours=1)).isoformat(),
        "end_time": (now + dt.timedelta(hours=2)).isoformat(),
        "status": "waiting",
    }
    res = auth(patient_user).post(url, payload, format="json")
    assert res.status_code in (403, 401)


def test_participants_can_retrieve_detail(
    auth, consultation, doctor_user, patient_user
):
    url = r_detail(
        [
            "consultation-detail",
            "consultations-detail",
            "api:v1:consultation-detail",
            "api:v1:consultations-detail",
        ],
        consultation["id"],
        "/api/v1/consultations",
    )
    assert auth(doctor_user).get(url).status_code == 200
    assert auth(patient_user).get(url).status_code == 200


def test_strangers_cannot_see_consultation(auth, consultation, another_patient_user):
    url = r_detail(
        [
            "consultation-detail",
            "consultations-detail",
            "api:v1:consultation-detail",
            "api:v1:consultations-detail",
        ],
        consultation["id"],
        "/api/v1/consultations",
    )
    res = auth(another_patient_user).get(url)
    assert res.status_code in (403, 404)


def test_filter_by_status_search_and_ordering(auth, superuser, doctor, patient, now):
    api = auth(superuser)
    url = r(
        [
            "consultation-list",
            "consultations-list",
            "api:v1:consultation-list",
            "api:v1:consultations-list",
        ],
        "/api/v1/consultations/",
    )

    for status, shift in [("waiting", 1), ("confirmed", 3), ("completed", 5)]:
        payload = {
            "doctor": str(doctor["id"]),
            "patient": str(patient["id"]),
            "status": status,
            "start_time": (now + dt.timedelta(hours=shift)).isoformat(),
            "end_time": (now + dt.timedelta(hours=shift + 1)).isoformat(),
        }
        api.post(url, payload, format="json")

    res = api.get(url, {"status": "confirmed"})
    assert res.status_code == 200
    results = res.data.get("results", res.data)
    assert all(it["status"] == "confirmed" for it in results)

    api.get(url, {"patient_name": "John"})
    api.get(url, {"doctor_name": "House"})
    api.get(url, {"ordering": "-created_at"})


def test_set_status_permissions(
    auth, consultation, doctor_user, patient_user, superuser
):
    url = r_action(
        [
            "consultation-set-status",
            "consultations-set-status",
            "api:v1:consultation-set-status",
            "api:v1:consultations-set-status",
        ],
        consultation["id"],
        action="set-status",
        fallback="/api/v1/consultations",
    )
    res = auth(patient_user).post(url, {"status": "confirmed"}, format="json")
    assert res.status_code in (403, 401)

    res = auth(doctor_user).post(url, {"status": "confirmed"}, format="json")
    assert res.status_code in (200, 204)

    res = auth(superuser).post(url, {"status": "completed"}, format="json")
    assert res.status_code in (200, 204)
