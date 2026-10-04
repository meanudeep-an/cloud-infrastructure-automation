def get_iam_users(iam_client):
    response = iam_client.list_users()
    return response["Users"]
