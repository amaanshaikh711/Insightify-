import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Professional Data Analysis Engine - Dynamic & Robust with Enhanced Visualizations"""
    
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        # Clean column names
        self.df.columns = [str(col).strip() for col in self.df.columns]
        
        self.analysis_results = {}
        self.charts = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Identify column types
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.date_cols = []
        
        # Try to identify date columns
        for col in self.categorical_cols[:]:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.date_cols.append(col)
                    self.categorical_cols.remove(col)
                except:
                    pass
        
        # Professional color palettes
        self.colors = {
            'primary': '#2E86DE',
            'secondary': '#10AC84',
            'accent': '#EE5A6F',
            'warning': '#F79F1F',
            'info': '#5F27CD',
            'success': '#00D2D3',
            'gradient': ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        }
        
        self.palettes = {
            'vibrant': ['#1e3799', '#0c2461', '#0a3d62', '#079992', '#78e08f', '#38ada9'],
            'sunset': ['#fc5c65', '#fd9644', '#fed330', '#26de81', '#2bcbba', '#45aaf2'],
            'ocean': ['#0652DD', '#1289A7', '#12CBC4', '#FDA7DF', '#ED4C67', '#B53471'],
            'forest': ['#006266', '#079992', '#38ada9', '#78e08f', '#b8e994', '#e58e26']
        }

    def perform_analysis(self):
        """Execute comprehensive data analysis"""
        print("[*] Starting in-depth data analysis...")
        print(f"[*] Dataset size: {len(self.df):,} rows, {len(self.df.columns)} columns")
        
        try:
            # 1. Basic Overview
            self.analysis_results['basic_stats'] = self._get_basic_stats()
            
            # 2. Numeric Analysis
            if self.numeric_cols:
                self.analysis_results['numeric_analysis'] = self._analyze_numeric_columns()
            
            # 3. Categorical Analysis
            if self.categorical_cols:
                self.analysis_results['categorical_analysis'] = self._analyze_categorical_columns()
            
            # 4. Time Series Analysis (if dates exist)
            if self.date_cols and self.numeric_cols:
                self.analysis_results['temporal_analysis'] = self._analyze_temporal_data()
            
            # 5. Correlation Analysis
            if len(self.numeric_cols) > 1:
                self.analysis_results['correlations'] = self._analyze_correlations()
            
            # 6. Generate Data-Driven Insights
            self.analysis_results['insights'] = self._generate_insights()
            
            print("[✓] Analysis completed successfully!")
            return self.analysis_results
        except Exception as e:
            print(f"[✗] Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def _get_basic_stats(self):
        """Calculate dataset overview statistics"""
        return {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'numeric_columns': len(self.numeric_cols),
            'categorical_columns': len(self.categorical_cols),
            'date_columns': len(self.date_cols),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
    
    def _analyze_numeric_columns(self):
        """Detailed analysis of numeric columns"""
        stats = {}
        for col in self.numeric_cols:
            col_data = self.df[col].dropna()
            stats[col] = {
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std(),
                'min': col_data.min(),
                'max': col_data.max(),
                'q1': col_data.quantile(0.25),
                'q3': col_data.quantile(0.75),
                'iqr': col_data.quantile(0.75) - col_data.quantile(0.25),
                'skewness': col_data.skew(),
                'kurtosis': col_data.kurtosis(),
                'zeros': (col_data == 0).sum(),
                'missing': self.df[col].isnull().sum()
            }
        return stats
    
    def _analyze_categorical_columns(self):
        """Detailed analysis of categorical columns"""
        stats = {}
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            stats[col] = {
                'unique_count': self.df[col].nunique(),
                'top_values': value_counts.head(10).to_dict(),
                'most_frequent': value_counts.index[0] if not value_counts.empty else None,
                'most_frequent_count': value_counts.values[0] if not value_counts.empty else 0,
                'concentration': (value_counts.values[0] / len(self.df) * 100) if not value_counts.empty else 0
            }
        return stats
    
    def _analyze_temporal_data(self):
        """Analyze trends over time using the first identified date column"""
        date_col = self.date_cols[0]
        temp_df = self.df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col])
        
        # Monthly aggregation
        monthly_data = temp_df.set_index(date_col)
        monthly_stats = monthly_data[self.numeric_cols].resample('M').agg(['sum', 'mean', 'count'])
        
        return {
            'date_column': date_col,
            'date_range': f"{temp_df[date_col].min().strftime('%Y-%m-%d')} to {temp_df[date_col].max().strftime('%Y-%m-%d')}",
            'duration_days': (temp_df[date_col].max() - temp_df[date_col].min()).days,
            'trends': monthly_stats.to_dict()
        }

    def _analyze_correlations(self):
        """Calculate correlation matrix"""
        corr_matrix = self.df[self.numeric_cols].corr()
        correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                val = corr_matrix.iloc[i, j]
                if abs(val) > 0.3:  # Lower threshold to capture more relationships
                    correlations.append({
                        'pair': f"{col1} vs {col2}",
                        'col1': col1,
                        'col2': col2,
                        'value': val,
                        'strength': 'Strong' if abs(val) > 0.7 else 'Moderate' if abs(val) > 0.5 else 'Weak',
                        'direction': 'Positive' if val > 0 else 'Negative'
                    })
        return sorted(correlations, key=lambda x: abs(x['value']), reverse=True)
    
    def _generate_insights(self):
        """Generate data-driven insights from the analysis"""
        insights = []
        
        # Numeric insights
        if 'numeric_analysis' in self.analysis_results:
            for col, stats in self.analysis_results['numeric_analysis'].items():
                # High variability insight
                if stats['std'] > stats['mean']:
                    insights.append(f"High variability detected in {col} (std: {stats['std']:.2f}, mean: {stats['mean']:.2f})")
                
                # Skewness insight
                if abs(stats['skewness']) > 1:
                    direction = "right" if stats['skewness'] > 0 else "left"
                    insights.append(f"{col} shows significant {direction}-skewed distribution (skewness: {stats['skewness']:.2f})")
        
        # Categorical insights
        if 'categorical_analysis' in self.analysis_results:
            for col, stats in self.analysis_results['categorical_analysis'].items():
                if stats['concentration'] > 50:
                    insights.append(f"{col} is highly concentrated: '{stats['most_frequent']}' represents {stats['concentration']:.1f}% of data")
                
                if stats['unique_count'] > len(self.df) * 0.9:
                    insights.append(f"{col} has very high cardinality ({stats['unique_count']} unique values)")
        
        # Correlation insights
        if 'correlations' in self.analysis_results:
            strong_corrs = [c for c in self.analysis_results['correlations'] if abs(c['value']) > 0.7]
            if strong_corrs:
                top_corr = strong_corrs[0]
                insights.append(f"Strong {top_corr['direction'].lower()} correlation found between {top_corr['col1']} and {top_corr['col2']} (r={top_corr['value']:.3f})")
        
        # Data quality insights
        basic = self.analysis_results.get('basic_stats', {})
        if basic.get('missing_values', 0) > 0:
            missing_pct = (basic['missing_values'] / (basic['total_records'] * basic['total_columns'])) * 100
            insights.append(f"Dataset contains {basic['missing_values']} missing values ({missing_pct:.2f}% of total data)")
        
        if basic.get('duplicate_rows', 0) > 0:
            dup_pct = (basic['duplicate_rows'] / basic['total_records']) * 100
            insights.append(f"Found {basic['duplicate_rows']} duplicate rows ({dup_pct:.2f}% of dataset)")
        
        return insights if insights else ["Data analysis completed successfully. All metrics are within normal ranges."]

    def generate_charts(self, output_dir='charts', chart_config=None):
        """Generate professional, accurate visualizations with vibrant styling"""
        os.makedirs(output_dir, exist_ok=True)
        print("[*] Generating professional visualizations...")
        
        # Default configuration if none provided
        if chart_config is None:
            chart_config = {
                'histograms': True,
                'pie_charts': True,
                'box_plots': True,
                'line_charts': True
            }
        
        # Enhanced matplotlib and seaborn settings
        sns.set_context("talk")
        sns.set_style("whitegrid", {
            'axes.facecolor': '#f8f9fa',
            'figure.facecolor': 'white',
            'grid.color': '#e0e0e0',
            'grid.linestyle': '--',
            'grid.linewidth': 0.7
        })
        
        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': '#f8f9fa',
            'axes.edgecolor': '#2c3e50',
            'axes.linewidth': 1.5,
            'axes.labelsize': 12,
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans']
        })
        
        chart_count = 0
        
        # 1. Histograms/Bar Graphs for Numeric Distributions (REDUCED from 5 to 3)
        if chart_config.get('histograms', True):
            for col in self.numeric_cols[:3]:  # Reduced from 5 to 3
                fig, ax = plt.subplots(figsize=(12, 6))
                
                data = self.df[col].dropna()
                
                # Create histogram with vibrant colors
                n, bins, patches = ax.hist(data, bins=30, edgecolor='white', linewidth=1.5, alpha=0.85)
                
                # Color gradient for bars
                cm = plt.cm.get_cmap('viridis')
                bin_centers = 0.5 * (bins[:-1] + bins[1:])
                col_normalized = (bin_centers - bin_centers.min()) / (bin_centers.max() - bin_centers.min())
                
                for c, p in zip(col_normalized, patches):
                    plt.setp(p, 'facecolor', cm(c))
                
                # Add KDE line
                from scipy import stats
                density = stats.gaussian_kde(data)
                xs = np.linspace(data.min(), data.max(), 200)
                density_values = density(xs)
                # Scale density to match histogram
                density_scaled = density_values * len(data) * (bins[1] - bins[0])
                ax.plot(xs, density_scaled, color=self.colors['accent'], linewidth=3, 
                       label='Density Curve', alpha=0.9)
                
                ax.set_xlabel(col, fontweight='bold', fontsize=12)
                ax.set_ylabel('Frequency', fontweight='bold', fontsize=12)
                ax.set_title(f'Distribution: {col}', fontweight='bold', fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')
                ax.legend(loc='best', fontsize=10)
                
                # Add statistics box
                stats_text = f"Mean: {data.mean():.2f}\nMedian: {data.median():.2f}\nStd: {data.std():.2f}\nMin: {data.min():.2f}\nMax: {data.max():.2f}"
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, pad=0.5))
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_histogram_{col}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 2. Stock Market-Style Line Charts for Numeric Variation (REDUCED from 5 to 3)
        if chart_config.get('line_charts', True):
            for col in self.numeric_cols[:3]:  # Reduced from 5 to 3
                fig, ax = plt.subplots(figsize=(14, 7))
                
                data = self.df[col].dropna()
                x_values = range(len(data))
                
                # Main line chart
                ax.plot(x_values, data.values, color=self.colors['primary'], linewidth=2, alpha=0.8, label=col)
                
                # Fill area under curve
                ax.fill_between(x_values, data.values, alpha=0.3, color=self.colors['primary'])
                
                # Add moving average (if enough data points)
                if len(data) > 20:
                    window = min(20, len(data) // 10)
                    moving_avg = data.rolling(window=window, center=True).mean()
                    ax.plot(x_values, moving_avg.values, color=self.colors['accent'], 
                           linewidth=2.5, linestyle='--', label=f'{window}-Period Moving Avg', alpha=0.9)
                
                # Add horizontal lines for mean and median
                mean_val = data.mean()
                median_val = data.median()
                ax.axhline(y=mean_val, color=self.colors['secondary'], linestyle='-.', 
                          linewidth=2, alpha=0.7, label=f'Mean: {mean_val:.2f}')
                ax.axhline(y=median_val, color=self.colors['warning'], linestyle=':', 
                          linewidth=2, alpha=0.7, label=f'Median: {median_val:.2f}')
                
                ax.set_xlabel('Record Index', fontweight='bold', fontsize=12)
                ax.set_ylabel(col, fontweight='bold', fontsize=12)
                ax.set_title(f'Variation Analysis: {col} (Stock Market Style)', fontweight='bold', fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.legend(loc='best', fontsize=10, framealpha=0.9)
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_line_variation_{col}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 3. Horizontal Bar Charts for Categorical Data (More readable)
        for col in self.categorical_cols[:5]:
            if self.df[col].nunique() <= 20:
                fig, ax = plt.subplots(figsize=(12, 7))
                
                top_cats = self.df[col].value_counts().head(10)
                colors_list = sns.color_palette(self.palettes['vibrant'], len(top_cats))
                
                bars = ax.barh(range(len(top_cats)), top_cats.values, color=colors_list,
                             edgecolor='#2c3e50', linewidth=1.5, alpha=0.85)
                
                ax.set_yticks(range(len(top_cats)))
                ax.set_yticklabels(top_cats.index, fontweight='bold')
                ax.set_xlabel('Count', fontweight='bold', fontsize=12)
                ax.set_title(f'Top 10 Categories: {col}', fontweight='bold', fontsize=14, pad=15)
                ax.grid(axis='x', alpha=0.3, linestyle='--')
                
                # Add value labels
                for i, (bar, value) in enumerate(zip(bars, top_cats.values)):
                    ax.text(value, i, f' {value:,}', va='center', fontweight='bold', fontsize=10)
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_bar_{col}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 4. Pie Charts for Top Categorical Distributions
        if chart_config.get('pie_charts', True):
            for col in self.categorical_cols[:3]:
                if 5 <= self.df[col].nunique() <= 10:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    
                    top_cats = self.df[col].value_counts().head(8)
                    colors_list = sns.color_palette(self.palettes['sunset'], len(top_cats))
                    
                    wedges, texts, autotexts = ax.pie(top_cats.values, labels=top_cats.index,
                                                       autopct='%1.1f%%', startangle=90,
                                                       colors=colors_list, explode=[0.05] * len(top_cats),
                                                       shadow=True, textprops={'fontweight': 'bold', 'fontsize': 10})
                    
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontsize(11)
                        autotext.set_fontweight('bold')
                    
                    ax.set_title(f'Distribution Breakdown: {col}', fontweight='bold', fontsize=14, pad=20)
                    
                    plt.tight_layout()
                    plt.savefig(f'{output_dir}/{chart_count:02d}_pie_{col}.png', dpi=150, bbox_inches='tight')
                    plt.close()
                    chart_count += 1
        
        # 5. Enhanced Correlation Heatmap
        if len(self.numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(12, 10))
            
            corr_matrix = self.df[self.numeric_cols].corr()
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
            
            sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
                       center=0, square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                       annot_kws={'fontsize': 9, 'fontweight': 'bold'},
                       vmin=-1, vmax=1, ax=ax)
            
            ax.set_title('Correlation Matrix Heatmap', fontweight='bold', fontsize=16, pad=20)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/{chart_count:02d}_correlation_heatmap.png', dpi=150, bbox_inches='tight')
            plt.close()
            chart_count += 1
        
        # 6. Line Graphs for Time Series (Temporal Data)
        if self.date_cols and self.numeric_cols:
            date_col = self.date_cols[0]
            
            for target_col in self.numeric_cols[:3]:
                fig, ax = plt.subplots(figsize=(14, 7))
                
                temp_df = self.df.sort_values(date_col).copy()
                temp_df[date_col] = pd.to_datetime(temp_df[date_col])
                
                # Aggregate by month for cleaner visualization
                monthly = temp_df.set_index(date_col)[target_col].resample('M').mean()
                
                ax.plot(monthly.index, monthly.values, color=self.colors['primary'],
                       linewidth=3, marker='o', markersize=6, markerfacecolor=self.colors['accent'],
                       markeredgecolor='white', markeredgewidth=2, alpha=0.9)
                
                ax.fill_between(monthly.index, monthly.values, alpha=0.3, color=self.colors['primary'])
                
                ax.set_xlabel('Time Period', fontweight='bold', fontsize=12)
                ax.set_ylabel(target_col, fontweight='bold', fontsize=12)
                ax.set_title(f'Trend Analysis: {target_col} Over Time', fontweight='bold', fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, linestyle='--')
                plt.xticks(rotation=45, ha='right')
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_line_trend_{target_col}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 6. Box Plots for Numeric Distributions (Shows outliers, REDUCED to 2)
        if chart_config.get('box_plots', True):
            for col in self.numeric_cols[:2]:  # Only 2 box plots
                fig, ax = plt.subplots(figsize=(10, 6))
                
                box_data = self.df[col].dropna()
                bp = ax.boxplot([box_data], vert=True, patch_artist=True, widths=0.5,
                               boxprops=dict(facecolor=self.colors['primary'], alpha=0.7, linewidth=2),
                               medianprops=dict(color='#c0392b', linewidth=3),
                               whiskerprops=dict(color=self.colors['primary'], linewidth=2),
                               capprops=dict(color=self.colors['primary'], linewidth=2),
                               flierprops=dict(marker='o', markerfacecolor=self.colors['accent'], 
                                             markersize=6, alpha=0.5))
                
                ax.set_ylabel(col, fontweight='bold', fontsize=12)
                ax.set_title(f'Distribution & Outliers: {col}', fontweight='bold', fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')
                
                # Add statistics
                stats_text = f"Mean: {box_data.mean():.2f}\nMedian: {box_data.median():.2f}\nStd: {box_data.std():.2f}\nQ1: {box_data.quantile(0.25):.2f}\nQ3: {box_data.quantile(0.75):.2f}"
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_boxplot_{col}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 7. Scatter Plots with Trend Lines (kept for correlations, using box_plots config)
        if chart_config.get('box_plots', True) and 'correlations' in self.analysis_results and self.analysis_results['correlations']:
            for corr in self.analysis_results['correlations'][:2]:  # Reduced to 2
                fig, ax = plt.subplots(figsize=(10, 7))
                
                col1, col2 = corr['col1'], corr['col2']
                
                # Scatter plot
                ax.scatter(self.df[col1], self.df[col2], alpha=0.6, s=60,
                          c=self.df[col2], cmap='viridis', edgecolors='white', linewidth=0.5)
                
                # Add trend line
                z = np.polyfit(self.df[col1].dropna(), self.df[col2].dropna(), 1)
                p = np.poly1d(z)
                ax.plot(self.df[col1], p(self.df[col1]), "r--", linewidth=2.5, alpha=0.8, label=f'Trend Line')
                
                ax.set_xlabel(col1, fontweight='bold', fontsize=12)
                ax.set_ylabel(col2, fontweight='bold', fontsize=12)
                ax.set_title(f'Correlation Analysis: {col1} vs {col2}\n({corr["strength"]} {corr["direction"]} - r={corr["value"]:.3f})',
                           fontweight='bold', fontsize=13, pad=15)
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.legend(loc='best', fontsize=10)
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{chart_count:02d}_scatter_{col1}_vs_{col2}.png', dpi=150, bbox_inches='tight')
                plt.close()
                chart_count += 1
        
        # 8. Multi-line chart for comparing numeric columns
        if len(self.numeric_cols) >= 2 and len(self.numeric_cols) <= 5:
            fig, ax = plt.subplots(figsize=(14, 7))
            
            # Normalize data for comparison
            df_normalized = self.df[self.numeric_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
            
            colors_multi = sns.color_palette(self.palettes['ocean'], len(self.numeric_cols))
            
            for i, col in enumerate(self.numeric_cols):
                ax.plot(df_normalized.index[:100], df_normalized[col][:100],
                       label=col, linewidth=2.5, color=colors_multi[i], alpha=0.8)
            
            ax.set_xlabel('Record Index', fontweight='bold', fontsize=12)
            ax.set_ylabel('Normalized Value', fontweight='bold', fontsize=12)
            ax.set_title('Multi-Variable Comparison (Normalized)', fontweight='bold', fontsize=14, pad=15)
            ax.legend(loc='best', fontsize=10, framealpha=0.9)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/{chart_count:02d}_multiline_comparison.png', dpi=150, bbox_inches='tight')
            plt.close()
            chart_count += 1

        print(f"[✓] Generated {chart_count} professional charts!")
        return output_dir
