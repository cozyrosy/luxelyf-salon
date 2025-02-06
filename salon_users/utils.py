import requests
import random
from django.conf import settings

FAST2SMS_API_KEY = settings.FAST2SMS_API_KEY

def send_otp(mobile_number):
    otp = random.randint(100000, 999999)  # Generate 6-digit OTP
    message = f"Your OTP for login is {otp}. Do not share it with anyone."

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "sender_id": "TXTIND",
        "route": "otp",
        "variables_values": str(otp),  # Ensure OTP is passed as a string
        "numbers": mobile_number,  # Use the mobile_number passed to the function
    }

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)  # Use json=payload instead of data=payload

    return otp if response.status_code == 200 else None
