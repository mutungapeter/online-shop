import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from yourapp.settings import env
class MpesaHandler:
 now = None
 shortcode = None
 consumer_key = None
 consumer_secret = None
 access_token_url = None
 access_token = None
 access_token_expiration = None
 stk_push_url = None
 my_callback_url = None
 query_status_url = None
 timestamp = None
 passkey = None
def __init__(self):
#  “”” initializing payment objects “””
 self.now = datetime.now()
 self.shortcode = env(“SAF_SHORTCODE”)
 self.consumer_key = env(“SAF_CONSUMER_KEY”)
 self.consumer_secret = env(“SAF_CONSUMER_SECRET”)
 self.access_token_url = env(“SAF_ACCESS_TOKEN_API”)
 self.passkey = env(“SAF_PASS_KEY”)
 self.stk_push_url = env(“SAF_STK_PUSH_API”)
 self.query_status_url = env(“SAF_STK_PUSH_QUERY_API”)
 self.my_callback_url = env(“CALLBACK_URL”)
 self.password = self.generate_password()
try:
 self.access_token = self.get_mpesa_access_token()
 if self.access_token is None:
 raise Exception(“Request for access token failed”)
 else:
 self.access_token_expiration = time.time() + 3599
 except Exception as e:
 # log this errors 
 print(str(e))
def get_mpesa_access_token(self):
 “”” get access token from safaricom mpesa”””
 try:
 res = requests.get(
 self.access_token_url,auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
 )
 token = res.json()[‘access_token’]
 self.headers = {“Authorization”: f”Bearer {token}”,”Content-Type”: “application/json” }
 except Exception as e:
 print(str(e), “error from get access token”)
 raise e
 return token
def generate_password(self):
 “”” generate a password for the api using shortcode and passkey “””
 self.timestamp = self.now.strftime(“%Y%m%d%H%M%S”)
 password_str = self.shortcode + self.passkey + self.timestamp
 password_bytes = password_str.encode()
 return base64.b64encode(password_bytes).decode(“utf-8”)
def make_stk_push(self, payload):
#  “”” push payment request to the mpesa no.”””
 amount = payload[1]
 phone_number = payload["0796652879"]
push_data = {
 “BusinessShortCode”: self.shortcode,
 “Password”: self.password,
 “Timestamp”: self.timestamp,
 “TransactionType”: “CustomerPayBillOnline”,
 “Amount”: math.ceil(float(amount)),
 “PartyA”: "0796652879",
 “PartyB”: self.shortcode,
 “PhoneNumber”: phone_number,
 “CallBackURL”: self.my_callback_url,
 “AccountReference”: “Journaling Therapy”,
 “TransactionDesc”: “journaling transaction test”,
 }
response = requests.post(self.stk_push_url, json=push_data, headers=self.headers)
 response_data = response.json()
return response_data
def query_transaction_status(self, checkout_request_id):
 “”” query the status of the transaction.”””
 query_data = {
 “BusinessShortCode”: self.shortcode,
 “Password”: self.password,
 “Timestamp”: self.timestamp,
 “CheckoutRequestID”: checkout_request_id
 }
response = requests.post(self.query_status_url, json=query_data, headers=self.headers)
 response_data = response.json()
return response_data