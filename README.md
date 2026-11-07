# St Martin Counsellors Backend

FastAPI backend for the St Martin Counsellors platform. This service handles authenticated admin access, validates Supabase user sessions, sends one-time passcodes (OTP) via email, and verifies the codes before allowing admin actions.

## Overview

The backend is designed to protect admin-only endpoints by requiring a valid Supabase session token and verifying a time-based OTP generated with TOTP. It is intended to work with the frontend application in the companion St Martin front-end project.

## Features

- FastAPI application with CORS enabled for the local frontend
- Supabase authentication and user lookup
- Bearer-token validation for admin users
- Email-based OTP delivery for two-step admin verification
- Time-based one-time password verification using `pyotp`
- Rate limiting support with `slowapi`

## Tech Stack

- Python 3.15+
- FastAPI
- Supabase
- PyOTP
- SMTP email delivery through Gmail
- Python-dotenv

## Project Structure

```text
stmartin_backend/
├── main.py                 # FastAPI application and routes
├── email_client.py         # Sends OTP emails
├── password_generator.py   # Generates and verifies TOTP codes
├── stmartin_supabase.py    # Supabase client and user validation
├── custom_response.py      # Custom response helper
├── models/
│   └── Counsellor.py       # Data model used for Supabase user data
├── requirements.txt
├── .env                    # Local environment variables (not committed)
└── README.md
```

## Requirements

- Python 3.15 or newer
- A Supabase project with a `counsellors` table or equivalent user profile data
- An SMTP-enabled email account (currently configured for Gmail SMTP in `email_client.py`)

## Environment Variables

Create a `.env` file in the project root with the following values:

```env
supabase_url=your_supabase_project_url
supabase_key=your_supabase_service_or_anon_key
sender_email=your_email@example.com
sender_password=your_app_password
otp_secret=your_shared_otp_secret
```

Notes:

- Use an app password for Gmail rather than your main account password.
- Keep the `.env` file out of version control.
- The `otp_secret` should be a secure secret used for TOTP generation.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate      # Windows PowerShell

pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The app will be available at:

- http://localhost:8000

## API Endpoints

### Admin verification

- `GET /admin/verification`
  - Requires a valid bearer token from Supabase-authenticated user
  - Sends a one-time verification code to the authenticated user email

- `POST /admin/verify-code/{code}`
  - Validates the submitted OTP against the configured TOTP secret
  - Returns a boolean verification result

## Security Notes

- Authentication is based on the Supabase access token and checks the user record in the `counsellors` table.
- The OTP is valid for a fixed time window and should be treated as a second factor for admin access.
- Do not expose secrets or `.env` values in public repositories.
- Keep the frontend origin and backend CORS settings aligned with your deployment environment.

## Development Notes

This backend is meant to support the admin login workflow used by the St Martin counselling platform. If you are integrating with the frontend, ensure the frontend sends the bearer token in the `Authorization` header and matches the expected CORS configuration.

