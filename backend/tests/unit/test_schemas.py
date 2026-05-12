import pytest
from pydantic import ValidationError

from app.server.schema.server import CreateServerParam, UpdateServerParam

BASE = {
    "name": "web-01",
    "ip_address": "192.168.1.10",
    "country": "Vietnam",
    "os": "Ubuntu",
    "os_version": "22.04 LTS",
    "platform": "Nginx",
    "arch": "x86_64",
    "status": "Online",
}


# CreateServerParam 

def test_create_valid_payload():
    obj = CreateServerParam(**BASE)
    assert obj.name == "web-01"
    assert obj.os_version == "22.04 LTS"
    assert obj.status == "Online"


def test_create_default_status_is_online():
    payload = {k: v for k, v in BASE.items() if k != "status"}
    obj = CreateServerParam(**payload)
    assert obj.status == "Online"


@pytest.mark.parametrize("ip", [
    "10.0.0.1", "255.255.255.255", "0.0.0.0", "192.168.1.100",
])
def test_create_valid_ipv4(ip: str):
    obj = CreateServerParam(**{**BASE, "ip_address": ip})
    assert obj.ip_address == ip


@pytest.mark.parametrize("bad_ip", [
    "999.999.999.999", "not-an-ip", "192.168.1", "", "300.0.0.1",
])
def test_create_invalid_ip_raises_validation_error(bad_ip: str):
    with pytest.raises(ValidationError):
        CreateServerParam(**{**BASE, "ip_address": bad_ip})


def test_create_invalid_status_raises():
    with pytest.raises(ValidationError):
        CreateServerParam(**{**BASE, "status": "Maintenance"})


def test_create_empty_name_raises():
    with pytest.raises(ValidationError):
        CreateServerParam(**{**BASE, "name": ""})


def test_create_single_char_country_raises():
    with pytest.raises(ValidationError):
        CreateServerParam(**{**BASE, "country": "X"})


# UpdateServerParam

def test_update_all_fields_optional():
    obj = UpdateServerParam()
    assert obj.name is None
    assert obj.ip_address is None
    assert obj.status is None


def test_update_partial_fields():
    obj = UpdateServerParam(name="new-name", status="Offline")
    assert obj.name == "new-name"
    assert obj.status == "Offline"
    assert obj.os is None


def test_update_invalid_ip_raises():
    with pytest.raises(ValidationError):
        UpdateServerParam(ip_address="not-an-ip")


def test_update_none_ip_is_allowed():
    obj = UpdateServerParam(ip_address=None)
    assert obj.ip_address is None


def test_update_invalid_status_raises():
    with pytest.raises(ValidationError):
        UpdateServerParam(status="Unknown")
