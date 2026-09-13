#!/usr/bin/env python3
"""
Insightify Web Server
Serves the professional web interface and handles report generation
"""

import os
import sys
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from backend.data_analyzer import DataAnalyzer
from backend.report_generator import PDFReportGenerator

class InsightifyRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for Insightify"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Strip query string / fragment so "/?x=1" still serves the homepage
        # (otherwise it falls through to a directory listing)
        path_only = self.path.split('?', 1)[0].split('#', 1)[0]
        if path_only == '/':
            self.path = '/frontend/index.html'
        elif path_only in ['/styles.css', '/app.js', '/index.html', '/logo.png', '/favicon.png', '/favicon.svg', '/logo-full.png']:
            self.path = '/frontend' + path_only
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for report generation"""
        if self.path == '/api/generate-report':
            self.handle_report_generation()
        else:
            self.send_error(404)
    
    def parse_multipart_form_data(self):
        """Parse multipart/form-data without using deprecated cgi module"""
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            return None, None
        
        # Extract boundary
        boundary = None
        for part in content_type.split(';'):
            if 'boundary=' in part:
                boundary = part.split('boundary=')[1].strip()
                break
        
        if not boundary:
            return None, None
        
        # Read the body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        # Parse multipart data
        parts = body.split(f'--{boundary}'.encode())
        form_data = {}
        file_data = None
        
        for part in parts:
            if not part or part == b'--\r\n' or part == b'--':
                continue
            
            # Split headers and content
            if b'\r\n\r\n' in part:
                headers_part, content = part.split(b'\r\n\r\n', 1)
                content = content.rstrip(b'\r\n')
                
                # Parse Content-Disposition
                headers_str = headers_part.decode('utf-8', errors='ignore')
                
                if 'Content-Disposition' in headers_str:
                    # Extract field name
                    name_match = headers_str.split('name="')
                    if len(name_match) > 1:
                        field_name = name_match[1].split('"')[0]
                        
                        # Check if it's a file
                        if 'filename="' in headers_str:
                            filename_match = headers_str.split('filename="')
                            if len(filename_match) > 1:
                                filename = filename_match[1].split('"')[0]
                                file_data = {
                                    'filename': filename,
                                    'content': content
                                }
                        else:
                            # Regular form field
                            form_data[field_name] = content.decode('utf-8', errors='ignore')
        
        return form_data, file_data
    
    def handle_report_generation(self):
        """Handle report generation request with file upload"""
        try:
            print("[*] Received report generation request")
            
            # Parse form data
            form_data, file_data = self.parse_multipart_form_data()
            
            if not file_data or not file_data.get('filename'):
                self.send_json_response({'error': 'No file uploaded'}, 400)
                return
            
            print(f"[*] File received: {file_data['filename']}")
            
            # Save the file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            upload_dir = "data"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            safe_filename = f"upload_{timestamp}_{os.path.basename(file_data['filename'])}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_data['content'])
            
            print(f"[*] File saved to: {file_path}")
            
            # Get other form fields
            report_title = form_data.get('title', 'Professional Data Analysis Report')
            report_subtitle = form_data.get('subtitle', 'Comprehensive Analysis & Insights')
            
            # Get chart type configuration options (default to True if not specified)
            chart_config = {
                'histograms': form_data.get('includeHistograms', 'true').lower() == 'true',
                'pie_charts': form_data.get('includePieCharts', 'true').lower() == 'true',
                'box_plots': form_data.get('includeBoxPlots', 'true').lower() == 'true',
                'line_charts': form_data.get('includeLineCharts', 'true').lower() == 'true'
            }
            
            print(f"[*] Chart Configuration:")
            print(f"    - Histograms: {chart_config['histograms']}")
            print(f"    - Pie Charts: {chart_config['pie_charts']}")
            print(f"    - Box Plots: {chart_config['box_plots']}")
            print(f"    - Line Charts: {chart_config['line_charts']}")
            
            print(f"[*] Starting analysis...")
            
            # Generate report
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            output_pdf = os.path.join(output_dir, f"report_{timestamp}.pdf")
            chart_dir = os.path.join(output_dir, f"charts_{timestamp}")
            
            # Run analysis
            analyzer = DataAnalyzer(file_path)
            analysis_results = analyzer.perform_analysis()
            print(f"[*] Analysis complete")
            
            # Generate charts with configuration
            analyzer.generate_charts(chart_dir, chart_config)
            print(f"[*] Charts generated based on configuration")
            
            # Generate PDF
            report_gen = PDFReportGenerator(output_pdf)
            
            # Add all sections (charts will be filtered by the analyzer)
            report_gen.add_title_page(report_title, report_subtitle, datetime.now().strftime("%B %d, %Y"))
            report_gen.add_executive_summary(analysis_results)
            report_gen.add_insights(analysis_results)
            report_gen.add_numeric_analysis(analysis_results)
            report_gen.add_categorical_analysis(analysis_results)
            report_gen.add_correlations(analysis_results)
            report_gen.add_visualizations(chart_dir)
            report_gen.add_conclusions()
            report_gen.build()
            
            print(f"[✓] Report generated: {output_pdf}")
            
            self.send_json_response({
                'success': True,
                'report': '/' + output_pdf.replace(os.sep, '/'),
                'charts': '/' + chart_dir.replace(os.sep, '/'),
                'message': 'Report generated successfully'
            })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Always revalidate in local dev so edits show up on reload
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def run_server(port=8000):
    """Run the Insightify web server"""
    server_address = ('', port)
    # Serve from current directory (root) so we can access data, output, and frontend
    # We will handle the redirection to frontend/index.html in do_GET
    # ThreadingHTTPServer keeps the UI responsive while reports are generated
    httpd = ThreadingHTTPServer(server_address, InsightifyRequestHandler)
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║          INSIGHTIFY - WEB SERVER STARTED                   ║
    ║                                                            ║
    ║  📊 Professional Data Analysis & Report Generation        ║
    ║                                                            ║
    ║  Server running at: http://localhost:{port}                ║
    ║                                                            ║
    ║  Press Ctrl+C to stop the server                          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down server...")
        httpd.shutdown()
        print("[✓] Server stopped")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
