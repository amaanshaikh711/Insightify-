"""
Insightify - Streamlit App
Professional Data Analysis & Report Generation
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from backend.data_analyzer import DataAnalyzer
from backend.report_generator import PDFReportGenerator

# Page configuration
st.set_page_config(
    page_title="Insightify - Professional Report Generation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .config-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 
10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'report_path' not in st.session_state:
    st.session_state.report_path = None

# Header
st.markdown('<h1 class="main-header">📊 Insightify</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Data Analysis & Report Generation</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Report Settings
    st.subheader("Report Settings")
    report_title = st.text_input("Report Title", value="Professional Data Analysis Report")
    report_subtitle = st.text_input("Report Subtitle", value="Comprehensive Analysis & Insights")
    
    st.markdown("---")
    
    # Chart Configuration
    st.subheader("📊 Chart Configuration")
    st.markdown('<div class="config-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_histograms = st.checkbox("📊 Histograms", value=True)
        include_pie_charts = st.checkbox("🥧 Pie Charts", value=True)
    
    with col2:
        include_box_plots = st.checkbox("📦 Box Plots", value=True)
        include_line_charts = st.checkbox("📈 Line Charts", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About
    with st.expander("ℹ️ About Insightify"):
        st.write("""
        **Insightify** is a professional data analysis and report generation platform.
        
        **Features:**
        - Comprehensive statistical analysis
        - Professional visualizations
        - PDF report generation
        - Customizable chart types
        - Data-driven insights
        
        **Version:** 3.0
        """)

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Generate", "📊 Data Preview", "📄 Download Report"])

with tab1:
    st.header("Upload Your Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your CSV file (max 500MB)"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file != st.session_state.uploaded_file:
                st.session_state.df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_file = uploaded_file
            
            df = st.session_state.df
            
            # Display file info
            st.success(f"✅ File loaded successfully: {uploaded_file.name}")
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="stat-box"><div class="stat-value">{:,}</div><div class="stat-label">Rows</div></div>'.format(len(df)), unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="stat-box"><div class="stat-value">{}</div><div class="stat-label">Columns</div></div>'.format(len(df.columns)), unsafe_allow_html=True)
            
            with col3:
                size_mb = uploaded_file.size / (1024 * 1024)
                st.markdown('<div class="stat-box"><div class="stat-value">{:.2f} MB</div><div class="stat-label">File Size</div></div>'.format(size_mb), unsafe_allow_html=True)
            
            with col4:
                missing = df.isnull().sum().sum()
                st.markdown('<div class="stat-box"><div class="stat-value">{:,}</div><div class="stat-label">Missing Values</div></div>'.format(missing), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Generate report button
            if st.button("🚀 Generate Professional Report", type="primary"):
                with st.spinner("Generating report... This may take a few minutes."):
                    try:
                        # Save uploaded file temporarily
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        upload_dir = "data"
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        temp_file_path = os.path.join(upload_dir, f"upload_{timestamp}_{uploaded_file.name}")
                        with open(temp_file_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Prepare output paths
                        output_dir = "output"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        output_pdf = os.path.join(output_dir, f"report_{timestamp}.pdf")
                        chart_dir = os.path.join(output_dir, f"charts_{timestamp}")
                        
                        # Chart configuration
                        chart_config = {
                            'histograms': include_histograms,
                            'pie_charts': include_pie_charts,
                            'box_plots': include_box_plots,
                            'line_charts': include_line_charts
                        }
                        
                        # Progress indicators
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Step 1: Analyze data
                        status_text.text("📊 Analyzing data...")
                        progress_bar.progress(20)
                        analyzer = DataAnalyzer(temp_file_path)
                        analysis_results = analyzer.perform_analysis()
                        
                        # Step 2: Generate charts
                        status_text.text("📈 Generating visualizations...")
                        progress_bar.progress(50)
                        analyzer.generate_charts(chart_dir, chart_config)
                        
                        # Step 3: Create PDF
                        status_text.text("📄 Creating PDF report...")
                        progress_bar.progress(75)
                        report_gen = PDFReportGenerator(output_pdf)
                        report_gen.add_title_page(report_title, report_subtitle, datetime.now().strftime("%B %d, %Y"))
                        report_gen.add_executive_summary(analysis_results)
                        report_gen.add_insights(analysis_results)
                        report_gen.add_numeric_analysis(analysis_results)
                        report_gen.add_categorical_analysis(analysis_results)
                        report_gen.add_correlations(analysis_results)
                        report_gen.add_visualizations(chart_dir)
                        report_gen.add_conclusions()
                        report_gen.build()
                        
                        # Complete
                        status_text.text("✅ Report generated successfully!")
                        progress_bar.progress(100)
                        
                        st.session_state.report_path = output_pdf
                        
                        st.success(f"🎉 Report generated successfully!")
                        st.balloons()
                        
                        # Show download button
                        with open(output_pdf, 'rb') as f:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=f,
                                file_name=f"insightify_report_{timestamp}.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                        
                        # Show insights
                        if 'insights' in analysis_results:
                            st.markdown("### 💡 Key Insights")
                            for i, insight in enumerate(analysis_results['insights'][:5], 1):
                                st.info(f"{i}. {insight}")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating report: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    else:
        st.info("👆 Please upload a CSV file to get started")

with tab2:
    st.header("Data Preview")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Data preview options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("📋 First Rows")
        
        with col2:
            n_rows = st.number_input("Rows to display", min_value=5, max_value=100, value=10)
        
        st.dataframe(df.head(n_rows), use_container_width=True)
        
        st.markdown("---")
        
        # Column information
        st.subheader("📊 Column Information")
        
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        
        st.dataframe(col_info, use_container_width=True)
        
        st.markdown("---")
        
        # Basic statistics
        st.subheader("📈 Basic Statistics")
        st.dataframe(df.describe(), use_container_width=True)
    
    else:
        st.info("📤 Upload a file first to see data preview")

with tab3:
    st.header("Download Report")
    
    if st.session_state.report_path and os.path.exists(st.session_state.report_path):
        st.success("✅ Report is ready for download!")
        
        with open(st.session_state.report_path, 'rb') as f:
            st.download_button(
                label="📥 Download PDF Report",
                data=f,
                file_name=os.path.basename(st.session_state.report_path),
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        
        st.info(f"📄 Report location: `{st.session_state.report_path}`")
    
    else:
        st.info("📊 Generate a report first to download it")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Insightify</strong> - Professional Data Analysis & Report Generation</p>
    <p>Version 3.0 | Created with Streamlit | © 2025</p>
</div>
""", unsafe_allow_html=True)
