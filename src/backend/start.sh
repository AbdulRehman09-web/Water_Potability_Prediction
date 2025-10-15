#!/bin/bash

echo "Water Potability Prediction"

echo "Downloading the model"
python setup.py

echo "Starting FastAPI server"
python app.py
