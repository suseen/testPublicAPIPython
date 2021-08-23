import json
import requests
import time


def test_get_weather():
    # verify whether the payload has only valid precipitation type
    uri = "http://www.7timer.info/bin/api.pl?"
    querystring = {
        'lon': 113.17,
        'lat': 23.09,
        'product': 'astro',
        'output': 'json'
    }
    resp = requests.get(uri, querystring)
    data = resp.json()["dataseries"]
    count = 0
    valid_prec_type = {'rain', 'snow', 'none'}
    for x in data:
        if x["prec_type"] not in valid_prec_type:
            count += 1
    assert count == 0, "there is an invalid precipitation type in payload"


def test_rate_limit_put():
    # verify rate limit for submitting joke - 5 attempt per two minutes
    uri = "https://v2.jokeapi.dev/submit"
    post_body = {
        "formatVersion": 3,
        "category": "Misc",
        "type": "single",
        "joke": "joke",
        "flags": {
            "nsfw": False,
            "religious": False,
            "political": False,
            "racist": False,
            "sexist": False,
            "explicit": False
        },
        "lang": "en"
    }

    headers = {
        "content-type": "application/json"
    }
    attempt = 1
    rate_limit_attempt = 5
    start_time = time.time()
    while attempt <= rate_limit_attempt+1:
        resp = requests.put(uri, data=json.dumps(post_body), headers=headers)
        if attempt > rate_limit_attempt:
            assert resp.json()["message"] == 'Submission blocked by Rate Limiting', 'rate limit failed'
        attempt += 1
    now = time.time()
    while int(now-start_time) < 120:
        now = time.time()
    resp = requests.put(uri, data=json.dumps(post_body), headers=headers)
    assert resp.status_code == 201, 'rate limit was not cancelled after 2 minutes'

