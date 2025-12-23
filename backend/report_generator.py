from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class PDFReportGenerator:
    """Professional PDF Report Generator - Enhanced with Vibrant Design"""
    
    def __init__(self, output_file='report.pdf'):
        self.output_file = output_file
        self.doc = SimpleDocTemplate(output_file, pagesize=A4,
                                     rightMargin=0.5*inch, leftMargin=0.5*inch,
                                     topMargin=0.75*inch, bottomMargin=0.75*inch)
        self.story = []
        self.styles = getSampleStyleSheet()
        
        # Professional color palette
        self.colors = {
            'primary': colors.HexColor('#2E86DE'),
            'secondary': colors.HexColor('#10AC84'),
            'accent': colors.HexColor('#EE5A6F'),
            'dark': colors.HexColor('#2c3e50'),
            'light_bg': colors.HexColor('#ecf0f1'),
            'success': colors.HexColor('#00D2D3'),
            'warning': colors.HexColor('#F79F1F'),
            'info': colors.HexColor('#5F27CD')
        }
        
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles with vibrant colors"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=self.colors['primary'],
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=38
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.white,
            spaceAfter=14,
            spaceBefore=14,
            fontName='Helvetica-Bold',
            backColor=self.colors['primary'],
            borderPadding=10,
            leading=22
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=self.colors['dark'],
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            leftIndent=10,
            borderColor=self.colors['secondary'],
            borderWidth=0,
            borderPadding=0,
            borderRadius=None
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            textColor=self.colors['dark'],
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=self.colors['secondary'],
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['dark'],
            backColor=colors.HexColor('#fff3cd'),
            borderColor=self.colors['warning'],
            borderWidth=2,
            borderPadding=12,
            spaceAfter=12,
            leading=16
        ))
    
    def add_title_page(self, title, subtitle, date_str):
        """Add professional title page with vibrant Insightify branding"""
        # Top branding with gradient effect
        self.story.append(Spacer(1, 0.3*inch))
        branding = Paragraph(
            "<font size=18 color='#2E86DE'><b>📊 INSIGHTIFY</b></font><br/><font size=10 color='#10AC84'><b>Professional Data Analysis & Intelligent Reporting</b></font>",
            ParagraphStyle(
                'Branding',
                parent=self.styles['Normal'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=30
            )
        )
        self.story.append(branding)
        
        # Decorative separator
        separator_data = [['']]
        separator_table = Table(separator_data, colWidths=[6.5*inch])
        separator_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 3, self.colors['primary']),
            ('LINEBELOW', (0, 0), (-1, -1), 1, self.colors['secondary']),
        ]))
        self.story.append(separator_table)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Title
        self.story.append(Spacer(1, 1*inch))
        title_para = Paragraph(title, self.styles['CustomTitle'])
        self.story.append(title_para)
        
        # Subtitle
        self.story.append(Spacer(1, 0.3*inch))
        subtitle_para = Paragraph(subtitle, self.styles['Subtitle'])
        self.story.append(subtitle_para)
        
        # Metadata box
        self.story.append(Spacer(1, 1*inch))
        metadata_data = [
            ['Report Generated:', date_str],
            ['Platform:', 'Insightify Professional Analytics'],
            ['Engine Version:', '3.0 (Enhanced AI Analytics)'],
            ['Report Status:', 'Confidential']
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['light_bg']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['dark']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['primary']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1.5, self.colors['primary']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        self.story.append(metadata_table)
        
        # Footer branding
        self.story.append(Spacer(1, 1.5*inch))
        footer_branding = Paragraph(
            "<i><font color='#7f8c8d'>Generated by Insightify™ - AI-Powered Data Analysis Platform<br/>Transforming Data into Actionable Insights</font></i>",
            ParagraphStyle(
                'FooterBranding',
                parent=self.styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER
            )
        )
        self.story.append(footer_branding)
        
        self.story.append(PageBreak())
    
    def add_executive_summary(self, analysis_results):
        """Add executive summary section with enhanced styling"""
        self.story.append(Paragraph("📋 Executive Summary", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        basic_stats = analysis_results.get('basic_stats', {})
        
        summary_text = f"""
        <b><font color='#2E86DE'>Report Overview:</font></b><br/>
        This comprehensive data analysis report presents key insights and actionable metrics from the provided dataset.
        Our analysis covers <b><font color='#EE5A6F'>{basic_stats.get('total_records', 0):,}</font></b> records across <b><font color='#EE5A6F'>{basic_stats.get('total_columns', 0)}</font></b> columns, 
        utilizing advanced statistical methods and visualization techniques.<br/><br/>
        
        <b><font color='#2E86DE'>Dataset Composition:</font></b><br/>
        • Numeric Variables: <b><font color='#10AC84'>{basic_stats.get('numeric_columns', 0)}</font></b> columns<br/>
        • Categorical Variables: <b><font color='#10AC84'>{basic_stats.get('categorical_columns', 0)}</font></b> columns<br/>
        • Temporal Variables: <b><font color='#10AC84'>{basic_stats.get('date_columns', 0)}</font></b> columns<br/>
        • Data Completeness: <b><font color='#F79F1F'>{basic_stats.get('missing_values', 0)}</font></b> missing values detected<br/>
        • Data Uniqueness: <b><font color='#F79F1F'>{basic_stats.get('duplicate_rows', 0)}</font></b> duplicate rows identified<br/>
        • Memory Footprint: <b>{basic_stats.get('memory_usage', 'N/A')}</b>
        """
        
        self.story.append(Paragraph(summary_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_insights(self, analysis_results):
        """Add data-driven insights section"""
        if 'insights' not in analysis_results or not analysis_results['insights']:
            return
        
        self.story.append(Paragraph("💡 Key Insights & Findings", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        insights = analysis_results['insights']
        
        insights_text = "<b><font color='#2E86DE'>Our analysis has uncovered the following significant patterns:</font></b><br/><br/>"
        
        for i, insight in enumerate(insights[:10], 1):  # Limit to top 10 insights
            insights_text += f"<b>{i}.</b> {insight}<br/><br/>"
        
        insight_para = Paragraph(insights_text, self.styles['CustomBody'])
        self.story.append(insight_para)
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(PageBreak())
    
    def add_numeric_analysis(self, analysis_results):
        """Add numeric analysis section with vibrant tables"""
        if 'numeric_analysis' not in analysis_results:
            return
            
        self.story.append(Paragraph("📊 Numeric Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        numeric_data = analysis_results['numeric_analysis']
        
        # Enhanced statistics table
        table_data = [['Column', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'IQR']]
        
        for col, stats in list(numeric_data.items())[:15]:  # Show top 15
            row = [
                col[:18],
                f"{stats['mean']:.2f}",
                f"{stats['median']:.2f}",
                f"{stats['std']:.2f}",
                f"{stats['min']:.2f}",
                f"{stats['max']:.2f}",
                f"{stats['iqr']:.2f}"
            ]
            table_data.append(row)
        
        if len(numeric_data) > 15:
            self.story.append(Paragraph(f"<i><font color='#F79F1F'>Showing top 15 of {len(numeric_data)} numeric columns</font></i>", self.styles['Normal']))
            self.story.append(Spacer(1, 0.1*inch))

        t = Table(table_data, colWidths=[1.3*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1.5, self.colors['dark']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_bg']]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('PADDING', (0, 1), (-1, -1), 6),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(PageBreak())

    def add_categorical_analysis(self, analysis_results):
        """Add categorical analysis section with enhanced styling"""
        if 'categorical_analysis' not in analysis_results:
            return

        self.story.append(Paragraph("📑 Categorical Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        cat_data = analysis_results['categorical_analysis']
        
        for col, stats in list(cat_data.items())[:5]:
            # Column header
            col_header = Paragraph(
                f"<b><font color='#2E86DE' size=12>Category: {col}</font></b>",
                self.styles['Normal']
            )
            self.story.append(col_header)
            self.story.append(Spacer(1, 0.05*inch))
            
            # Stats summary
            stats_text = f"<b>Unique Values:</b> {stats['unique_count']} | <b>Most Frequent:</b> '{stats['most_frequent']}' ({stats['concentration']:.1f}% of data)"
            self.story.append(Paragraph(stats_text, self.styles['Normal']))
            self.story.append(Spacer(1, 0.1*inch))
            
            # Top values table
            top_vals = [['Value', 'Count', 'Percentage']]
            total = sum(stats['top_values'].values())
            for val, count in list(stats['top_values'].items())[:10]:
                pct = (count / total * 100) if total > 0 else 0
                top_vals.append([str(val)[:25], f"{count:,}", f"{pct:.1f}%"])
            
            t = Table(top_vals, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['secondary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1.5, self.colors['dark']),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_bg']]),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            self.story.append(t)
            self.story.append(Spacer(1, 0.25*inch))
            
        self.story.append(PageBreak())

    def add_correlations(self, analysis_results):
        """Add correlation analysis with strength indicators"""
        if 'correlations' not in analysis_results:
            return

        self.story.append(Paragraph("🔗 Correlation Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        corrs = analysis_results['correlations']
        if not corrs:
            self.story.append(Paragraph("<i>No significant correlations detected in the dataset.</i>", self.styles['Normal']))
            return

        intro_text = f"<b><font color='#2E86DE'>Identified {len(corrs)} significant relationships between variables:</font></b><br/>" \
                     "Correlation coefficients range from -1 (perfect negative) to +1 (perfect positive)."
        self.story.append(Paragraph(intro_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.15*inch))

        table_data = [['Variables Pair', 'Coefficient', 'Strength', 'Direction']]
        for corr in corrs[:12]:  # Show top 12
            # Color code by strength
            coef_val = corr['value']
            if abs(coef_val) > 0.7:
                color_code = '#00D2D3'  # Strong - cyan
            elif abs(coef_val) > 0.5:
                color_code = '#F79F1F'  # Moderate - orange
            else:
                color_code = '#7f8c8d'  # Weak - gray
            
            table_data.append([
                corr['pair'][:35],
                f"{corr['value']:.4f}",
                corr['strength'],
                corr['direction']
            ])
            
        t = Table(table_data, colWidths=[2.8*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['accent']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1.5, self.colors['dark']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_bg']]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(PageBreak())

    def add_visualizations(self, chart_dir):
        """Add visualization charts to report"""
        self.story.append(Paragraph("📈 Data Visualizations", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        if not os.path.exists(chart_dir):
            return

        chart_files = sorted([f for f in os.listdir(chart_dir) if f.endswith('.png')])
        
        for i, chart_file in enumerate(chart_files):
            chart_path = os.path.join(chart_dir, chart_file)
            
            # Extract and format chart title
            chart_title = chart_file.replace('_', ' ').replace('.png', '')
            if len(chart_title) > 2 and chart_title[:2].isdigit():
                chart_title = chart_title[3:]  # Remove "00_" prefix
            
            # Add styled chart title
            title_para = Paragraph(
                f"<b><font color='#2E86DE' size=12>{chart_title.title()}</font></b>",
                self.styles['Normal']
            )
            self.story.append(title_para)
            self.story.append(Spacer(1, 0.05*inch))
            
            # Add image
            try:
                img = Image(chart_path, width=6.5*inch, height=4*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.25*inch))
                
                # Add page break after every 2 charts
                if (i + 1) % 2 == 0 and i < len(chart_files) - 1:
                    self.story.append(PageBreak())
            except Exception as e:
                print(f"Error adding image {chart_file}: {e}")
        
        self.story.append(PageBreak())
    
    def add_conclusions(self):
        """Add conclusions section with actionable recommendations"""
        self.story.append(Paragraph("🎯 Conclusions & Recommendations", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.15*inch))
        
        conclusions_text = """
        <b><font color='#2E86DE' size=12>Key Findings:</font></b><br/><br/>
        
        <b>1. Data Quality Assessment:</b><br/>
        The dataset has undergone comprehensive quality checks. Review the Executive Summary for critical insights
        regarding data completeness, duplicate records, and overall integrity. Address any missing values or 
        duplicates identified before proceeding with predictive modeling.<br/><br/>
        
        <b>2. Statistical Distribution Analysis:</b><br/>
        Our numeric analysis reveals the central tendencies, variability, and distribution patterns across all
        quantitative variables. Box plots highlight potential outliers that may require further investigation
        or treatment depending on your analytical objectives.<br/><br/>
        
        <b>3. Correlation & Relationship Discovery:</b><br/>
        The correlation analysis has identified statistically significant relationships between variables.
        Strong positive or negative correlations (|r| > 0.7) indicate potential predictive relationships that
        could be leveraged in machine learning models or business intelligence applications.<br/><br/>
        
        <b><font color='#10AC84' size=12>Actionable Recommendations:</font></b><br/><br/>
        
        ✓ <b>Investigate High-Correlation Pairs:</b> Variables with strong correlations warrant deeper analysis
        to determine causality versus mere association. Consider domain expertise when interpreting these relationships.<br/><br/>
        
        ✓ <b>Address Data Quality Issues:</b> Implement data cleaning protocols for missing values and duplicates.
        Consider imputation strategies or removal based on the nature and extent of missing data.<br/><br/>
        
        ✓ <b>Leverage Visualizations for Stakeholder Communication:</b> The generated charts provide clear,
        professional representations of your data suitable for executive presentations and decision-making forums.<br/><br/>
        
        ✓ <b>Monitor Categorical Distributions:</b> Highly concentrated categories or imbalanced classes may require
        special handling in predictive models (e.g., SMOTE for oversampling, stratified sampling).<br/><br/>
        
        ✓ <b>Temporal Pattern Exploration:</b> If time-series trends are present, consider seasonal decomposition
        and forecasting techniques to predict future patterns.
        """
        
        self.story.append(Paragraph(conclusions_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.4*inch))
        
        # Footer with timestamp
        footer_data = [[f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}']]
        footer_table = Table(footer_data, colWidths=[6.5*inch])
        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['light_bg']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['dark']),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 2, self.colors['primary']),
        ]))
        self.story.append(footer_table)
        
        self.story.append(Spacer(1, 0.2*inch))
        footer_text = """
        <i><font color='#7f8c8d'>This report contains proprietary and confidential business information. 
        Distribution should be limited to authorized personnel only. For questions about this analysis, 
        please contact your data analytics team.</font></i>
        """
        self.story.append(Paragraph(footer_text, self.styles['Normal']))
    
    def build(self):
        """Build and save the PDF"""
        try:
            self.doc.build(self.story)
            print(f"[✓] Professional PDF Report generated: {self.output_file}")
        except Exception as e:
            print(f"[✗] Error building PDF: {e}")
            import traceback
            traceback.print_exc()
