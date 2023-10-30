def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
    
def test_unauthorized_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_get_one_posts(client, test_post):
    res = client.get("/posts/1")
    assert res.status_code == 401