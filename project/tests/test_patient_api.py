import pytest

from .urlhelper import r, r_detail

pytestmark = pytest.mark.django_db


def _emails_from_list_response(data):
    items = data.get("results", data)
    out = []
    for it in items:
        user = it.get("user")
        if isinstance(user, dict):
            out.append(user.get("email"))
        else:
            out.append(it.get("email"))
    return [e for e in out if e]


def test_patient_sees_only_self(
    auth, patient_user, another_patient_user, patient, another_patient
):
    url = r(
        [
            "patient-list",
            "patients-list",
            "api:v1:patient-list",
            "api:v1:patients-list",
        ],
        "/api/v1/patients/",
    )
    res = auth(patient_user).get(url)
    assert res.status_code == 200
    emails = _emails_from_list_response(res.data)
    assert patient_user.email in emails
    assert another_patient_user.email not in emails


def test_doctor_and_admin_see_all(
    auth, doctor_user, superuser, patient, another_patient
):
    url = r(
        [
            "patient-list",
            "patients-list",
            "api:v1:patient-list",
            "api:v1:patients-list",
        ],
        "/api/v1/patients/",
    )
    res_doc = auth(doctor_user).get(url)
    assert res_doc.status_code == 200
    count_doc = res_doc.data.get(
        "count",
        len(
            res_doc.data
            if isinstance(res_doc.data, list)
            else res_doc.data.get("results", [])
        ),
    )
    assert count_doc >= 2

    res_admin = auth(superuser).get(url)
    assert res_admin.status_code == 200
    count_admin = res_admin.data.get(
        "count",
        len(
            res_admin.data
            if isinstance(res_admin.data, list)
            else res_admin.data.get("results", [])
        ),
    )
    assert count_admin >= 2


def test_patient_cannot_update_other_profile(auth, patient_user, another_patient):
    url = r_detail(
        [
            "patient-detail",
            "patients-detail",
            "api:v1:patient-detail",
            "api:v1:patients-detail",
        ],
        another_patient["id"],
        "/api/v1/patients",
    )
    res = auth(patient_user).patch(url, {"notes": "hack"}, format="json")
    assert res.status_code in (403, 404)
