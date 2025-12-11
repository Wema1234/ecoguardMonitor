1. Created a separate app that will contain our mpesa integration procedures
 2. create a model , transactions model
 3. settings.py project - configure the needed environmental credentials

 ## mpesa connections
 media details
=======
 ## MPESA INTEGRATION
 1. Created a separate app that will contain our mpesa integration procedures
 2. create a model , transactions model
 3. settings.py project - configure the needed environmental credentials

 ## M-Pesa Setup Instructions
 1. Copy `.env.example` to `.env` and fill in your credentials
 2. For M-Pesa sandbox testing:
    - Get consumer key and secret from Safaricom Developer Portal
    - Use shortcode: 174379 (sandbox)
    - Get passkey from Safaricom Developer Portal
    - Set callback URL to your ngrok/public URL + /mpesa/callback/
 3. For production, use live credentials and shortcode

 ## mpesa connections
 media details
