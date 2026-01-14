"""
Flask application for ETL pipeline
Main entry point for the web interface
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE
from etl.extract import extract
from etl.transform import transform
from etl.load import load_data, get_record_count
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_etl():
    """Process ETL pipeline for uploaded file"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF, CSV, or Excel files.', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filename}")
        
        try:
            # Extract phase
            logger.info("Starting extraction...")
            extracted_df = extract(filepath)
            logger.info(f"Extracted {len(extracted_df)} records")
            
            # Transform phase
            logger.info("Starting transformation...")
            transformed_df = transform(extracted_df)
            logger.info(f"Transformed {len(transformed_df)} records")
            
            # Load phase
            logger.info("Starting load...")
            rows_inserted = load_data(transformed_df)
            logger.info(f"Loaded {rows_inserted} records")
            
            # Get total record count
            total_records = get_record_count()
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            flash(f'ETL Process completed successfully! {rows_inserted} records inserted. Total records in database: {total_records}', 'success')
            
        except Exception as e:
            # Clean up uploaded file on error
            try:
                os.remove(filepath)
            except:
                pass
            
            error_msg = f"ETL Error: {str(e)}"
            logger.error(error_msg)
            flash(error_msg, 'error')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        flash(error_msg, 'error')
        return redirect(url_for('index'))


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'ETL Service is running'})


if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("=" * 60)
    print("Bank Statement ETL Application")
    print("=" * 60)
    print(f"Starting Flask server...")
    print(f"Open http://localhost:5000 in your browser")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

