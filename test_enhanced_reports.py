#!/usr/bin/env python3
"""
Quick Test Script for Enhanced Report Generation
Demonstrates the new professional visualizations and insights
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.data_analyzer import DataAnalyzer
from backend.report_generator import PDFReportGenerator

def test_enhanced_reports():
    """Test the new enhanced report generation features"""
    
    print("=" * 80)
    print("🧪 TESTING ENHANCED INSIGHTIFY REPORT GENERATION")
    print("=" * 80)
    
    # Find sample data
    sample_files = [
        "data/train.csv",
        "data/upload_20251206_180925_BMW sales data (2010-2024) (1).csv"
    ]
    
    test_file = None
    for file in sample_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if not test_file:
        print("❌ No sample data found!")
        return
    
    print(f"\n📁 Using test file: {test_file}")
    print("-" * 80)
    
    try:
        # Step 1: Initialize analyzer
        print("\n[1/5] Initializing Enhanced Data Analyzer...")
        analyzer = DataAnalyzer(test_file)
        print(f"      ✓ Detected {len(analyzer.numeric_cols)} numeric columns")
        print(f"      ✓ Detected {len(analyzer.categorical_cols)} categorical columns")
        print(f"      ✓ Detected {len(analyzer.date_cols)} date columns")
        
        # Step 2: Perform analysis
        print("\n[2/5] Performing Comprehensive Analysis...")
        analysis_results = analyzer.perform_analysis()
        print(f"      ✓ Generated {len(analysis_results.get('insights', []))} data-driven insights")
        
        # Step 3: Generate vibrant charts
        print("\n[3/5] Generating Professional Visualizations...")
        chart_dir = "output/test_enhanced_charts"
        analyzer.generate_charts(chart_dir)
        chart_count = len([f for f in os.listdir(chart_dir) if f.endswith('.png')])
        print(f"      ✓ Created {chart_count} professional charts with vibrant colors")
        
        # Step 4: Create enhanced PDF
        print("\n[4/5] Building Professional PDF Report...")
        output_pdf = "output/test_enhanced_report.pdf"
        report_gen = PDFReportGenerator(output_pdf)
        
        report_gen.add_title_page(
            "Enhanced Data Analysis Report",
            "Professional Analytics with Vibrant Visualizations",
            datetime.now().strftime("%B %d, %Y")
        )
        report_gen.add_executive_summary(analysis_results)
        report_gen.add_insights(analysis_results)
        report_gen.add_numeric_analysis(analysis_results)
        report_gen.add_categorical_analysis(analysis_results)
        report_gen.add_correlations(analysis_results)
        report_gen.add_visualizations(chart_dir)
        report_gen.add_conclusions()
        report_gen.build()
        
        # Step 5: Display sample insights
        print("\n[5/5] Sample Insights Generated:")
        print("-" * 80)
        for i, insight in enumerate(analysis_results.get('insights', [])[:5], 1):
            print(f"      {i}. {insight}")
        
        # Success summary
        print("\n" + "=" * 80)
        print("✅ ENHANCED REPORT GENERATION TEST COMPLETED!")
        print("=" * 80)
        print(f"\n📄 PDF Report: {os.path.abspath(output_pdf)}")
        print(f"📊 Charts Directory: {os.path.abspath(chart_dir)}")
        print(f"💡 Insights Generated: {len(analysis_results.get('insights', []))}")
        print(f"📈 Charts Created: {chart_count}")
        print("\n🎨 Features Demonstrated:")
        print("   ✓ Vibrant color palettes")
        print("   ✓ Professional box plots, pie charts, line graphs")
        print("   ✓ Enhanced correlation heatmaps")
        print("   ✓ Data-driven insights & recommendations")
        print("   ✓ Professional PDF with rich colors")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_enhanced_reports()
