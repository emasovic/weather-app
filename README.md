# Weather app

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [API Documentation](#api-documentation)

## Overview

This meteorological web application collects, stores, and visualizes weather data from IoT devices installed in meteorological stations across various cities. The application allows users to view real-time weather updates, submit daily forecasts, and access historical weather data.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.11
- pip (Python package installer)
- Docker (optional, for containerized setup)
- SQLite (if not using Docker)

## Installation

1. **Create a Virtual Environment (optional but recommended)**:

- python -m venv venv
- source venv/bin/activate # On Windows use `venv\Scripts\activate`

2. **Install Required Packages**:

- pip install -r requirements.txt

## Running the Application

1. **Build the Docker Image**:

- docker build -t weather-app .

2. **Run the Docker Container**:

- docker run weather-app

## Testing the Application

1. Ensure your virtual environment is activated (if using):

2. Run the test suite:

- pytest tests/

## API Documentation

The application provides a RESTful API. You can find the API endpoints and documentation at http://localhost:8000/docs after running the application.
