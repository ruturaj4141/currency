# Currency Detector Web App

A web application that detects Indian currency notes using your device's camera.

## Features

- Real-time currency detection
- Voice feedback for visually impaired users
- Works on mobile and desktop browsers
- Switch between front and back cameras

## Deployment Guide

### 1. GitHub Setup

1. Create a new GitHub repository
2. Upload all files from this folder to the repository
   - Make sure `requirements.txt` is in the root directory
   - Ensure the model file is in the `model` folder

### 2. Render Deployment

1. Go to [Render.com](https://render.com) and create an account
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: currency-detector
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. Add Environment Variable (optional):
   - Key: `PYTHON_VERSION`
   - Value: `3.9.0`

6. Click "Create Web Service"

Your app will be deployed at a URL like: `https://currency-detector-xxxx.onrender.com`

## Local Development

To run the app locally:

```
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.
