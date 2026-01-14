# Commands to Run the ETL Project

## Main Command to Start the Application

### Start Flask Application
```bash
python app.py
```

### Alternative: Using Flask Command
```bash
flask run
```

## Step-by-Step Instructions

### 1. Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python app.py
```

### 3. Access the Web Interface
Open your browser and navigate to:
```
http://localhost:5000
```

## PowerShell Commands (Windows)

### Run from Project Directory
```powershell
Set-Location "C:\Users\suman\OneDrive\Desktop\Project Complete ETL_QA"
python app.py
```

### Or Simply
```powershell
python app.py
```

## Expected Output

When you run `python app.py`, you should see:
```
============================================================
Bank Statement ETL Application
============================================================
Starting Flask server...
Open http://localhost:5000 in your browser
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## Using the Application

1. **Start the server**: Run `python app.py`
2. **Open browser**: Go to `http://localhost:5000`
3. **Upload file**: Select a bank statement (PDF, CSV, or Excel)
4. **Process**: Click "Process ETL" button
5. **View results**: Check SQL Server for loaded data

## Troubleshooting

### If Python is not found:
```bash
# Use full path to Python
C:\Python313\python.exe app.py
```

### If modules are missing:
```bash
# Install dependencies
pip install -r requirements.txt
```

### If port 5000 is already in use:
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or another port
```

### Check if SQL Server is running:
- Open SQL Server Management Studio (SSMS)
- Connect to `SUMANTH\SQLEXPRESS`
- Verify the service is running

## Quick Start Commands

### Complete Setup and Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start application
python app.py

# 3. Open browser to http://localhost:5000
```

## Background Process (Optional)

### Run in Background (Windows PowerShell)
```powershell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

### Stop the Application
Press `Ctrl+C` in the terminal where the app is running

