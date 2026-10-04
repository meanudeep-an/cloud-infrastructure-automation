import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .iam import get_iam_users

def get_identity(sts_client):
    return sts_client.get_caller_identity()


def get_iam_users(iam_client):
    response = iam_client.list_users()
    return response["Users"]


def main():
    try:
        sts_client = boto3.client("sts")
        iam_client = boto3.client("iam")

        identity = get_identity(sts_client)
        users = get_iam_users(iam_client)

        print("AWS Infrastructure Inventory")
        print("-----------------------------")

        print("\nAccount")
        print(f"  Account : {identity['Account']}")
        print(f"  Identity: {identity['Arn']}")

        print("\nIAM Users")

        if not users:
            print("  None")
        else:
            for user in users:
                print(f"  {user['UserName']}  |  {user['CreateDate']}")

    except (BotoCoreError, ClientError) as error:
        print(f"AWS API error: {error}")


if __name__ == "__main__":
    main()
