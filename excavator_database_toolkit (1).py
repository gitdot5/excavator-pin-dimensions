#!/usr/bin/env python3
"""
Excavator Pin Dimensions Database Toolkit
Complete Python solution for managing excavator pin specifications

Features:
- Data loading and processing
- Multiple export formats (CSV, Excel, PDF, XML, JSON)
- Data analysis and statistics
- Search and filtering capabilities
- Data validation and quality checks
- GitHub repository management
- API endpoints (Flask)
- Visualization and reporting

Author: Excavator Database Project
License: MIT
"""

import pandas as pd
import numpy as np
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sqlite3
from pathlib import Path
import datetime
import logging
from typing import Dict, List, Optional, Union, Any
import argparse
import sys
import os

# Optional imports for advanced features
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class ExcavatorDatabase:
    """
    Main class for managing excavator pin dimensions database
    """
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize the excavator database
        
        Args:
            data_file: Path to the main database file (CSV or Excel)
        """
        self.data_file = data_file
        self.df = None
        self.logger = self._setup_logging()
        
        # Database schema
        self.required_columns = [
            'Manufacturer', 'Model', 'Stick_Pin_Diameter_mm', 'Stick_Pin_Diameter_inch',
            'Stick_Width_mm', 'Stick_Width_inch', 'Link_Pin_Diameter_mm', 'Link_Pin_Diameter_inch',
            'Link_Width_mm', 'Link_Width_inch', 'Pin_Centers_mm', 'Pin_Centers_inch',
            'Data_Source', 'Notes'
        ]
        
        # Load data if file provided
        if data_file and Path(data_file).exists():
            self.load_data(data_file)
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('excavator_database.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def load_data(self, file_path: str) -> bool:
        """
        Load excavator data from file
        
        Args:
            file_path: Path to data file (CSV or Excel)
            
        Returns:
            bool: Success status
        """
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.csv':
                self.df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            self.logger.info(f"Loaded {len(self.df)} records from {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return False
    
    def validate_data(self) -> Dict[str, Any]:
        """
        Validate database integrity and quality
        
        Returns:
            dict: Validation results
        """
        if self.df is None:
            return {"error": "No data loaded"}
        
        results = {
            "total_records": len(self.df),
            "missing_columns": [],
            "missing_values": {},
            "duplicate_records": 0,
            "data_quality_score": 0,
            "issues": []
        }
        
        # Check required columns
        for col in self.required_columns:
            if col not in self.df.columns:
                results["missing_columns"].append(col)
        
        # Check missing values
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                results["missing_values"][col] = missing_count
        
        # Check duplicates
        duplicates = self.df.duplicated(subset=['Manufacturer', 'Model']).sum()
        results["duplicate_records"] = duplicates
        
        # Calculate quality score
        total_cells = len(self.df) * len(self.df.columns)
        missing_cells = sum(results["missing_values"].values())
        results["data_quality_score"] = round((1 - missing_cells / total_cells) * 100, 2)
        
        # Identify issues
        if results["missing_columns"]:
            results["issues"].append(f"Missing required columns: {results['missing_columns']}")
        if duplicates > 0:
            results["issues"].append(f"Found {duplicates} duplicate records")
        if results["data_quality_score"] < 90:
            results["issues"].append(f"Data quality score below 90%: {results['data_quality_score']}%")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive database statistics
        
        Returns:
            dict: Database statistics
        """
        if self.df is None:
            return {"error": "No data loaded"}
        
        stats = {
            "overview": {
                "total_records": len(self.df),
                "total_manufacturers": self.df['Manufacturer'].nunique(),
                "date_generated": datetime.datetime.now().isoformat()
            },
            "manufacturers": {},
            "pin_diameter_distribution": {},
            "data_sources": {},
            "weight_classes": {}
        }
        
        # Manufacturer statistics
        manufacturer_counts = self.df['Manufacturer'].value_counts()
        stats["manufacturers"] = manufacturer_counts.to_dict()
        
        # Pin diameter distribution
        if 'Stick_Pin_Diameter_mm' in self.df.columns:
            pin_diameters = self.df['Stick_Pin_Diameter_mm'].dropna()
            stats["pin_diameter_distribution"] = {
                "min": float(pin_diameters.min()),
                "max": float(pin_diameters.max()),
                "mean": float(pin_diameters.mean()),
                "median": float(pin_diameters.median())
            }
        
        # Data sources
        if 'Data_Source' in self.df.columns:
            source_counts = self.df['Data_Source'].value_counts()
            stats["data_sources"] = source_counts.to_dict()
        
        # Weight classes based on pin diameter
        if 'Stick_Pin_Diameter_mm' in self.df.columns:
            weight_classes = self._classify_by_weight()
            stats["weight_classes"] = weight_classes
        
        return stats
    
    def _classify_by_weight(self) -> Dict[str, int]:
        """Classify excavators by weight class based on pin diameter"""
        if 'Stick_Pin_Diameter_mm' not in self.df.columns:
            return {}
        
        pin_diameters = self.df['Stick_Pin_Diameter_mm'].dropna()
        
        classes = {
            "Mini (< 6 tons)": (pin_diameters <= 30).sum(),
            "Compact (6-15 tons)": ((pin_diameters > 30) & (pin_diameters <= 45)).sum(),
            "Medium (15-30 tons)": ((pin_diameters > 45) & (pin_diameters <= 65)).sum(),
            "Large (30-50 tons)": ((pin_diameters > 65) & (pin_diameters <= 90)).sum(),
            "Heavy (50-80 tons)": ((pin_diameters > 90) & (pin_diameters <= 120)).sum(),
            "Ultra Heavy (> 80 tons)": (pin_diameters > 120).sum()
        }
        
        return {k: int(v) for k, v in classes.items()}
    
    def search(self, **kwargs) -> pd.DataFrame:
        """
        Search excavators by various criteria
        
        Args:
            manufacturer: Manufacturer name
            model: Model name (partial match)
            pin_diameter_min: Minimum pin diameter (mm)
            pin_diameter_max: Maximum pin diameter (mm)
            data_source: Data source filter
            
        Returns:
            pd.DataFrame: Filtered results
        """
        if self.df is None:
            return pd.DataFrame()
        
        result = self.df.copy()
        
        # Filter by manufacturer
        if 'manufacturer' in kwargs and kwargs['manufacturer']:
            result = result[result['Manufacturer'].str.contains(kwargs['manufacturer'], case=False, na=False)]
        
        # Filter by model
        if 'model' in kwargs and kwargs['model']:
            result = result[result['Model'].str.contains(kwargs['model'], case=False, na=False)]
        
        # Filter by pin diameter range
        if 'pin_diameter_min' in kwargs and kwargs['pin_diameter_min']:
            result = result[result['Stick_Pin_Diameter_mm'] >= kwargs['pin_diameter_min']]
        
        if 'pin_diameter_max' in kwargs and kwargs['pin_diameter_max']:
            result = result[result['Stick_Pin_Diameter_mm'] <= kwargs['pin_diameter_max']]
        
        # Filter by data source
        if 'data_source' in kwargs and kwargs['data_source']:
            result = result[result['Data_Source'].str.contains(kwargs['data_source'], case=False, na=False)]
        
        return result
    
    def export_csv(self, output_path: str) -> bool:
        """Export database to CSV format"""
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            self.df.to_csv(output_path, index=False)
            self.logger.info(f"Exported {len(self.df)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting CSV: {e}")
            return False
    
    def export_excel(self, output_path: str) -> bool:
        """Export database to Excel format with formatting"""
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Main data sheet
                self.df.to_excel(writer, sheet_name='Excavator Database', index=False)
                
                # Statistics sheet
                stats = self.get_statistics()
                stats_df = pd.DataFrame([
                    ['Total Records', stats['overview']['total_records']],
                    ['Total Manufacturers', stats['overview']['total_manufacturers']],
                    ['Date Generated', stats['overview']['date_generated']]
                ], columns=['Metric', 'Value'])
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
                # Manufacturers sheet
                mfg_df = pd.DataFrame(list(stats['manufacturers'].items()), 
                                    columns=['Manufacturer', 'Model Count'])
                mfg_df.to_excel(writer, sheet_name='Manufacturers', index=False)
            
            self.logger.info(f"Exported {len(self.df)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting Excel: {e}")
            return False
    
    def export_json(self, output_path: str) -> bool:
        """Export database to JSON format"""
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            # Convert DataFrame to JSON with metadata
            data = {
                "metadata": {
                    "total_records": len(self.df),
                    "total_manufacturers": self.df['Manufacturer'].nunique(),
                    "export_date": datetime.datetime.now().isoformat(),
                    "version": "2024.1"
                },
                "excavators": self.df.to_dict('records')
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(self.df)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting JSON: {e}")
            return False
    
    def export_xml(self, output_path: str) -> bool:
        """Export database to XML format"""
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            # Create root element
            root = ET.Element("ExcavatorDatabase")
            
            # Add metadata
            metadata = ET.SubElement(root, "Metadata")
            ET.SubElement(metadata, "TotalRecords").text = str(len(self.df))
            ET.SubElement(metadata, "TotalManufacturers").text = str(self.df['Manufacturer'].nunique())
            ET.SubElement(metadata, "ExportDate").text = datetime.datetime.now().isoformat()
            ET.SubElement(metadata, "Version").text = "2024.1"
            
            # Add excavators
            excavators = ET.SubElement(root, "Excavators")
            
            for _, row in self.df.iterrows():
                excavator = ET.SubElement(excavators, "Excavator")
                
                for col in self.df.columns:
                    element = ET.SubElement(excavator, col.replace(' ', '_'))
                    element.text = str(row[col]) if pd.notna(row[col]) else ""
            
            # Create pretty XML
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            xml_lines = [line for line in xml_str.split('\n') if line.strip()]
            xml_str = '\n'.join(xml_lines)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            self.logger.info(f"Exported {len(self.df)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting XML: {e}")
            return False
    
    def export_pdf(self, output_path: str) -> bool:
        """Export database to PDF format"""
        if not REPORTLAB_AVAILABLE:
            self.logger.error("ReportLab not available. Install with: pip install reportlab")
            return False
        
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            doc = SimpleDocTemplate(output_path, pagesize=landscape(A4))
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("Excavator Pin Dimensions Database", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Statistics
            stats = self.get_statistics()
            stats_data = [
                ["Total Records", str(stats['overview']['total_records'])],
                ["Total Manufacturers", str(stats['overview']['total_manufacturers'])],
                ["Export Date", stats['overview']['date_generated'][:10]]
            ]
            
            stats_table = Table(stats_data)
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 30))
            
            # Main data table (first 100 records)
            df_sample = self.df.head(100)
            
            # Prepare table data
            table_data = [['Manufacturer', 'Model', 'Pin Ø (mm)', 'Pin Ø (in)', 'Stick W (mm)', 'Link W (mm)']]
            
            for _, row in df_sample.iterrows():
                table_data.append([
                    str(row['Manufacturer'])[:15],
                    str(row['Model'])[:15],
                    str(row['Stick_Pin_Diameter_mm']) if pd.notna(row['Stick_Pin_Diameter_mm']) else '-',
                    str(row['Stick_Pin_Diameter_inch']) if pd.notna(row['Stick_Pin_Diameter_inch']) else '-',
                    str(row['Stick_Width_mm']) if pd.notna(row['Stick_Width_mm']) else '-',
                    str(row['Link_Width_mm']) if pd.notna(row['Link_Width_mm']) else '-'
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            story.append(table)
            doc.build(story)
            
            self.logger.info(f"Exported PDF with {len(df_sample)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting PDF: {e}")
            return False
    
    def create_sqlite_database(self, db_path: str) -> bool:
        """Create SQLite database from the data"""
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            conn = sqlite3.connect(db_path)
            
            # Create main table
            self.df.to_sql('excavators', conn, if_exists='replace', index=False)
            
            # Create indexes for better performance
            cursor = conn.cursor()
            cursor.execute('CREATE INDEX idx_manufacturer ON excavators(Manufacturer)')
            cursor.execute('CREATE INDEX idx_model ON excavators(Model)')
            cursor.execute('CREATE INDEX idx_pin_diameter ON excavators(Stick_Pin_Diameter_mm)')
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Created SQLite database with {len(self.df)} records at {db_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating SQLite database: {e}")
            return False
    
    def generate_visualizations(self, output_dir: str) -> bool:
        """Generate visualization charts"""
        if not MATPLOTLIB_AVAILABLE:
            self.logger.error("Matplotlib not available. Install with: pip install matplotlib seaborn")
            return False
        
        try:
            if self.df is None:
                raise ValueError("No data loaded")
            
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
            
            # Set style
            plt.style.use('default')
            sns.set_palette("husl")
            
            # 1. Manufacturer distribution
            plt.figure(figsize=(12, 8))
            manufacturer_counts = self.df['Manufacturer'].value_counts().head(15)
            manufacturer_counts.plot(kind='bar')
            plt.title('Top 15 Manufacturers by Model Count')
            plt.xlabel('Manufacturer')
            plt.ylabel('Number of Models')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(output_dir / 'manufacturer_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. Pin diameter distribution
            if 'Stick_Pin_Diameter_mm' in self.df.columns:
                plt.figure(figsize=(10, 6))
                pin_diameters = self.df['Stick_Pin_Diameter_mm'].dropna()
                plt.hist(pin_diameters, bins=30, alpha=0.7, edgecolor='black')
                plt.title('Pin Diameter Distribution')
                plt.xlabel('Pin Diameter (mm)')
                plt.ylabel('Frequency')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(output_dir / 'pin_diameter_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            # 3. Weight class distribution
            weight_classes = self._classify_by_weight()
            if weight_classes:
                plt.figure(figsize=(10, 8))
                classes = list(weight_classes.keys())
                counts = list(weight_classes.values())
                
                plt.pie(counts, labels=classes, autopct='%1.1f%%', startangle=90)
                plt.title('Excavator Weight Class Distribution')
                plt.axis('equal')
                plt.tight_layout()
                plt.savefig(output_dir / 'weight_class_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            self.logger.info(f"Generated visualizations in {output_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {e}")
            return False

class ExcavatorAPI:
    """
    Flask API for excavator database
    """
    
    def __init__(self, database: ExcavatorDatabase):
        if not FLASK_AVAILABLE:
            raise ImportError("Flask not available. Install with: pip install flask flask-cors")
        
        self.database = database
        self.app = Flask(__name__)
        CORS(self.app)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/excavators', methods=['GET'])
        def get_excavators():
            """Get all excavators with optional filtering"""
            try:
                # Get query parameters
                manufacturer = request.args.get('manufacturer')
                model = request.args.get('model')
                pin_diameter_min = request.args.get('pin_diameter_min', type=float)
                pin_diameter_max = request.args.get('pin_diameter_max', type=float)
                limit = request.args.get('limit', default=100, type=int)
                
                # Search with filters
                results = self.database.search(
                    manufacturer=manufacturer,
                    model=model,
                    pin_diameter_min=pin_diameter_min,
                    pin_diameter_max=pin_diameter_max
                )
                
                # Limit results
                results = results.head(limit)
                
                return jsonify({
                    'success': True,
                    'count': len(results),
                    'data': results.to_dict('records')
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/manufacturers', methods=['GET'])
        def get_manufacturers():
            """Get list of all manufacturers"""
            try:
                if self.database.df is None:
                    return jsonify({'success': False, 'error': 'No data loaded'}), 400
                
                manufacturers = self.database.df['Manufacturer'].unique().tolist()
                manufacturers.sort()
                
                return jsonify({
                    'success': True,
                    'count': len(manufacturers),
                    'data': manufacturers
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/statistics', methods=['GET'])
        def get_statistics():
            """Get database statistics"""
            try:
                stats = self.database.get_statistics()
                return jsonify({
                    'success': True,
                    'data': stats
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/search', methods=['POST'])
        def search_excavators():
            """Advanced search with POST data"""
            try:
                search_params = request.get_json()
                results = self.database.search(**search_params)
                
                return jsonify({
                    'success': True,
                    'count': len(results),
                    'data': results.to_dict('records')
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the API server"""
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Excavator Pin Dimensions Database Toolkit')
    parser.add_argument('--data', '-d', help='Path to data file (CSV or Excel)')
    parser.add_argument('--output', '-o', help='Output directory', default='./output')
    parser.add_argument('--format', '-f', choices=['csv', 'excel', 'json', 'xml', 'pdf', 'sqlite', 'all'], 
                       default='csv', help='Export format')
    parser.add_argument('--search', '-s', help='Search term')
    parser.add_argument('--manufacturer', '-m', help='Filter by manufacturer')
    parser.add_argument('--validate', action='store_true', help='Validate data quality')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    parser.add_argument('--api', action='store_true', help='Start API server')
    parser.add_argument('--port', type=int, default=5000, help='API server port')
    
    args = parser.parse_args()
    
    # Initialize database
    db = ExcavatorDatabase(args.data)
    
    if db.df is None:
        print("Error: No data loaded. Please provide a valid data file with --data")
        return 1
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Validate data
    if args.validate:
        print("Validating data...")
        validation = db.validate_data()
        print(json.dumps(validation, indent=2))
    
    # Show statistics
    if args.stats:
        print("Database Statistics:")
        stats = db.get_statistics()
        print(json.dumps(stats, indent=2))
    
    # Search functionality
    if args.search or args.manufacturer:
        print("Searching database...")
        results = db.search(
            manufacturer=args.manufacturer,
            model=args.search
        )
        print(f"Found {len(results)} results")
        if len(results) > 0:
            print(results[['Manufacturer', 'Model', 'Stick_Pin_Diameter_mm']].head(10))
    
    # Export data
    if args.format in ['csv', 'all']:
        print("Exporting to CSV...")
        db.export_csv(output_dir / 'excavator_database.csv')
    
    if args.format in ['excel', 'all']:
        print("Exporting to Excel...")
        db.export_excel(output_dir / 'excavator_database.xlsx')
    
    if args.format in ['json', 'all']:
        print("Exporting to JSON...")
        db.export_json(output_dir / 'excavator_database.json')
    
    if args.format in ['xml', 'all']:
        print("Exporting to XML...")
        db.export_xml(output_dir / 'excavator_database.xml')
    
    if args.format in ['pdf', 'all']:
        print("Exporting to PDF...")
        db.export_pdf(output_dir / 'excavator_database.pdf')
    
    if args.format in ['sqlite', 'all']:
        print("Creating SQLite database...")
        db.create_sqlite_database(output_dir / 'excavator_database.db')
    
    # Generate visualizations
    if args.visualize:
        print("Generating visualizations...")
        db.generate_visualizations(output_dir / 'charts')
    
    # Start API server
    if args.api:
        print(f"Starting API server on port {args.port}...")
        api = ExcavatorAPI(db)
        api.run(port=args.port)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

