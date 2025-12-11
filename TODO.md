t# TODO: Fix M-Pesa STK Push Issues

## Steps to Complete
- [x] Add phone number validation in stk_push view (ensure starts with 254 and is 12 digits, including 9-digit format)
- [x] Make callback URL configurable via environment variable
- [x] Improve logging in views.py (replace print with logging)
- [x] Add error handling for API response in stk_push
- [x] Test the changes by running the app and checking logs
