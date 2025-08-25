# Thai Truck Weigh Station Data Analyzer & Dashboard

A comprehensive analysis and visualization system for Thai truck weigh station log data, updated with real operational data from July 2568 (Thai Buddhist calendar).

## 📊 System Overview

This system provides:
- **Real-time data analysis** of truck weigh station operations
- **Interactive dashboard** with business intelligence insights
- **Fleet optimization recommendations** based on performance metrics
- **Capacity utilization analysis** for operational efficiency
- **Pricing strategy insights** for revenue optimization

## 🗂️ Files Structure

```
website_automation/
├── 📂 html_dashboards/              # All HTML dashboard files
│   ├── index.html                   # Navigation hub
│   ├── thai_truck_dashboard.html    # Main truck analysis dashboard
│   ├── recycled_items_dashboard.html # Recycled items sales dashboard
│   └── [debug & test files]         # Testing and debugging tools
├── 📂 python_analyzers/             # All Python scripts & data
│   ├── simple_thai_analyzer.py      # Main analysis engine
│   ├── dashboard_data.json          # Generated dashboard data
│   ├── thai_truck_weigh_logs_real_2568.xlsx  # Real operational data
│   ├── thai_truck_weigh_analysis_simple.xlsx # Analysis results
│   └── [other analysis files]       # Additional scripts
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
python3 simple_thai_analyzer.py
```

### 3. View Dashboard
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000/html_dashboards/` in your browser to access the navigation hub.

## 📈 Real Data Analysis Results

### Key Metrics (July 2568)
- **Total Records**: 339 operations
- **Unique Trucks**: 8 vehicles
- **Date Range**: July 1-31, 2568
- **Total Revenue**: 59,030 THB
- **Average Daily Operations**: 10.9

### Top Performers
- **Highest Revenue**: 82-4347 (28,755 THB)
- **Most Operations**: 82-7890 (52 operations)
- **Highest Weight**: 82-7890 (771 kg total)

### Capacity Utilization
- **Average Weight**: 14.6 tons
- **Capacity Utilization**: 97.6%
- **Max Capacity Hits**: 142 operations
- **Underutilized Operations**: 20

### Operational Insights
- **24/7 Operations**: Full day coverage
- **Peak Hours**: 00:00 (19 operations)
- **Low Activity**: 15:00 (9 operations) - Maintenance window opportunity
- **Average Processing Time**: 9.7 minutes per truck

## 🎯 Business Intelligence Features

### Fleet Performance Analysis
- Performance tier classification (Elite/High/Good/Needs Attention)
- Revenue per truck analysis
- Route optimization recommendations
- Capacity utilization tracking

### Pricing Strategy Analysis
- Price variation analysis (15.5% variation)
- Revenue by price tier breakdown
- High-value operation identification
- Pricing optimization recommendations

### Operational Efficiency
- 24/7 operations pattern analysis
- Processing time optimization
- Peak hours identification
- Maintenance window recommendations

### Waste Management Insights
- Redemption rate analysis (100% efficiency)
- Weight vs. value correlation
- Waste type analysis
- Quality optimization recommendations

## 📊 Dashboard Features

### Interactive Charts
- **Fleet Performance Overview**: Top performers and performance tiers
- **Capacity Utilization**: Weight distribution and optimization opportunities
- **Hourly Operations**: 24/7 pattern visualization
- **Revenue Analysis**: Pricing strategy and revenue optimization
- **Truck Details**: Individual truck performance metrics

### Business Intelligence Sections
- **Client Pricing Strategy**: Client segmentation and pricing analysis
- **Operational Efficiency**: Time patterns and processing optimization
- **Waste Management**: Quality and redemption rate analysis
- **Strategic BI**: Portfolio analysis and ROI insights

## 🔧 Technical Details

### Data Structure (13 Columns A-M)
- **Column A**: Date (วนดอปไปช) - Thai Buddhist calendar
- **Column B**: Log Number (เลขที่บันทึก)
- **Column C**: License Plate (เลขทะเบียนรถ)
- **Column D**: Time In (เวลาเข้า)
- **Column E**: Time Out (เวลาออก)
- **Column F**: Total Weight (น้ำหนักรวมรถ)
- **Column G**: Max Redemption Weight (น้ำหนักสูงสุดที่ไถ่ได้)
- **Column H**: Empty Truck Weight (น้ำหนักรถเปล่า)
- **Column I**: Full Garbage Weight (น้ำหนักขยะเต็ม)
- **Column J**: Redeemable Weight (น้ำหนักขยะที่ไถ่ได้)
- **Column K**: Price Per Ton (ราคาไถ่ต่อตัน)
- **Column L**: Additional Data (ข้อมูลเพิ่มเติม) - Client and waste type info
- **Column M**: Log Count (จำนวนรายการ)

### Analysis Capabilities
- **Real-time data processing** from Excel files
- **Thai Buddhist calendar support** (2568 format)
- **Multi-language column detection** (Thai/English)
- **Comprehensive statistical analysis**
- **JSON export for dashboard integration**

## 💡 Key Insights from Real Data

### Fleet Optimization Opportunities
1. **Replicate 82-4347's model**: Highest revenue per operation (669 THB/op)
2. **Optimize 82-7890's route**: Most operations (52) with high efficiency
3. **Focus on underutilized operations**: 20 operations below 12 tons capacity

### Revenue Optimization
1. **Standardize pricing**: Current 15.5% variation suggests optimization opportunity
2. **Focus on high-value operations**: Above 1,500 THB/ton
3. **Analyze low-price operations**: Below 1,200 THB/ton for improvement

### Operational Improvements
1. **Night shift optimization**: 00:00-06:00 has consistent but lower volume
2. **Maintenance scheduling**: 15:00 window (9 operations) ideal for maintenance
3. **Processing time**: 9.7 minutes average with 5-15 minute range

## 🛠️ Customization

### Adding New Data
1. Place new Excel file in the project directory
2. Update the file path in `simple_thai_analyzer.py`
3. Run the analyzer to generate updated dashboard data

### Modifying Analysis
- Edit analysis functions in `simple_thai_analyzer.py`
- Add new metrics to the dashboard data export
- Update dashboard HTML for new visualizations

### Extending Dashboard
- Add new chart sections to `thai_truck_dashboard.html`
- Implement new JavaScript functions for data visualization
- Customize CSS styling for different themes

## 📋 Requirements

- Python 3.7+
- pandas
- numpy
- openpyxl
- Modern web browser (for dashboard)

## 🔄 Update Process

To update with new data:
1. Replace `thai_truck_weigh_logs_real_2568.xlsx` with new data
2. Run `python3 simple_thai_analyzer.py`
3. Refresh dashboard in browser

## 📞 Support

For questions or issues:
1. Check the console output for error messages
2. Verify Excel file format matches expected structure
3. Ensure all dependencies are installed
4. Check browser console for dashboard errors

---

**Last Updated**: August 25, 2025  
**Data Period**: July 2568 (Thai Buddhist Calendar)  
**Total Operations Analyzed**: 339 records  
**Fleet Size**: 8 trucks
