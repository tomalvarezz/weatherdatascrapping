#!/usr/bin/env bash
set -e  # Exit immediately if any command fails

# Step 1: Create virtual environment (useful for portability and wont interfere with local dependencies)
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Create .env if not exists
if [ ! -f .env ]; then
  echo "OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast" > .env
  echo "GEOCODING_URL=https://geocoding-api.open-meteo.com/v1/search" >> .env
  echo ".env file created."
else
  echo ".env already exists."
fi

# Step 4: Run the FastAPI server
echo "Starting FastAPI server..."
uvicorn main:app --reload
