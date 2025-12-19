from ._common import client, sleep_ms


def test_start_transitions_to_running():
    c = client()
    res = c.post("/timer/start")
    assert res.status_code == 200
    assert res.get_json() == {"state": "running", "elapsed_ms": 0}

    res_again = c.post("/timer/start")
    assert res_again.status_code == 409
    assert res_again.get_json() == {"error": "ALREADY_RUNNING"}


def test_stop_requires_running_and_reports_elapsed():
    c = client()
    res_stop = c.post("/timer/stop")
    assert res_stop.status_code == 409
    assert res_stop.get_json() == {"error": "ALREADY_STOPPED"}

    c.post("/timer/start")
    sleep_ms(20)
    res = c.post("/timer/stop")
    body = res.get_json()
    assert res.status_code == 200
    assert body["state"] == "stopped"
    assert body["elapsed_ms"] >= 15


def test_elapsed_increases_while_running():
    c = client()
    c.post("/timer/start")
    sleep_ms(15)
    first = c.get("/timer").get_json()["elapsed_ms"]
    sleep_ms(15)
    second = c.get("/timer").get_json()["elapsed_ms"]
    assert second > first

    stop_body = c.post("/timer/stop").get_json()
    assert stop_body["elapsed_ms"] >= second


def test_elapsed_accumulates_on_restart():
    c = client()
    c.post("/timer/start")
    sleep_ms(20)
    first_stop = c.post("/timer/stop").get_json()["elapsed_ms"]

    c.post("/timer/start")
    sleep_ms(15)
    second_stop = c.post("/timer/stop").get_json()["elapsed_ms"]

    assert second_stop >= first_stop + 10
