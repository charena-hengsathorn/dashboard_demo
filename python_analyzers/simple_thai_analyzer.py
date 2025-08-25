#!/usr/bin/env python3
"""
Simple Thai Truck Weigh Station Log Data Analyzer
Comprehensive analysis without visualization dependencies.
Updated for correct column structure A-M with Thai Buddhist calendar year 2568.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SimpleThaiTruckAnalyzer:
    """Simple analyzer class for Thai truck weigh station log data without matplotlib."""
    
    def __init__(self, file_path=None, df=None):
        """Initialize with either file path or DataFrame."""
        if df is not None:
            self.df = df
        elif file_path:
            self.df = self.load_data(file_path)
        else:
            raise ValueError("Either file_path or df must be provided")
        
        self.setup_data()
    
    def load_data(self, file_path):
        """Load data from Excel file."""
        try:
            # Try to read the file
            df = pd.read_excel(file_path)
            print(f"Data loaded successfully from {file_path}")
            print(f"Columns detected: {len(df.columns)} (A-{chr(65 + len(df.columns) - 1)})")
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    
    def setup_data(self):
        """Setup and clean the data."""
        # Detect Thai columns for the 13-column structure (A-M) - Truck Weigh Station
        self.thai_columns = {
            'date': [col for col in self.df.columns if 'วนดอปไปช' in str(col) or 'Date' in str(col)][0],
            'log_number': [col for col in self.df.columns if 'เลขที่บันทึก' in str(col) or 'Log_Number' in str(col)][0],
            'license_plate': [col for col in self.df.columns if 'เลขทะเบียนรถ' in str(col) or 'License_Plate' in str(col)][0],
            'time_in': [col for col in self.df.columns if 'เวลาเข้า' in str(col) or 'Time_In' in str(col)][0],
            'time_out': [col for col in self.df.columns if 'เวลาออก' in str(col) or 'Time_Out' in str(col)][0],
            'total_weight': [col for col in self.df.columns if 'น้ำหนักรวมรถ' in str(col) or 'Total_Weight' in str(col)][0],
            'max_redemption': [col for col in self.df.columns if 'น้ำหนักสูงสุดที่ไถ่ได้' in str(col) or 'Max_Redemption_Weight' in str(col)][0],
            'empty_weight': [col for col in self.df.columns if 'น้ำหนักรถเปล่า' in str(col) or 'Empty_Truck_Weight' in str(col)][0],
            'garbage_weight': [col for col in self.df.columns if 'น้ำหนักขยะเต็ม' in str(col) or 'Full_Garbage_Weight' in str(col)][0],
            'redeemable_weight': [col for col in self.df.columns if 'น้ำหนักขยะที่ไถ่ได้' in str(col) or 'Redeemable_Weight' in str(col)][0],
            'price_per_ton': [col for col in self.df.columns if 'ราคาไถ่ต่อตัน' in str(col) or 'Price_Per_Ton' in str(col)][0],
            'additional_data': [col for col in self.df.columns if 'ข้อมูลเพิ่มเติม' in str(col) or 'Additional_Data' in str(col)][0],
            'log_count': [col for col in self.df.columns if 'จำนวนรายการ' in str(col) or 'Log_Count' in str(col)][0]
        }
        
        # Remove total rows and clean data
        self.df_clean = self.df[self.df[self.thai_columns['log_number']] != 'รวม'].copy()
        
        # Convert date column (handle both 2568 and 2025 formats)
        date_col = self.thai_columns['date']
        try:
            # Try Thai Buddhist calendar format first (2568)
            self.df_clean[date_col] = pd.to_datetime(
                self.df_clean[date_col], 
                format='%d %b %y', 
                errors='coerce'
            )
            # If dates are in 2025, convert to 2568 for display
            if self.df_clean[date_col].dt.year.iloc[0] == 2025:
                print("Converting Western calendar dates to Thai Buddhist calendar (2568)")
                self.df_clean[date_col] = self.df_clean[date_col].dt.year + 543
        except:
            print("Date conversion failed, keeping original format")
        
        # Convert numeric columns
        numeric_cols = [
            self.thai_columns['total_weight'],
            self.thai_columns['max_redemption'],
            self.thai_columns['empty_weight'],
            self.thai_columns['garbage_weight'],
            self.thai_columns['redeemable_weight'],
            self.thai_columns['price_per_ton'],
            self.thai_columns['log_count']
        ]
        
        # Extract redemption value from Column L (ข้อมูลเพิ่มเติม) which contains "CLIENT-X - WASTE_TYPE - VALUE THB"
        if self.thai_columns['additional_data'] in self.df_clean.columns:
            # Extract the numeric value from the end of the additional_data string
            extracted_values = self.df_clean[self.thai_columns['additional_data']].str.extract(r'(\d+(?:,\d+)*\.?\d*)\s*THB')
            # Replace commas in numbers like "23,738.68" and convert to float
            self.df_clean['redemption_value'] = extracted_values[0].str.replace(',', '').astype(float)
        
        for col in numeric_cols:
            if col in self.df_clean.columns:
                self.df_clean[col] = pd.to_numeric(self.df_clean[col], errors='coerce')
        
        print(f"Data cleaned: {len(self.df_clean)} records")
        print(f"Column structure: A-M ({len(self.thai_columns)} columns)")
    
    def basic_statistics(self):
        """Display basic statistics about the data."""
        print("=" * 60)
        print("BASIC STATISTICS")
        print("=" * 60)
        
        print(f"Total Records: {len(self.df_clean)}")
        print(f"Date Range: {self.df_clean[self.thai_columns['date']].min()} to {self.df_clean[self.thai_columns['date']].max()}")
        print(f"Unique Trucks: {self.df_clean[self.thai_columns['license_plate']].nunique()}")
        print(f"License Plates: {', '.join(self.df_clean[self.thai_columns['license_plate']].unique()[:10])}...")
        
        print(f"\nWeight Statistics:")
        print(f"  Average Total Weight: {self.df_clean[self.thai_columns['total_weight']].mean():.2f} kg")
        print(f"  Average Garbage Weight: {self.df_clean[self.thai_columns['garbage_weight']].mean():.2f} kg")
        print(f"  Average Redeemable Weight: {self.df_clean[self.thai_columns['redeemable_weight']].mean():.2f} kg")
        
        print(f"\nRedemption Statistics:")
        if 'redemption_value' in self.df_clean.columns:
            total_value = self.df_clean['redemption_value'].sum()
            avg_value = self.df_clean['redemption_value'].mean()
            print(f"  Total Redemption Value (Column L): {total_value:,.2f} THB")
            print(f"  Average Redemption per Record: {avg_value:,.2f} THB")
        else:
            # Fallback calculation if Column L parsing failed
            total_value = (self.df_clean[self.thai_columns['redeemable_weight']] * self.df_clean[self.thai_columns['price_per_ton']] / 1000).sum()
            avg_value = (self.df_clean[self.thai_columns['redeemable_weight']] * self.df_clean[self.thai_columns['price_per_ton']] / 1000).mean()
            print(f"  Total Redemption Value (Calculated): {total_value:,.2f} THB")
            print(f"  Average Redemption per Record: {avg_value:,.2f} THB")
        print(f"  Average Price per Ton: {self.df_clean[self.thai_columns['price_per_ton']].mean():,.2f} THB")
        
        print(f"\nClient Analysis:")
        if self.thai_columns['additional_data'] in self.df_clean.columns:
            clients = self.df_clean[self.thai_columns['additional_data']].str.split(' - ').str[0].nunique()
            waste_types = self.df_clean[self.thai_columns['additional_data']].str.split(' - ').str[1].nunique()
            print(f"  Unique Clients: {clients}")
            print(f"  Waste Types: {waste_types}")
    
    def daily_analysis(self):
        """Analyze daily patterns."""
        print("\n" + "=" * 60)
        print("DAILY ANALYSIS")
        print("=" * 60)
        
        daily_stats = self.df_clean.groupby(self.thai_columns['date']).agg({
            self.thai_columns['total_weight']: ['count', 'sum', 'mean'],
            self.thai_columns['garbage_weight']: 'sum',
            self.thai_columns['redeemable_weight']: 'sum',
            self.thai_columns['price_per_ton']: 'mean',
            self.thai_columns['log_count']: 'sum'
        }).round(2)
        
        daily_stats.columns = ['Records', 'Total_Weight_Sum', 'Avg_Weight', 'Total_Garbage', 'Total_Redeemable', 'Avg_Price_Per_Ton', 'Total_Logs']
        
        print("Daily Summary (first 10 days):")
        print(daily_stats.head(10))
        
        return daily_stats
    
    def truck_analysis(self):
        """Analyze truck performance."""
        print("\n" + "=" * 60)
        print("TRUCK ANALYSIS")
        print("=" * 60)
        
        truck_stats = self.df_clean.groupby(self.thai_columns['license_plate']).agg({
            self.thai_columns['total_weight']: ['count', 'sum', 'mean'],
            self.thai_columns['garbage_weight']: 'sum',
            self.thai_columns['redeemable_weight']: 'sum',
            self.thai_columns['price_per_ton']: 'mean',
            self.thai_columns['log_count']: 'sum'
        }).round(2)
        
        truck_stats.columns = ['Records', 'Total_Weight_Sum', 'Avg_Weight', 'Total_Garbage', 'Total_Redeemable', 'Avg_Price_Per_Ton', 'Total_Logs']
        
        # Add revenue calculation if redemption_value exists
        if 'redemption_value' in self.df_clean.columns:
            revenue_by_truck = self.df_clean.groupby(self.thai_columns['license_plate'])['redemption_value'].sum().round(2)
            truck_stats['Total_Revenue'] = revenue_by_truck
        else:
            # Calculate revenue from redeemable weight and price per ton
            truck_stats['Total_Revenue'] = (truck_stats['Total_Redeemable'] * truck_stats['Avg_Price_Per_Ton'] / 1000).round(2)
        
        print("Truck Performance Summary:")
        print(truck_stats.head(15))  # Show top 15 trucks
        
        return truck_stats
    
    def time_pattern_analysis(self):
        """Analyze time patterns."""
        print("\n" + "=" * 60)
        print("TIME PATTERN ANALYSIS")
        print("=" * 60)
        
        # Extract hour from time_in
        self.df_clean['hour'] = pd.to_datetime(
            self.df_clean[self.thai_columns['time_in']], 
            format='%H.%M.%S', 
            errors='coerce'
        ).dt.hour
        
        hour_distribution = self.df_clean['hour'].value_counts().sort_index()
        
        print("Operations by Hour of Day:")
        for hour, count in hour_distribution.items():
            print(f"  {hour:02d}:00 - {hour:02d}:59: {count} operations")
        
        return hour_distribution
    
    def fleet_optimization_analysis(self):
        """Analyze fleet optimization opportunities."""
        print("\n" + "=" * 60)
        print("FLEET OPTIMIZATION ANALYSIS")
        print("=" * 60)
        
        # Fleet performance metrics
        fleet_performance = self.truck_analysis()
        
        # Top performers
        top_revenue = fleet_performance.loc[fleet_performance['Total_Revenue'].idxmax()]
        top_operations = fleet_performance.loc[fleet_performance['Records'].idxmax()]
        top_weight = fleet_performance.loc[fleet_performance['Total_Weight_Sum'].idxmax()]
        
        print("🏆 TOP PERFORMERS:")
        print(f"  Highest Revenue: {top_revenue.name} - {top_revenue['Total_Revenue']:,.0f} THB")
        print(f"  Most Operations: {top_operations.name} - {top_operations['Records']} operations")
        print(f"  Highest Weight: {top_weight.name} - {top_weight['Total_Weight_Sum']:,.0f} kg")
        
        # Performance tiers
        elite_threshold = fleet_performance['Total_Revenue'].quantile(0.8)
        high_threshold = fleet_performance['Total_Revenue'].quantile(0.6)
        good_threshold = fleet_performance['Total_Revenue'].quantile(0.4)
        
        elite_trucks = fleet_performance[fleet_performance['Total_Revenue'] > elite_threshold]
        high_trucks = fleet_performance[(fleet_performance['Total_Revenue'] > high_threshold) & 
                                      (fleet_performance['Total_Revenue'] <= elite_threshold)]
        good_trucks = fleet_performance[(fleet_performance['Total_Revenue'] > good_threshold) & 
                                      (fleet_performance['Total_Revenue'] <= high_threshold)]
        needs_attention = fleet_performance[fleet_performance['Total_Revenue'] <= good_threshold]
        
        print(f"\n📊 PERFORMANCE TIERS:")
        print(f"  🏆 Elite Trucks (>80th percentile): {len(elite_trucks)} trucks")
        print(f"  ⭐ High Performers (60-80th percentile): {len(high_trucks)} trucks")
        print(f"  📈 Good Performers (40-60th percentile): {len(good_trucks)} trucks")
        print(f"  ⚠️ Needs Attention (<40th percentile): {len(needs_attention)} trucks")
        
        # Route optimization insights
        print(f"\n🛣️ ROUTE OPTIMIZATION INSIGHTS:")
        print(f"  Top route to replicate: {top_operations.name} ({top_operations['Records']} operations)")
        print(f"  Most efficient weight handling: {top_weight.name} ({top_weight['Avg_Weight']:,.0f} kg avg)")
        print(f"  Best revenue per operation: {top_revenue.name} ({top_revenue['Total_Revenue']/top_revenue['Records']:,.0f} THB/op)")
        
        return fleet_performance

    def capacity_utilization_analysis(self):
        """Analyze weight capacity utilization across the fleet."""
        print("\n" + "=" * 60)
        print("WEIGHT CAPACITY UTILIZATION ANALYSIS")
        print("=" * 60)
        
        # Capacity analysis
        max_capacity = 15  # tons
        total_weight_col = self.thai_columns['total_weight']
        
        if total_weight_col in self.df_clean.columns:
            # Calculate capacity metrics
            avg_weight = self.df_clean[total_weight_col].mean()
            max_capacity_hits = (self.df_clean[total_weight_col] >= max_capacity).sum()
            underutilized_count = (self.df_clean[total_weight_col] < (max_capacity * 0.8)).sum()
            capacity_utilization = (avg_weight / max_capacity) * 100
            
            print(f"⚖️ CAPACITY METRICS:")
            print(f"  Average Total Weight: {avg_weight:.1f} tons")
            print(f"  Max Capacity Hits (15 tons): {max_capacity_hits} operations")
            print(f"  Capacity Utilization: {capacity_utilization:.1f}%")
            print(f"  Underutilized Operations (<12 tons): {underutilized_count}")
            
            # Capacity by truck
            capacity_by_truck = self.df_clean.groupby(self.thai_columns['license_plate'])[total_weight_col].agg([
                'count', 'mean', 'max', 'min'
            ]).round(2)
            capacity_by_truck.columns = ['Operations', 'Avg_Weight', 'Max_Weight', 'Min_Weight']
            capacity_by_truck['Capacity_Utilization_%'] = (capacity_by_truck['Avg_Weight'] / max_capacity * 100).round(1)
            
            print(f"\n🚛 CAPACITY BY TRUCK:")
            print(capacity_by_truck.sort_values('Capacity_Utilization_%', ascending=False).head(10))
            
            # Optimization recommendations
            print(f"\n💡 CAPACITY OPTIMIZATION RECOMMENDATIONS:")
            print(f"  • Standardize truck sizes for optimal {max_capacity}-ton capacity utilization")
            print(f"  • Optimize routes to maximize weight per trip (current avg: {avg_weight:.1f} tons)")
            print(f"  • Focus on {underutilized_count} underutilized operations for improvement")
            print(f"  • Balance load distribution across {len(capacity_by_truck)} trucks")
            
            return capacity_by_truck
        else:
            print("Total weight column not found")
            return pd.DataFrame()

    def pricing_strategy_analysis(self):
        """Analyze pricing strategy and revenue optimization."""
        print("\n" + "=" * 60)
        print("PRICING STRATEGY ANALYSIS")
        print("=" * 60)
        
        price_col = self.thai_columns['price_per_ton']
        if price_col in self.df_clean.columns:
            # Pricing analysis
            avg_price = self.df_clean[price_col].mean()
            price_range = self.df_clean[price_col].max() - self.df_clean[price_col].min()
            price_std = self.df_clean[price_col].std()
            
            print(f"💰 PRICING INSIGHTS:")
            print(f"  Average Price per Ton: {avg_price:,.0f} THB")
            print(f"  Price Range: {price_range:,.0f} THB")
            print(f"  Price Standard Deviation: {price_std:,.0f} THB")
            
            # Price distribution
            price_quartiles = self.df_clean[price_col].quantile([0.25, 0.5, 0.75])
            print(f"  Price Quartiles: Q1={price_quartiles[0.25]:,.0f}, Q2={price_quartiles[0.5]:,.0f}, Q3={price_quartiles[0.75]:,.0f} THB")
            
            # Pricing by client (if available)
            if 'redemption_value' in self.df_clean.columns:
                revenue_by_price = self.df_clean.groupby(price_col)['redemption_value'].agg(['count', 'sum']).round(2)
                revenue_by_price.columns = ['Operations', 'Total_Revenue']
                revenue_by_price['Avg_Revenue_per_Op'] = (revenue_by_price['Total_Revenue'] / revenue_by_price['Operations']).round(2)
                
                print(f"\n📊 REVENUE BY PRICE TIER:")
                print(revenue_by_price.sort_index())
            
            # Optimization recommendations
            print(f"\n💡 PRICING OPTIMIZATION RECOMMENDATIONS:")
            if price_std > avg_price * 0.1:  # If standard deviation > 10% of average
                print(f"  • Consider standardizing pricing (current variation: {price_std/avg_price*100:.1f}%)")
            else:
                print(f"  • Pricing is relatively consistent (variation: {price_std/avg_price*100:.1f}%)")
            
            print(f"  • Focus on high-value operations above {price_quartiles[0.75]:,.0f} THB/ton")
            print(f"  • Analyze low-price operations below {price_quartiles[0.25]:,.0f} THB/ton for improvement")
            
            return revenue_by_price if 'redemption_value' in self.df_clean.columns else pd.DataFrame()
        else:
            print("Price per ton column not found")
            return pd.DataFrame()

    def column_structure_analysis(self):
        """Analyze the column structure and data types."""
        print("\n" + "=" * 60)
        print("COLUMN STRUCTURE ANALYSIS")
        print("=" * 60)
        
        print("Column Structure (A-M):")
        column_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        
        for i, (col_letter, col_name) in enumerate(zip(column_letters, self.df.columns)):
            data_type = str(self.df[col_name].dtype)
            non_null_count = self.df[col_name].count()
            unique_count = self.df[col_name].nunique()
            
            print(f"  Column {col_letter}: {col_name}")
            print(f"    Data Type: {data_type}")
            print(f"    Non-null Count: {non_null_count}")
            print(f"    Unique Values: {unique_count}")
            
            # Show sample values for first few columns
            if i < 5:
                sample_values = self.df[col_name].dropna().head(3).tolist()
                print(f"    Sample Values: {sample_values}")
            print()
    
    def export_analysis(self, filename='thai_machinery_analysis_simple.xlsx'):
        """Export analysis results to Excel."""
        print(f"\nExporting analysis to {filename}...")
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Clean data
            self.df_clean.to_excel(writer, sheet_name='Clean_Data', index=False)
            
            # Daily statistics
            daily_stats = self.daily_analysis()
            daily_stats.to_excel(writer, sheet_name='Daily_Statistics')
            
            # Truck statistics
            truck_stats = self.truck_analysis()
            truck_stats.to_excel(writer, sheet_name='Truck_Statistics')
            
            # Hour distribution
            hour_dist = self.time_pattern_analysis()
            hour_dist.to_frame('Operations_Count').to_excel(writer, sheet_name='Hour_Distribution')
            
            # Fleet optimization analysis
            fleet_opt = self.fleet_optimization_analysis()
            fleet_opt.to_excel(writer, sheet_name='Fleet_Optimization', index=True)
            
            # Capacity utilization analysis
            capacity_util = self.capacity_utilization_analysis()
            capacity_util.to_excel(writer, sheet_name='Capacity_Utilization', index=True)
            
            # Pricing strategy analysis
            pricing_strategy = self.pricing_strategy_analysis()
            if not pricing_strategy.empty:
                pricing_strategy.to_excel(writer, sheet_name='Pricing_Strategy', index=True)
            
            # Column structure analysis
            column_analysis = pd.DataFrame({
                'Column': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'],
                'Column_Name': list(self.df.columns),
                'Data_Type': [str(self.df[col].dtype) for col in self.df.columns],
                'Non_Null_Count': [self.df[col].count() for col in self.df.columns],
                'Unique_Values': [self.df[col].nunique() for col in self.df.columns]
            })
            column_analysis.to_excel(writer, sheet_name='Column_Analysis', index=False)
            
            # Summary statistics
            summary_stats = pd.DataFrame({
                'Metric': [
                    'Total Records',
                    'Date Range Start',
                    'Date Range End',
                    'Unique Trucks',
                    'Total Garbage Weight',
                    'Total Redeemable Weight',
                    'Average Price per Ton',
                    'Total Revenue',
                    'Average Capacity Utilization %',
                    'Performance Tiers (Elite/High/Good/Needs Attention)'
                ],
                'Value': [
                    len(self.df_clean),
                    str(self.df_clean[self.thai_columns['date']].min()),
                    str(self.df_clean[self.thai_columns['date']].max()),
                    self.df_clean[self.thai_columns['license_plate']].nunique(),
                    f"{self.df_clean[self.thai_columns['garbage_weight']].sum():,.2f} kg",
                    f"{self.df_clean[self.thai_columns['redeemable_weight']].sum():,.2f} kg",
                    f"{self.df_clean[self.thai_columns['price_per_ton']].mean():,.2f} THB",
                    f"{self.df_clean['redemption_value'].sum():,.2f} THB" if 'redemption_value' in self.df_clean.columns else "N/A",
                    f"{(self.df_clean[self.thai_columns['total_weight']].mean() / 15 * 100):.1f}%" if self.thai_columns['total_weight'] in self.df_clean.columns else "N/A",
                    "See Fleet_Optimization sheet for details"
                ]
            })
            summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)
        
        print(f"Analysis exported to {filename}")
    
    def export_json_for_dashboard(self, filename='dashboard_data.json'):
        """Export data in JSON format for the dashboard."""
        print(f"\nExporting dashboard data to {filename}...")
        
        import json
        
        # Get all the analysis data
        daily_stats = self.daily_analysis()
        truck_stats = self.truck_analysis()
        hour_dist = self.time_pattern_analysis()
        fleet_opt = self.fleet_optimization_analysis()
        capacity_util = self.capacity_utilization_analysis()
        pricing_strategy = self.pricing_strategy_analysis()
        
        # Get new business intelligence data
        client_pricing = self.client_pricing_analysis()
        operational_efficiency = self.operational_efficiency_analysis()
        waste_management = self.waste_management_analysis()
        strategic_bi = self.strategic_business_intelligence()
        
        # Prepare dashboard data structure
        dashboard_data = {
            "metadata": {
                "totalRecords": len(self.df_clean),
                "uniqueTrucks": self.df_clean[self.thai_columns['license_plate']].nunique(),
                "dateRange": f"{self.df_clean[self.thai_columns['date']].min()} to {self.df_clean[self.thai_columns['date']].max()}",
                "analysisDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "rawData": self.prepare_raw_data_for_dashboard(),
            "fleetPerformance": {
                "topPerformers": {
                    "highestRevenue": {
                        "license": truck_stats.loc[truck_stats['Total_Revenue'].idxmax()].name,
                        "revenue": float(truck_stats.loc[truck_stats['Total_Revenue'].idxmax()]['Total_Revenue']),
                        "operations": int(truck_stats.loc[truck_stats['Total_Revenue'].idxmax()]['Records'])
                    },
                    "mostOperations": {
                        "license": truck_stats.loc[truck_stats['Records'].idxmax()].name,
                        "operations": int(truck_stats.loc[truck_stats['Records'].idxmax()]['Records']),
                        "revenue": float(truck_stats.loc[truck_stats['Records'].idxmax()]['Total_Revenue'])
                    },
                    "highestWeight": {
                        "license": truck_stats.loc[truck_stats['Total_Weight_Sum'].idxmax()].name,
                        "weight": float(truck_stats.loc[truck_stats['Total_Weight_Sum'].idxmax()]['Total_Weight_Sum']),
                        "operations": int(truck_stats.loc[truck_stats['Total_Weight_Sum'].idxmax()]['Records'])
                    }
                },
                "performanceTiers": {
                    "elite": int(len(truck_stats[truck_stats['Total_Revenue'] > truck_stats['Total_Revenue'].quantile(0.8)])),
                    "high": int(len(truck_stats[(truck_stats['Total_Revenue'] > truck_stats['Total_Revenue'].quantile(0.6)) & (truck_stats['Total_Revenue'] <= truck_stats['Total_Revenue'].quantile(0.8))])),
                    "good": int(len(truck_stats[(truck_stats['Total_Revenue'] > truck_stats['Total_Revenue'].quantile(0.4)) & (truck_stats['Total_Revenue'] <= truck_stats['Total_Revenue'].quantile(0.6))])),
                    "needsAttention": int(len(truck_stats[truck_stats['Total_Revenue'] <= truck_stats['Total_Revenue'].quantile(0.4)]))
                }
            },
            "capacityUtilization": {
                "averageWeight": float(self.df_clean[self.thai_columns['total_weight']].mean()),
                "maxCapacityHits": int((self.df_clean[self.thai_columns['total_weight']] >= 15).sum()),
                "capacityUtilizationPercent": float((self.df_clean[self.thai_columns['total_weight']].mean() / 15) * 100),
                "underutilizedOperations": int((self.df_clean[self.thai_columns['total_weight']] < 12).sum())
            },
            "pricingStrategy": {
                "averagePricePerTon": float(self.df_clean[self.thai_columns['price_per_ton']].mean()),
                "priceRange": float(self.df_clean[self.thai_columns['price_per_ton']].max() - self.df_clean[self.thai_columns['price_per_ton']].min()),
                "priceStandardDeviation": float(self.df_clean[self.thai_columns['price_per_ton']].std()),
                "priceQuartiles": {
                    "q1": float(self.df_clean[self.thai_columns['price_per_ton']].quantile(0.25)),
                    "q2": float(self.df_clean[self.thai_columns['price_per_ton']].quantile(0.5)),
                    "q3": float(self.df_clean[self.thai_columns['price_per_ton']].quantile(0.75))
                }
            },
            "hourlyDistribution": hour_dist.to_dict() if not hour_dist.empty else {},
            "truckDetails": truck_stats.reset_index().to_dict('records') if not truck_stats.empty else [],
            "capacityByTruck": capacity_util.reset_index().to_dict('records') if not capacity_util.empty else [],
            
            # New business intelligence data
            "clientPricing": client_pricing.to_dict('index') if not client_pricing.empty else {},
            "operationalEfficiency": operational_efficiency,
            "wasteManagement": waste_management,
            "strategicBI": strategic_bi
        }
        
        # Write to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, ensure_ascii=False, indent=2, default=str)
        
        # Also copy to html_dashboards folder for easier access
        html_filename = '../html_dashboards/dashboard_data.json'
        try:
            with open(html_filename, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, ensure_ascii=False, indent=2, default=str)
            print(f"  Also saved to: {html_filename}")
        except Exception as e:
            print(f"  Note: Could not save to html_dashboards folder: {e}")
        
        print(f"Dashboard data exported to {filename}")
    
    def client_pricing_analysis(self):
        """Analyze client pricing strategies and variations."""
        print("\n" + "=" * 60)
        print("CLIENT PRICING STRATEGY ANALYSIS")
        print("=" * 60)
        
        # Extract client information from additional data
        client_data = []
        for _, row in self.df_clean.iterrows():
            additional_data = str(row[self.thai_columns['additional_data']])
            if 'CLIENT-' in additional_data:
                parts = additional_data.split(' - ')
                if len(parts) >= 3:
                    client = parts[0]
                    waste_type = parts[1]
                    price_per_ton = row[self.thai_columns['price_per_ton']]
                    redeemable_weight = row[self.thai_columns['redeemable_weight']]
                    total_revenue = redeemable_weight * price_per_ton / 1000
                    
                    client_data.append({
                        'client': client,
                        'waste_type': waste_type,
                        'price_per_ton': price_per_ton,
                        'redeemable_weight': redeemable_weight,
                        'total_revenue': total_revenue,
                        'license_plate': row[self.thai_columns['license_plate']]
                    })
        
        if client_data:
            client_df = pd.DataFrame(client_data)
            
            # Client pricing analysis
            client_pricing = client_df.groupby('client')['price_per_ton'].agg(['mean', 'min', 'max', 'count']).round(2)
            client_pricing.columns = ['Avg_Price_Per_Ton', 'Min_Price', 'Max_Price', 'Operations']
            
            print("💰 CLIENT PRICING STRATEGY:")
            print(f"  Price variation: {client_pricing['Min_Price'].min():.0f} THB/ton to {client_pricing['Max_Price'].max():.0f} THB/ton")
            print(f"  Price spread: {((client_pricing['Max_Price'].max() - client_pricing['Min_Price'].min()) / client_pricing['Avg_Price_Per_Ton'].mean() * 100):.1f}%")
            
            # Top and lowest payers
            top_payer = client_pricing.loc[client_pricing['Avg_Price_Per_Ton'].idxmax()]
            lowest_payer = client_pricing.loc[client_pricing['Avg_Price_Per_Ton'].idxmin()]
            
            print(f"  Top Payer: {client_pricing['Avg_Price_Per_Ton'].idxmax()} gets {top_payer['Avg_Price_Per_Ton']:.0f} THB/ton")
            print(f"  Lowest Payer: {client_pricing['Avg_Price_Per_Ton'].idxmin()} gets {lowest_payer['Avg_Price_Per_Ton']:.0f} THB/ton")
            print(f"  Action: Negotiate higher rates with low-paying clients or offer premium services")
            
            return client_pricing
        else:
            print("No client data found in additional data column")
            return pd.DataFrame()
    
    def operational_efficiency_analysis(self):
        """Analyze operational efficiency and time patterns."""
        print("\n" + "=" * 60)
        print("OPERATIONAL EFFICIENCY ANALYSIS")
        print("=" * 60)
        
        # Calculate processing times
        processing_times = []
        for _, row in self.df_clean.iterrows():
            time_in = str(row[self.thai_columns['time_in']])
            time_out = str(row[self.thai_columns['time_out']])
            
            try:
                # Parse times (HH.MM.SS format)
                in_parts = time_in.split('.')
                out_parts = time_out.split('.')
                
                if len(in_parts) >= 2 and len(out_parts) >= 2:
                    in_minutes = int(in_parts[0]) * 60 + int(in_parts[1])
                    out_minutes = int(out_parts[0]) * 60 + int(out_parts[1])
                    
                    # Handle day wrap-around
                    if out_minutes < in_minutes:
                        out_minutes += 24 * 60
                    
                    processing_time = out_minutes - in_minutes
                    processing_times.append(processing_time)
            except:
                continue
        
        if processing_times:
            avg_processing_time = np.mean(processing_times)
            print(f"⏰ PROCESSING TIME OPTIMIZATION:")
            print(f"  Average processing time: {avg_processing_time:.1f} minutes per truck")
            print(f"  Range: {min(processing_times):.0f} to {max(processing_times):.0f} minutes")
        
        # Peak hours analysis
        hour_dist = self.time_pattern_analysis()
        peak_hour = None
        low_hour = None
        active_hours = 0
        
        if not hour_dist.empty:
            try:
                # hour_dist is a Series, so we need to find the peak differently
                peak_hour_name = hour_dist.idxmax()
                peak_hour_count = hour_dist.max()
                low_hour_name = hour_dist.idxmin()
                low_hour_count = hour_dist.min()
                
                print(f"  Peak Hours: {peak_hour_name} ({peak_hour_count} ops)")
                print(f"  Low Activity: {low_hour_name} ({low_hour_count} ops) - Maintenance Window Opportunity")
                
                # 24/7 operations pattern
                active_hours = len(hour_dist[hour_dist > 0])
                print(f"  24/7 OPERATIONS PATTERN:")
                print(f"  Operations span: {active_hours} hours per day")
                print(f"  Night Shift Efficiency: 00:00-06:00 has lower volume but consistent operations")
                print(f"  Action: Optimize night shift staffing and pricing")
            except Exception as e:
                print(f"  Error in peak hours analysis: {e}")
        
        return {
            'avg_processing_time': avg_processing_time if processing_times else 0,
            'peak_hour': peak_hour_name if 'peak_hour_name' in locals() else None,
            'low_hour': low_hour_name if 'low_hour_name' in locals() else None,
            'active_hours': active_hours
        }
    
    def waste_management_analysis(self):
        """Analyze waste management and quality insights."""
        print("\n" + "=" * 60)
        print("WASTE MANAGEMENT & QUALITY ANALYSIS")
        print("=" * 60)
        
        # Redemption rate analysis
        avg_garbage_weight = self.df_clean[self.thai_columns['garbage_weight']].mean()
        avg_redeemable_weight = self.df_clean[self.thai_columns['redeemable_weight']].mean()
        redemption_rate = (avg_redeemable_weight / avg_garbage_weight) * 100 if avg_garbage_weight > 0 else 0
        loss_rate = 100 - redemption_rate
        
        print(f"🗑️ REDEMPTION RATE OPTIMIZATION:")
        print(f"  Average garbage weight: {avg_garbage_weight:.1f} tons")
        print(f"  Average redeemable: {avg_redeemable_weight:.1f} tons ({redemption_rate:.0f}% of garbage weight)")
        print(f"  {loss_rate:.0f}% Loss: {avg_garbage_weight - avg_redeemable_weight:.1f} tons per truck is non-redeemable waste")
        print(f"  Action: Improve sorting processes to increase redeemable percentage")
        
        # Weight vs Value correlation
        correlation = self.df_clean[self.thai_columns['garbage_weight']].corr(
            self.df_clean[self.thai_columns['price_per_ton']]
        )
        
        print(f"  WEIGHT VS. VALUE CORRELATION:")
        print(f"  Correlation coefficient: {correlation:.3f}")
        if abs(correlation) < 0.3:
            print(f"  Higher weight doesn't always mean higher value")
            print(f"  Quality over Quantity: Focus on waste type quality, not just weight")
        else:
            print(f"  Strong correlation between weight and value")
        
        # Waste type analysis
        waste_types = {}
        for _, row in self.df_clean.iterrows():
            additional_data = str(row[self.thai_columns['additional_data']])
            if ' - ' in additional_data:
                parts = additional_data.split(' - ')
                if len(parts) >= 2:
                    waste_type = parts[1]
                    if waste_type not in waste_types:
                        waste_types[waste_type] = {'count': 0, 'total_value': 0}
                    waste_types[waste_type]['count'] += 1
                    waste_types[waste_type]['total_value'] += row.get('redemption_value', 0)
        
        if waste_types:
            print(f"  WASTE TYPE ANALYSIS:")
            for waste_type, data in waste_types.items():
                avg_value = data['total_value'] / data['count']
                print(f"    {waste_type}: {data['count']} operations, {avg_value:.0f} THB avg value")
        
        return {
            'redemption_rate': redemption_rate,
            'loss_rate': loss_rate,
            'weight_value_correlation': correlation,
            'waste_types': waste_types
        }
    
    def strategic_business_intelligence(self):
        """Generate strategic business intelligence insights."""
        print("\n" + "=" * 60)
        print("STRATEGIC BUSINESS INTELLIGENCE")
        print("=" * 60)
        
        # Client portfolio analysis
        client_data = []
        for _, row in self.df_clean.iterrows():
            additional_data = str(row[self.thai_columns['additional_data']])
            if 'CLIENT-' in additional_data:
                parts = additional_data.split(' - ')
                if len(parts) >= 3:
                    client = parts[0]
                    waste_type = parts[1]
                    client_data.append({'client': client, 'waste_type': waste_type})
        
        if client_data:
            client_df = pd.DataFrame(client_data)
            unique_clients = client_df['client'].nunique()
            unique_waste_types = client_df['waste_type'].nunique()
            
            print(f"📊 CLIENT PORTFOLIO ANALYSIS:")
            print(f"  {unique_clients} active clients with different waste preferences")
            print(f"  {unique_waste_types} different waste types processed")
            print(f"  Client Segmentation: Some clients consistently provide higher-value waste")
            print(f"  Action: Develop targeted services for high-value waste streams")
        
        # Seasonal & daily patterns
        total_records = len(self.df_clean)
        unique_dates = self.df_clean[self.thai_columns['date']].nunique()
        avg_daily_operations = total_records / unique_dates if unique_dates > 0 else 0
        
        print(f"  SEASONAL & DAILY PATTERNS:")
        print(f"  Consistent daily operations ({total_records} records across {unique_dates} days)")
        print(f"  Average daily operations: {avg_daily_operations:.1f}")
        print(f"  Predictability: Enables better resource planning and staffing")
        print(f"  Action: Implement predictive scheduling based on historical patterns")
        
        # Cost-benefit analysis
        total_revenue = self.df_clean.get('redemption_value', pd.Series([0] * len(self.df_clean))).sum()
        unique_trucks = self.df_clean[self.thai_columns['license_plate']].nunique()
        avg_revenue_per_truck = total_revenue / unique_trucks if unique_trucks > 0 else 0
        
        print(f"  COST-BENEFIT ANALYSIS:")
        print(f"  Total redemption value: {total_revenue:,.0f} THB")
        print(f"  Per Truck Revenue: Average {avg_revenue_per_truck:,.0f} THB per truck")
        print(f"  ROI Calculation: Compare truck costs vs. revenue generation")
        
        # Revenue per truck analysis
        truck_stats = self.truck_analysis()
        if not truck_stats.empty:
            highest_revenue_truck = truck_stats.loc[truck_stats['Total_Revenue'].idxmax()]
            print(f"  REVENUE PER TRUCK ANALYSIS:")
            print(f"  Highest revenue truck: {highest_revenue_truck.name} ({highest_revenue_truck['Total_Revenue']:,.0f} THB)")
            print(f"  ROI Opportunity: Invest in more trucks like {highest_revenue_truck.name} or replicate their operational model")
        
        return {
            'unique_clients': unique_clients if client_data else 0,
            'unique_waste_types': unique_waste_types if client_data else 0,
            'total_revenue': total_revenue,
            'avg_revenue_per_truck': avg_revenue_per_truck,
            'avg_daily_operations': avg_daily_operations,
            'highest_revenue_truck': highest_revenue_truck.name if not truck_stats.empty else None
        }
    
    def prepare_raw_data_for_dashboard(self):
        """Prepare raw data in the format expected by the dashboard."""
        raw_data = []
        
        for _, row in self.df_clean.iterrows():
            # Extract the redemption value from Column L
            redemption_value = row.get('redemption_value', 0)
            
            raw_record = {
                "date": str(row[self.thai_columns['date']]),
                "logNumber": str(row[self.thai_columns['log_number']]),
                "license": str(row[self.thai_columns['license_plate']]),
                "timeIn": str(row[self.thai_columns['time_in']]),
                "timeOut": str(row[self.thai_columns['time_out']]),
                "totalWeight": float(row[self.thai_columns['total_weight']]),
                "maxRedemption": float(row[self.thai_columns['max_redemption']]),
                "emptyWeight": float(row[self.thai_columns['empty_weight']]),
                "garbageWeight": float(row[self.thai_columns['garbage_weight']]),
                "redeemable": float(row[self.thai_columns['redeemable_weight']]),
                "pricePerTon": float(row[self.thai_columns['price_per_ton']]),
                "totalRedemptionValue": float(redemption_value),
                "additionalData": str(row[self.thai_columns['additional_data']])
            }
            raw_data.append(raw_record)
        
        return raw_data
    
    def generate_report(self):
        """Generate a comprehensive analysis report."""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 60)
        print("Thai Truck Weigh Station Log Data - 13 Columns (A-M)")
        print("Thai Buddhist Calendar Year 2568")
        print("=" * 60)
        
        # Column structure analysis
        self.column_structure_analysis()
        
        # Basic statistics
        self.basic_statistics()
        
        # Detailed analysis
        daily_stats = self.daily_analysis()
        truck_stats = self.truck_analysis()
        hour_dist = self.time_pattern_analysis()
        
        # New fleet optimization analyses
        fleet_opt = self.fleet_optimization_analysis()
        capacity_util = self.capacity_utilization_analysis()
        pricing_strategy = self.pricing_strategy_analysis()
        
        # Advanced business intelligence analyses
        client_pricing_analysis = self.client_pricing_analysis()
        operational_efficiency_analysis = self.operational_efficiency_analysis()
        waste_management_analysis = self.waste_management_analysis()
        strategic_business_intelligence = self.strategic_business_intelligence()
        
        # Export results
        self.export_analysis('thai_truck_weigh_analysis_simple.xlsx')
        
        # Export JSON data for dashboard
        self.export_json_for_dashboard('dashboard_data.json')
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE!")
        print("=" * 60)
        print("Files generated:")
        print("  - thai_truck_weigh_analysis_simple.xlsx (Excel with all data and analysis)")
        print("  - dashboard_data.json (JSON data for dashboard)")
        print("\nKey insights:")
        print("  - Column A: Date tracking (Thai Buddhist calendar)")
        print("  - Columns B-L: Truck weigh station operational data")
        print("  - Column M: Log count per date")
        print("  - Green summary rows provide daily totals")
        print("  - Track garbage collection and redemption patterns")
        print("  - Compare truck performance and client pricing")

def main():
    """Main function to run the analysis."""
    print("Simple Thai Truck Weigh Station Log Data Analyzer (13 Columns A-M)")
    print("Thai Buddhist Calendar Year 2568")
    print("=" * 50)
    
    # Try to load the new real data file
    try:
        analyzer = SimpleThaiTruckAnalyzer('thai_truck_weigh_logs_real_2568.xlsx')
        analyzer.generate_report()
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure you have the 'thai_truck_weigh_logs_real_2568.xlsx' file or provide a different file path.")

if __name__ == "__main__":
    main()
