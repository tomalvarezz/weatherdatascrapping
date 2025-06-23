@echo off

REM Step 1: Create virtual environment (Optional, but better for portability as it doesnt crash with other dependency stuff in you local machine)
python -m venv venv
call venv\Scripts\activate

REM Step 2: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Step 3: Create .env if not exists
IF NOT EXIST .env (
    echo OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast > .env
    echo GEOCODING_URL=https://geocoding-api.open-meteo.com/v1/search >> .env
    echo .env file created.
) ELSE (
    echo .env already exists.
)

REM Step 4: Run the FastAPI server
echo Starting FastAPI server...
uvicorn main:app --reload
