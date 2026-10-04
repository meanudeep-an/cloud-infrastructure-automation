import pytest
from botocore.exceptions import ClientError

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


def test_get_iam_users_when_empty():
    class MockIAMClient:
        def list_users(self):
            return {"Users": []}

    users = get_iam_users(MockIAMClient())

    assert users == []


def test_get_iam_users_when_aws_api_fails():
    class MockIAMClient:
        def list_users(self):
            raise ClientError(
                {
                    "Error": {
                        "Code": "AccessDenied",
                        "Message": "User is not authorized to perform this operation",
                    }
                },
                "ListUsers",
            )

    with pytest.raises(ClientError) as error:
        get_iam_users(MockIAMClient())

    assert error.value.response["Error"]["Code"] == "AccessDenied"
