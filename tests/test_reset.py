from ._common import client, sleep_ms


def test_reset_requires_stopped():
    c = client()
    assert c.post("/timer/start").status_code == 200
    res = c.post("/timer/reset")
    assert res.status_code == 409
    assert res.get_json() == {"error": "CANNOT_RESET_WHILE_RUNNING"}


def test_reset_clears_elapsed_and_laps():
    c = client()
    c.post("/timer/start")
    sleep_ms(15)
    c.post("/timer/lap")
    sleep_ms(10)
    c.post("/timer/stop")

    res = c.post("/timer/reset")
    body = res.get_json()
    assert res.status_code == 200
    assert body == {"state": "stopped", "elapsed_ms": 0, "laps": []}

    # double check via GET
    state = c.get("/timer").get_json()
    assert state["elapsed_ms"] == 0
    assert state["laps"] == []

