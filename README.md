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

### Environment Configuration
1. **Create .env file**
   In both `minimode` and `promode` directories, create a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   SEPRER_API_KEY=your_free_seprer_key_here
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
- **API Key Issues**:
  - Verify .env file exists in correct directory
  - Check API key format and validity
  - Ensure no whitespace in API keys

For further assistance, consult project documentation or contact development team.
