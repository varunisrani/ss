# Project Setup Guide

## Frontend Setup
1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```
   Access at `http://localhost:3000`

## Backend Setup

### Common Setup (Both Modes)
1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

### Minimode Setup
1. **Navigate and Setup Environment**
   ```bash
   cd minimode
   python -m venv venv
   source venv/bin/activate  # Unix/MacOS
   # OR
   .\venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Server**
   ```bash
   python app.py
   ```
   Server starts on first available port: [5000-5005]

### Promode Setup
1. **Navigate and Setup Environment**
   ```bash
   cd promode
   python -m venv venv
   source venv/bin/activate  # Unix/MacOS
   # OR
   .\venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Server**
   ```bash
   python app.py
   ```
   Server starts on port 5001

## Additional Information
- Ensure Python and npm are installed
- Run only one mode (mini/pro) at a time
- Deactivate venv when switching modes: `deactivate`

## Troubleshooting
- **CORS Issues**: Verify backend allows frontend origin
- **Port Conflicts**: Check for running processes on required ports
- **Venv Issues**: 
  - Ensure correct venv activation
  - Verify Python version compatibility
  - Delete venv and recreate if dependencies conflict

For further assistance, consult project documentation or contact development team.