from aws_inventory.iam import get_iam_users

def test_get_iam_users():
    class MockIAMClient:
        def list_users(self):
            return {
                "Users": [
                    {
                        "UserName": "test-user",
                        "UserId": "AIDATEST123",
                    }
                ]
            }

    users = get_iam_users(MockIAMClient())

    assert len(users) == 1
    assert users[0]["UserName"] == "test-user"
