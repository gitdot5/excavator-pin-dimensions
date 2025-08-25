Excavator Pin Dimensions Database
📊 Database Overview
This repository contains the most complete collection of excavator pin dimensions and
specifications available. The database includes detailed measurements for stick pins, link
pins, widths, and center distances for excavators from all major manufacturers.
📈 Database Statistics
Metric Count
Total Records 929
Manufacturers 54
Original PDF Models 564
New 2019-2024 Models 184
Additional Manufacturers 162
Electric Models 10
Specialty Models 9
🏭 Supported Manufacturers
Major Global Brands
LLiicceennssee MIITT
Daattaa VVeerrssiioonn 22002244..11
RReeccoorrddss 992299
Maannuuffaaccttuurreerrss 5544
The most comprehensive excavator pin dimensions database available
Complete specifications for 929+ excavator models from 54+ manufacturers worldwide
• Caterpillar (150+ models) - Complete lineup including Next Generation series
• Komatsu (50+ models) - PC series, WB series, latest Dash-11 models
• Volvo (85+ models) - EC series, ECR series, E-series
• JCB (45+ models) - JS series, JZ series, latest models
• Hitachi (65+ models) - Zaxis series, EX series, Zaxis-6
• Hyundai (45+ models) - R series, HX Z & A series
• Case (85+ models) - CX series, C-series
• John Deere (25+ models) - Complete G-series lineup
• Kubota (35+ models) - KX series, U series, KX-4 series
• Liebherr (25+ models) - R series, R900 series
Regional & Specialty Brands
• Chinese Manufacturers: Sany, XCMG, Zoomlion, LiuGong, Lonking, Sunward, Shantui,
Yuchai
• European Specialists: Mecalac, Schaeff, Eurocomach, Wacker Neuson, Atlas
• Japanese Brands: Takeuchi, Kobelco, Sumitomo, IHI, Airman, Yanmar, Hanix
• Other Brands: Bobcat, Link-Belt, Develon, New Holland, Terex, Gehl, and more
📋 Data Specifications
Each excavator record includes:
• Manufacturer - Equipment manufacturer name
• Model - Specific model designation
• Stick Pin Diameter - Metric (mm) and Imperial (inch)
• Stick Width - Metric (mm) and Imperial (inch)
• Link Pin Diameter - Metric (mm) and Imperial (inch)
• Link Width - Metric (mm) and Imperial (inch)
• Pin Centers - Distance between pin centers (mm/inch)
• Tip Radius - Bucket tip radius measurements
• Data Source - Original source of specifications
• Notes - Additional technical information
📁 File Formats
The database is available in multiple formats for maximum compatibility:
Format File Description
Excel excavator_database.xlsx Full-featured spreadsheet with formatting
CSV excavator_database.csv Universal format for data analysis
PDF excavator_database.pdf Professional printable reference (21 pages)
XML excavator_database.xml Structured data for API integration
🚀 Quick Start
Download Data
Bash
# Clone the repository
git clone https://github.com/gitdot5/excavator-pin-dimensions.git
# Navigate to data directory
cd excavator-pin-dimensions/data
Import into Excel/Google Sheets
1. Download excavator_database.csv
2. Open in Excel or Google Sheets
3. Use "Import" or "Open" function
4. Select CSV format with comma delimiter
Use with Python
Python
import pandas as pd
# Load the database
df = pd.read_csv('excavator_database.csv')
# Find specific manufacturer
caterpillar_models = df[df['Manufacturer'] == 'Caterpillar']
# Search by pin diameter
large_excavators = df[df['Stick_Pin_Diameter_mm'] >= 80]
# Filter by model year (2019-2024)
new_models = df[df['Data_Source'].str.contains('New_2024')]
🔍 Search Examples
Find Models by Pin Size
Python
# Mini excavators (< 50mm pin)
mini_excavators = df[df['Stick_Pin_Diameter_mm'] < 50]
# Medium excavators (50-80mm pin)
medium_excavators = df[(df['Stick_Pin_Diameter_mm'] >= 50) &
(df['Stick_Pin_Diameter_mm'] < 80)]
# Large excavators (80mm+ pin)
large_excavators = df[df['Stick_Pin_Diameter_mm'] >= 80]
Find by Manufacturer
Python
# Japanese manufacturers
japanese_brands = ['Komatsu', 'Hitachi', 'Kubota', 'Takeuchi', 'Kobelco']
japanese_models = df[df['Manufacturer'].isin(japanese_brands)]
# European manufacturers
european_brands = ['Volvo', 'Liebherr', 'JCB', 'Mecalac', 'Atlas']
european_models = df[df['Manufacturer'].isin(european_brands)]
📊 Data Sources
This comprehensive database combines data from multiple authoritative sources:
• Original Equipment Manufacturer (OEM) Specifications - Direct from manufacturer
documentation
• Industry Standard References - Professional pin dimension charts
• Technical Service Manuals - Official service documentation
• Parts Catalogs - Manufacturer parts and specifications
• Industry Research - 2019-2024 model updates and specifications
• Professional Databases - Scribd technical documents and industry references
🔄 Version History
Version 2024.1 (Current)
• 929 total records across 54 manufacturers
• Added 184 new 2019-2024 models from major manufacturers
• Included 162 additional models from regional and specialty brands
• Added 10 electric excavator models with latest technology
• Enhanced data validation and quality control
• Professional XML format with metadata and statistics
Data Quality
• ✅ Verified Specifications - Cross-referenced with multiple sources
• ✅ Standardized Format - Consistent units and naming conventions
• ✅ Regular Updates - Continuously updated with new models
• ✅ Error Checking - Automated validation of measurements
• ✅ Source Tracking - Full traceability of data origins
🛠️ Applications
This database is valuable for:
Construction Industry
• Parts Ordering - Ensure correct pin specifications
• Equipment Maintenance - Quick reference for service technicians
• Fleet Management - Standardize parts inventory
• Cost Estimation - Accurate parts and service planning
Software Development
• Equipment Management Systems - Integrate pin specifications
• Parts Catalog Applications - Build searchable databases
• Mobile Apps - Field reference tools for technicians
• API Development - Create web services for equipment data
Research & Analysis
• Market Analysis - Equipment specifications and trends
• Compatibility Studies - Cross-manufacturer part compatibility
• Industry Standards - Reference for specification development
• Academic Research - Construction equipment studies
📈 Future Enhancements
Planned improvements include:
• Real-time Updates - Automated manufacturer data feeds
• API Endpoints - RESTful API for programmatic access
• Mobile App - Dedicated mobile application
• 3D Models - Visual pin and attachment representations
• Compatibility Matrix - Cross-manufacturer part compatibility
• Historical Data - Track specification changes over time
🤝 Contributing
We welcome contributions to improve and expand this database:
How to Contribute
1. Fork this repository
2. Add new excavator models or corrections
3. Verify specifications with official sources
4. Submit a pull request with detailed information
Contribution Guidelines
• Provide official source for all specifications
• Use consistent formatting and units
• Include model year and configuration details
• Verify accuracy before submitting
Data Validation
All contributions are reviewed for:
• ✅ Accuracy - Verified against official sources
• ✅ Completeness - All required fields populated
• ✅ Consistency - Matches database format standards
• ✅ Uniqueness - No duplicate entries
📞 Support & Contact
Issues & Questions
• GitHub Issues - Report bugs or request features
• Discussions - Ask questions or share ideas
• Wiki - Additional documentation and guides
Professional Services
For commercial applications or custom data requirements:
• Data Licensing - Commercial use licensing
• Custom Databases - Specialized equipment databases
• API Development - Custom API endpoints
• Consulting Services - Equipment specification consulting
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
Usage Rights
• ✅ Commercial Use - Use in commercial applications
• ✅ Modification - Modify and adapt the data
• ✅ Distribution - Share and redistribute
• ✅ Private Use - Use for internal projects
Attribution
When using this database, please provide attribution:
Plain Text
Excavator Pin Dimensions Database
https://github.com/gitdot5/excavator-pin-dimensions
🌟 Acknowledgments
Special thanks to:
• Equipment Manufacturers - For providing official specifications
• Industry Professionals - For validation and feedback
• Open Source Community - For tools and frameworks
• Construction Industry - For supporting open data initiatives
⭐ Star this repository if you find it useful!
🔗 Share with colleagues in the construction and equipment industry
📢 Follow for updates on new excavator models and specifications
This database represents the most comprehensive collection of excavator pin dimensions
available. It serves the global construction industry by providing accurate, accessible, and
standardized equipment specifications.
