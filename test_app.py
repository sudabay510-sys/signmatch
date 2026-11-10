"""Tests for SignMatch."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

os.environ["SIGNMATCH_DB"] = str(ROOT / "test.db")
os.environ["SIGNMATCH_ADMIN_PASSWORD"] = "test-admin-password"
os.environ["SIGNMATCH_SECRET"] = "test-secret"

from brands import BRANDS  # noqa: E402
from quiz_engine import create_app  # noqa: E402


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = tmp_path / "app.db"
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_SCHEMA", raising=False)
    monkeypatch.setenv("SIGNMATCH_DB", str(db))
    brand = dict(BRANDS["signmatch"])
    brand["root"] = str(ROOT)
    application = create_app(brand)
    application.config["TESTING"] = True
    with application.test_client() as c:
        yield c


def test_landing_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert BRANDS["signmatch"]["name"].encode() in r.data


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True


def test_quiz_flow_and_founding(client):
    r = client.get("/quiz", follow_redirects=False)
    assert r.status_code in (302, 303)
    # step 1
    r = client.get("/quiz/1")
    assert r.status_code == 200
    token = None
    # extract form_token from html
    html = r.data.decode()
    marker = 'name="form_token" value="'
    assert marker in html
    token = html.split(marker, 1)[1].split('"', 1)[0]

    questions = BRANDS["signmatch"]["questions"]
    for i, q in enumerate(questions, start=1):
        r = client.get(f"/quiz/{i}")
        html = r.data.decode()
        token = html.split(marker, 1)[1].split('"', 1)[0]
        data = {"form_token": token, "action": "next"}
        if q["type"] == "choice":
            if q.get("multi"):
                data["answer"] = q["options"][0]["id"]
            else:
                data["answer"] = q["options"][0]["id"]
        else:
            data["answer"] = "Test answer"
        r = client.post(f"/quiz/{i}", data=data, follow_redirects=False)
        assert r.status_code in (302, 303)

    r = client.get("/computing")
    assert r.status_code == 200
    r = client.get("/results")
    assert r.status_code == 200
    assert b"plan" in r.data.lower() or b"Plan" in r.data

    r = client.get("/paywall")
    assert r.status_code == 200
    assert b"Checkout coming soon" in r.data or b"founding" in r.data.lower()

    r = client.get("/founding")
    html = r.data.decode()
    token = html.split(marker, 1)[1].split('"', 1)[0]
    r = client.post(
        "/founding",
        data={"form_token": token, "email": "founder@example.com", "name": "Founder", "tier": BRANDS["signmatch"]["pricing"][0]["id"]},
        follow_redirects=False,
    )
    assert r.status_code in (302, 303)
    r = client.get("/founding/thanks")
    assert r.status_code == 200


def test_csrf_rejects_bad_token(client):
    client.get("/quiz/1")
    r = client.post("/quiz/1", data={"form_token": "nope", "action": "next", "answer": "x"})
    assert r.status_code == 400


def test_admin_requires_password(client):
    r = client.get("/admin")
    assert r.status_code == 401
    # login
    html = r.data.decode()
    marker = 'name="form_token" value="'
    token = html.split(marker, 1)[1].split('"', 1)[0]
    r = client.post("/admin", data={"form_token": token, "password": "test-admin-password"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Founding leads" in r.data


def test_legal_pages(client):
    for path in ("/privacy", "/terms", "/disclaimer"):
        assert client.get(path).status_code == 200


def test_print_requires_plan(client):
    r = client.get("/plan/print", follow_redirects=False)
    assert r.status_code in (302, 303)
