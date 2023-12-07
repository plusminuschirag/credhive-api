import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from unittest.mock import patch
from starlette import status

from main import app
from routers.authentication.authenticate import verify_token

load_dotenv()


client = TestClient(app)


# Mocking the database model for testing
class MockCreditModel:
    @staticmethod
    def get_all_credits():
        return [
            {
                "CIN": "375",
                "company_name": "KMT",
                "address": "PSC 9272, Box 0102\nAPO AE 04350",
                "registration_date": "2021-09-21",
                "number_of_employees": 525,
                "raised_capital": 2258687,
                "turnover": 28122016,
                "net_profit": 6759702,
                "contact_number": "526.729.1296x803",
                "contact_email": "jodi93@hill.com",
                "company_website": "http://www.thomas.com/",
                "loan_amount": 3500750,
                "loan_interest_percentage": 6.98,
                "account_status": "Inactive",
            },
            {
                "CIN": "502",
                "company_name": "Saunders Group",
                "address": "24247 Mary Center\nConnerton, DE 13500",
                "registration_date": "2018-07-10",
                "number_of_employees": 966,
                "raised_capital": 595366,
                "turnover": 46732561,
                "net_profit": 5383763,
                "contact_number": "(252)997-4860x895",
                "contact_email": "amberlewis@mann-deleon.org",
                "company_website": "http://www.rogers.com/",
                "loan_amount": 2620355,
                "loan_interest_percentage": 7.35,
                "account_status": "Active",
            },
            {
                "CIN": "633",
                "company_name": "Chaney LLC",
                "address": "35520 Mays Greens Apt. 951\nSouth Russellbury, WI 60387",
                "registration_date": "2021-04-11",
                "number_of_employees": 31,
                "raised_capital": 7756909,
                "turnover": 24783401,
                "net_profit": 9692941,
                "contact_number": "482.408.7561x453",
                "contact_email": "njohnson@stephens-smith.com",
                "company_website": "https://montoya.com/",
                "loan_amount": 314237,
                "loan_interest_percentage": 9.81,
                "account_status": "Pending",
            },
        ]


def mock_verify_token():
    return os.environ.get("JWT_USERNAME")


def get_mocked_token():
    response = client.post(
        "/authentication/token",
        data={"username": os.environ.get("JWT_USERNAME"), "password": os.environ.get("JWT_PASSWORD")},
    )
    data = response.json()
    return data["access_token"]


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.get_all_credits", side_effect=MockCreditModel.get_all_credits)
def test_get_credits_success(mock_verify, mock_model):
    token = get_mocked_token()
    response = client.get("/credits", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert len(response.json()["data"]) == 3


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.get_all_credits", return_value=[])
def test_get_credits_no_data(mock_verify, mock_model):
    token = get_mocked_token()
    response = client.get("/credits", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No credits found"


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.get_id_credit", return_value=MockCreditModel.get_all_credits()[0])
def test_get_credit_by_id_success(mock_verify, mock_get_id_credit):
    token = get_mocked_token()
    test_id = "375"  # Use a valid test ID
    response = client.get(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["CIN"] == test_id


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.get_id_credit", return_value=None)
def test_get_credit_by_id_not_found(mock_verify, mock_get_id_credit):
    token = get_mocked_token()
    test_id = "nonexistent_id"
    response = client.get(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Credit ID not found"


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.save_credit", return_value=(True, "Credit added successfully"))
def test_add_new_credit_success(mock_verify, mock_save_credit):
    token = get_mocked_token()
    new_credit_data = {
        "CIN": "616XOXO",
        "company_name": "Chaney LLC",
        "address": "35520 Mays Greens Apt. 951\nSouth Russellbury, WI 60387",
        "registration_date": "2021-04-11",
        "number_of_employees": 31,
        "raised_capital": 7756909,
        "turnover": 24783401,
        "net_profit": 9692941,
        "contact_number": "482.408.7561x453",
        "contact_email": "njohnson@stephens-smith.com",
        "company_website": "https://montoya.com/",
        "loan_amount": 314237,
        "loan_interest_percentage": 9.81,
        "account_status": "Pending",
    }
    response = client.post("/credits", headers={"Authorization": f"Bearer {token}"}, json=new_credit_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["saved"] == new_credit_data


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.save_credit", return_value=(False, "Credit not added"))
def test_add_new_credit_failure(mock_verify, mock_save_credit):
    token = get_mocked_token()
    new_credit_data = {
        "CIN": "633",
        "company_name": "Chaney LLC",
        "address": "35520 Mays Greens Apt. 951\nSouth Russellbury, WI 60387",
        "registration_date": "2021-04-11",
        "number_of_employees": 31,
        "raised_capital": 7756909,
        "turnover": 24783401,
        "net_profit": 9692941,
        "contact_number": "482.408.7561x453",
        "contact_email": "njohnson@stephens-smith.com",
        "company_website": "https://montoya.com/",
        "loan_amount": 314237,
        "loan_interest_percentage": 9.81,
        "account_status": "Pending",
    }
    response = client.post("/credits", headers={"Authorization": f"Bearer {token}"}, json=new_credit_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Credit not added"


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.update_credit_data", return_value=True)
def test_update_credit_success(mock_verify, mock_update_credit):
    token = get_mocked_token()
    test_id = "375"  # Use a valid test ID
    update_data = {
        "company_name": "KPMG",
    }
    response = client.put(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["updated"]


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.update_credit_data", return_value=False)
def test_update_credit_failure(mock_verify, mock_update_credit):
    token = get_mocked_token()
    test_id = "nonexistent_id"
    update_data = {
        "company_name": "KPMG",
    }
    response = client.put(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Credit ID not found for update"


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.delete_credit_by_id", return_value=True)
def test_delete_credit_success(mock_verify, mock_delete_credit):
    token = get_mocked_token()
    test_id = "375"  # Use a valid test ID
    response = client.delete(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["deleted_credit_id"] == test_id


@patch("routers.authentication.authenticate.verify_token", side_effect=mock_verify_token)
@patch("data.models.credit_model.CreditModel.delete_credit_by_id", return_value=False)
def test_delete_credit_failure(mock_verify, mock_delete_credit):
    token = get_mocked_token()
    test_id = "nonexistent_id"
    response = client.delete(f"/credits/{test_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Credit ID not found for deletion"
