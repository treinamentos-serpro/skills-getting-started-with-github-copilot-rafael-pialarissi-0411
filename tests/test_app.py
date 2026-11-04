import pytest


ACTIVITY = "Chess Club"
SIGNUP_URL = f"/activities/{ACTIVITY}/signup"
PARTICIPANTS_URL = f"/activities/{ACTIVITY}/participants"
EMAIL = "test-student@mergington.edu"


def test_root_redirects_to_frontend(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client, activities):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities
    assert ACTIVITY in response.json()


def test_signup_updates_activity_immediately(client, activities):
    before = list(activities[ACTIVITY]["participants"])

    response = client.post(SIGNUP_URL, params={"email": EMAIL})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {EMAIL} for {ACTIVITY}"}
    activity = client.get("/activities").json()[ACTIVITY]
    assert activity["participants"] == before + [EMAIL]
    assert len(activity["participants"]) <= activity["max_participants"]


def test_signup_rejects_duplicate_without_changing_participants(client, activities):
    before = list(activities[ACTIVITY]["participants"])

    response = client.post(SIGNUP_URL, params={"email": before[0]})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert activities[ACTIVITY]["participants"] == before


def test_signup_allows_last_spot_and_rejects_next_student(client, activities):
    activity = activities[ACTIVITY]
    activity["max_participants"] = len(activity["participants"]) + 1

    response = client.post(SIGNUP_URL, params={"email": EMAIL})

    assert response.status_code == 200
    assert len(activity["participants"]) == activity["max_participants"]
    before = list(activity["participants"])

    response = client.post(SIGNUP_URL, params={"email": "another@mergington.edu"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
    assert activity["participants"] == before


def test_unregister_updates_activity_immediately(client, activities):
    before = list(activities[ACTIVITY]["participants"])
    email = before[0]

    response = client.delete(PARTICIPANTS_URL, params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {ACTIVITY}"}
    assert client.get("/activities").json()[ACTIVITY]["participants"] == before[1:]

    response = client.delete(PARTICIPANTS_URL, params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert activities[ACTIVITY]["participants"] == before[1:]


def test_unregister_rejects_unknown_participant_without_changing_data(client, activities):
    before = list(activities[ACTIVITY]["participants"])

    response = client.delete(PARTICIPANTS_URL, params={"email": EMAIL})

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert activities[ACTIVITY]["participants"] == before


def test_student_can_sign_up_again_after_unregistering(client, activities):
    email = activities[ACTIVITY]["participants"][0]

    assert client.delete(PARTICIPANTS_URL, params={"email": email}).status_code == 200
    assert client.post(SIGNUP_URL, params={"email": email}).status_code == 200
    participants = client.get("/activities").json()[ACTIVITY]["participants"]
    assert participants.count(email) == 1


@pytest.mark.parametrize(
    ("method", "endpoint"),
    [("POST", "signup"), ("DELETE", "participants")],
)
def test_unknown_activity_returns_not_found(client, activities, method, endpoint):
    before = client.get("/activities").json()

    response = client.request(
        method, f"/activities/Unknown Activity/{endpoint}", params={"email": EMAIL}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activities == before


@pytest.mark.parametrize(
    ("method", "url"),
    [("POST", SIGNUP_URL), ("DELETE", PARTICIPANTS_URL)],
)
def test_missing_email_returns_validation_error(client, activities, method, url):
    before = list(activities[ACTIVITY]["participants"])

    response = client.request(method, url)

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"]
        for error in response.json()["detail"]
    )
    assert activities[ACTIVITY]["participants"] == before
