from datetime import datetime

from ._common import client

ALLOWED = ["UTC", "Asia/Tokyo", "America/New_York", "Europe/London"]


def test_clock_returns_allowed_timezones():
    c = client()
    for tz in ALLOWED:
        res = c.get(f"/clock?tz={tz}")
        assert res.status_code == 200
        body = res.get_json()
        assert body["tz"] == tz
        assert isinstance(body["epoch_ms"], int)

        dt = datetime.fromisoformat(body["iso"])
        # epoch_ms should be close to parsed iso timestamp
        diff = abs(int(dt.timestamp() * 1000) - body["epoch_ms"])
        assert diff < 1500


def test_clock_rejects_invalid_timezone():
    c = client()
    res = c.get("/clock?tz=Asia/Somewhere")
    assert res.status_code == 400
    assert res.get_json() == {"error": "INVALID_TIMEZONE"}
