def test_openapi_documents_activity_routes(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "get" in paths["/activities"]
    assert "post" in paths["/activities/{activity_name}/signup"]
    assert "delete" in paths["/activities/{activity_name}/participants"]


def test_static_files_are_served(client):
    response = client.get("/static/index.html")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert client.get("/static/missing-file.html").status_code == 404