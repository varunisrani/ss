# Project Setup Guide

This guide will help you set up the frontend and backend for this project. Follow the instructions below to get started.

## Frontend Setup

1. **Install Dependencies**

   Navigate to the frontend directory and run the following command to install all necessary dependencies:

   ```bash
   npm install
   ```

2. **Start the Development Server**

   After installing the dependencies, start the development server with:

   ```bash
   npm run dev
   ```

   This will start the frontend application, and you can view it in your browser at `http://localhost:3000`.

## Backend Setup

The backend has two modes: `minimode` and `promode`. Follow the instructions for each mode below.

### Minimode Setup

1. **Navigate to the Minimode Directory**

   Change your directory to the `minimode` folder:

   ```bash
   cd minimode
   ```

2. **Install Python Dependencies**

   Ensure you have Python installed, then install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Minimode Server**

   Start the server by running:

   ```bash
   python app.py
   ```

   The server will start on the first available port from the list `[5000, 5001, 5002, 5003, 5004, 5005]`.

### Promode Setup

1. **Navigate to the Promode Directory**

   Change your directory to the `promode` folder:

   ```bash
   cd promode
   ```

2. **Install Python Dependencies**

   Ensure you have Python installed, then install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Promode Server**

   Start the server by running:

   ```bash
   python app.py
   ```

   The server will start on port `5001`.

## Additional Information

- Ensure that your Python environment is correctly set up and that you have the necessary permissions to install packages and run scripts.
- If you encounter any issues, check the console output for error messages and ensure all dependencies are correctly installed.

## Troubleshooting

- **CORS Issues**: If you encounter CORS issues, ensure that the backend server is configured to allow requests from your frontend's origin.
- **Port Conflicts**: If a port is already in use, the server will attempt to start on the next available port. Ensure no other applications are using the specified ports.

For further assistance, please refer to the project's documentation or contact the development team.

