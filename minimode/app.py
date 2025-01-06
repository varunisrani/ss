from quart import Quart, request, jsonify, make_response
from quart_cors import cors
import logging
import os
from pathlib import Path
from market_analysis_crew import get_report_generator, create_reports
import time

app = Quart(__name__)

# CORS configuration
app = cors(app, allow_origin=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004", "http://localhost:3005", "http://localhost:3006", "http://localhost:3007", "http://localhost:3008", "http://localhost:3009", "http://localhost:3010"], 
          allow_methods=["GET", "POST", "OPTIONS"],
          allow_headers=["Content-Type"],
          max_age=3600)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Update route handlers to be async
@app.route('/api/report-content/<filename>', methods=['GET', 'OPTIONS'])
async def get_report_content(filename):
    """Get content of a specific report"""
    if request.method == 'OPTIONS':
        response = await make_response()
        return response

    try:
        # Security check to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            return jsonify({
                'status': 'error',
                'message': 'Invalid filename'
            }), 400
            
        # Look for the file in both the current directory and reports directory
        file_path = os.path.join(os.getcwd(), filename)
        reports_dir = os.path.join(os.getcwd(), 'reports')
        
        if os.path.exists(file_path):
            target_path = file_path
        elif os.path.exists(os.path.join(reports_dir, filename)):
            target_path = os.path.join(reports_dir, filename)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Report not found'
            }), 404
            
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return jsonify({
            'status': 'success',
            'content': content,
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error reading report content: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/reports', methods=['GET', 'OPTIONS'])
async def get_reports():
    """Get all generated reports"""
    if request.method == 'OPTIONS':
        response = await make_response()
        return response

    try:
        # Get all report files from the directory
        report_files = []
        current_dir = os.getcwd()
        
        # Function to process files in a directory
        def process_directory(directory):
            for file in os.listdir(directory):
                if file.endswith('_report.md'):
                    # Parse filename to get metadata
                    parts = file.replace('_report.md', '').split('_')
                    company_name = parts[0]
                    report_type = '_'.join(parts[1:-2]) if len(parts) > 3 else parts[1]
                    timestamp = '_'.join(parts[-2:])
                    
                    report_files.append({
                        'company_name': company_name,
                        'report_type': report_type,
                        'timestamp': timestamp,
                        'filename': file
                    })
        
        # Check both current directory and reports directory
        process_directory(current_dir)
        reports_dir = os.path.join(current_dir, 'reports')
        if os.path.exists(reports_dir):
            process_directory(reports_dir)
        
        response = jsonify({
            'status': 'success',
            'reports': sorted(report_files, key=lambda x: x['timestamp'], reverse=True)
        })
        
        # Add CORS headers
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
        
    except Exception as e:
        logger.error(f"Error fetching reports: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
async def generate_report():
    """Endpoint for generating any type of report"""
    if request.method == 'OPTIONS':
        response = await make_response()
        return response

    try:
        data = await request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400

        report_type = data.get('report_type')
        inputs = data.get('inputs', {})

        # Validate inputs
        if not report_type:
            return jsonify({
                'status': 'error',
                'message': 'Report type is required'
            }), 400

        if not inputs.get('company_name'):
            return jsonify({
                'status': 'error',
                'message': 'Company name is required'
            }), 400

        # Report-specific validation
        if report_type == 'competitor_tracking':
            if not inputs.get('competitors'):
                return jsonify({
                    'status': 'error',
                    'message': 'Competitors list is required'
                }), 400
            if not inputs.get('metrics'):
                return jsonify({
                    'status': 'error',
                    'message': 'Tracking metrics are required'
                }), 400

        elif report_type == 'icp_report':
            required_fields = [
                'business_model',
                'target_market',
                'company_size',
                'annual_revenue'
            ]
            missing = [field for field in required_fields if not inputs.get(field)]
            if missing:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required fields: {", ".join(missing)}'
                }), 400

        elif report_type == 'gap_analysis':
            required_fields = [
                'focus_areas',
                'analysis_depth',
                'market_region'
            ]
            missing = [field for field in required_fields if not inputs.get(field)]
            if missing:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required fields: {", ".join(missing)}'
                }), 400

        logger.info(f"Starting {report_type} for {inputs['company_name']}")
        
        # Generate report using the report generator
        generator = get_report_generator()
        result = generator.generate_report(report_type, inputs)
        
        # Create report files
        validation_file, report_file = create_reports(result, inputs, report_type)
        
        # Read the generated files
        with open(validation_file, 'r') as f:
            validation_report = f.read()
            
        with open(report_file, 'r') as f:
            analysis_report = f.read()
            
        return jsonify({
            'status': 'success',
            'validation_report': validation_report,
            'analysis_report': analysis_report,
            'summary': {
                'company': inputs['company_name'],
                'report_type': report_type,
                'industry': inputs.get('industry', ''),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_type': inputs.get('analysis_type', ''),
                'metrics': inputs.get('metrics', {}),
                'focus_areas': inputs.get('focus_areas', []),
                'market_region': inputs.get('market_region', 'global')
            }
        })

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/market-analysis', methods=['POST', 'OPTIONS'])
async def analyze_market():
    """Legacy endpoint for market analysis"""
    if request.method == 'OPTIONS':
        response = await make_response()
        return response

    try:
        data = await request.get_json()
        if not data or not data.get('company_name'):
            return jsonify({
                'status': 'error',
                'message': 'Company name is required'
            }), 400

        user_inputs = {
            "company_name": data.get('company_name'),
            "industry": data.get('industry', ''),
            "focus_areas": data.get('focus_areas', []),
            "time_period": data.get('time_period', 'current')
        }

        logger.info(f"Starting market analysis for {user_inputs['company_name']}")
        
        # Get the generator and start analysis
        try:
            generator = get_report_generator()
            result = generator.generate_report('market_analysis', user_inputs)
            
            # Generate reports
            validation_file, report_file = create_reports(result, user_inputs, 'market_analysis')
            
            # Read the reports
            with open(validation_file, 'r') as f:
                validation_report = f.read()
            
            with open(report_file, 'r') as f:
                analysis_report = f.read()
                
            return jsonify({
                'status': 'success',
                'validation_report': validation_report,
                'analysis_report': analysis_report,
                'summary': {
                    'company': user_inputs['company_name'],
                    'industry': user_inputs['industry'],
                    'focus_areas': user_inputs['focus_areas'],
                    'time_period': user_inputs['time_period']
                }
            })
        except Exception as e:
            logger.error(f"Error during report generation: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Error generating report: {str(e)}'
            }), 500

    except Exception as e:
        logger.error(f"Error in market analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/analyze-website', methods=['POST', 'OPTIONS'])
async def analyze_website():
    """Endpoint for analyzing a website"""
    if request.method == 'OPTIONS':
        response = await make_response()
        return response

    try:
        data = await request.get_json()
        if not data or not data.get('website_url'):
            return jsonify({
                'status': 'error',
                'message': 'Website URL is required'
            }), 400

        # Process the website analysis here...
        # For example, you might call a function to analyze the website
        # and return the results.

        return jsonify({
            'status': 'success',
            'message': 'Website analysis complete',
            # 'results': analysis_results  # Include actual results here
        })

    except Exception as e:
        logger.error(f"Error analyzing website: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)