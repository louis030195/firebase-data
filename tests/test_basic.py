from firebase_data import export_auth
def test_export_auth():
    """
        Export Firebase authentication users to a local file
    """
    export_auth(
        "./svc.dev.json",
        "./data"
    )
    # Check a json file with users has properly been created in ./data
    with open("./data/users.json", "r") as f:
        users = f.read()
        assert len(users) > 0
