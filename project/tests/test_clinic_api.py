import pytest

from .urlhelper import r, r_detail

pytestmark = pytest.mark.django_db


def test_clinic_list_is_public(api, clinic):
    url = r(
        ["clinic-list", "clinics-list", "api:v1:clinic-list", "api:v1:clinics-list"],
        "/api/v1/clinics/",
    )
    res = api.get(url)
    assert res.status_code == 200
    data = res.data.get("results", res.data)
    if isinstance(data, dict):
        assert data.get("id") == clinic["id"]
    else:
        assert any(str(it.get("id")) == str(clinic["id"]) for it in data)


def test_clinic_update_only_superuser(auth, superuser, doctor_user, clinic):
    url = r_detail(
        [
            "clinic-detail",
            "clinics-detail",
            "api:v1:clinic-detail",
            "api:v1:clinics-detail",
        ],
        clinic["id"],
        "/api/v1/clinics",
    )
    res = auth(doctor_user).patch(url, {"name": "New Name"}, format="json")
    assert res.status_code in (403, 401)

    res = auth(superuser).patch(url, {"name": "New Name"}, format="json")
    assert res.status_code == 200
    assert res.data["name"] == "New Name"
