import requests
import os
from jsonschema import validate
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
USER_ID = os.getenv("USER_ID")

PRODUCT_SCHEMA = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "price": {
      "type": "integer"
    },
    "stock": {
      "type": "integer"
    },
    "category": {
      "type": "string"
    },
    "user_id": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "description",
    "price",
    "stock",
    "category",
    "user_id"
  ]
}

fake = Faker()
test_access_token = None

# allure title dll disini
def test_login_success():
    # step hitapi
    global test_access_token

    payload = {
    "email": "pyautoid@gmail.com",
    "password": "1234567890"
    }

    response = requests.post(f'{BASE_URL}/auth/v1/token?grant_type=password', headers={"apikey":API_KEY}, json=payload)
    data = response.json()
    # step assert
    assert response.status_code == 200
    assert data['expires_in'] == 3600

    test_access_token = data['access_token']

# CREATE PROD
def test_create_product_success():
    print(test_access_token)
    productnya = {
    "name": fake.catch_phrase(),
    "description": fake.text(max_nb_chars=200),
    "price": fake.random_number(digits=5),
    "stock": fake.random_int(min=1, max=100),
    "category": "Electronics",
    "user_id": USER_ID
    }
    
    print(productnya)

    headers = {"apikey":API_KEY,
            "Authorization": f"Bearer {test_access_token}",
            "Content-Type" : "application/json",
            "prefer":"return=representation"}

    response_prod = requests.post(f'{BASE_URL}/rest/v1/products',headers=headers, json=productnya)
    assert response_prod.status_code == 201
    data = response_prod.json()
    product = data[0]
    
    validate(instance=product, schema=PRODUCT_SCHEMA)
    