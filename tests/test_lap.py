from ._common import client, sleep_ms


def test_lap_requires_running_state():
    c = client()
    res = c.post("/timer/lap")
    assert res.status_code == 409
    assert res.get_json() == {"error": "NOT_RUNNING"}


def test_lap_records_elapsed_deltas():
    c = client()
    assert c.post("/timer/start").status_code == 200

    sleep_ms(20)
    res1 = c.post("/timer/lap")
    body1 = res1.get_json()
    assert res1.status_code == 201
    assert body1["lap_index"] == 1
    assert body1["total_elapsed_ms"] >= 15

    sleep_ms(25)
    res2 = c.post("/timer/lap")
    body2 = res2.get_json()
    assert res2.status_code == 201
    assert body2["lap_index"] == 2
    assert body2["total_elapsed_ms"] > body1["total_elapsed_ms"]
    assert body2["lap_elapsed_ms"] == body2["total_elapsed_ms"] - body1["total_elapsed_ms"]

    timer_state = c.get("/timer").get_json()
    assert len(timer_state["laps"]) == 2
    assert timer_state["laps"][-1]["total_elapsed_ms"] == body2["total_elapsed_ms"]

