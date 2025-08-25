#!/usr/bin/env python3
"""
Test script to verify dashboard data integrity and functionality.
"""

import json
import pandas as pd
from datetime import datetime

def test_dashboard_data():
    """Test the dashboard data for integrity and completeness."""
    print("🧪 Testing Dashboard Data Integrity")
    print("=" * 50)
    
    try:
        # Load dashboard data
        with open('dashboard_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ Dashboard data loaded successfully")
        
        # Test metadata
        metadata = data.get('metadata', {})
        print(f"📊 Metadata:")
        print(f"   Total Records: {metadata.get('totalRecords', 'N/A')}")
        print(f"   Unique Trucks: {metadata.get('uniqueTrucks', 'N/A')}")
        print(f"   Date Range: {metadata.get('dateRange', 'N/A')}")
        print(f"   Analysis Date: {metadata.get('analysisDate', 'N/A')}")
        
        # Test raw data
        raw_data = data.get('rawData', [])
        print(f"📋 Raw Data: {len(raw_data)} records")
        
        if raw_data:
            sample_record = raw_data[0]
            print(f"   Sample record keys: {list(sample_record.keys())}")
            print(f"   Sample license: {sample_record.get('license', 'N/A')}")
            print(f"   Sample weight: {sample_record.get('totalWeight', 'N/A')}")
        
        # Test fleet performance data
        fleet_data = data.get('fleetPerformance', {})
        if fleet_data:
            print(f"🚛 Fleet Performance Data:")
            top_performers = fleet_data.get('topPerformers', {})
            if top_performers:
                print(f"   Highest Revenue: {top_performers.get('highestRevenue', {}).get('license', 'N/A')}")
                print(f"   Most Operations: {top_performers.get('mostOperations', {}).get('license', 'N/A')}")
                print(f"   Highest Weight: {top_performers.get('highestWeight', {}).get('license', 'N/A')}")
        
        # Test capacity utilization
        capacity_data = data.get('capacityUtilization', {})
        if capacity_data:
            print(f"⚖️ Capacity Utilization:")
            print(f"   Average Weight: {capacity_data.get('averageWeight', 'N/A')}")
            print(f"   Capacity Utilization: {capacity_data.get('capacityUtilizationPercent', 'N/A')}%")
            print(f"   Max Capacity Hits: {capacity_data.get('maxCapacityHits', 'N/A')}")
        
        # Test pricing strategy
        pricing_data = data.get('pricingStrategy', {})
        if pricing_data:
            print(f"💰 Pricing Strategy:")
            print(f"   Average Price per Ton: {pricing_data.get('averagePricePerTon', 'N/A')}")
            print(f"   Price Range: {pricing_data.get('priceRange', 'N/A')}")
        
        # Test truck details
        truck_details = data.get('truckDetails', [])
        print(f"🚚 Truck Details: {len(truck_details)} trucks")
        
        if truck_details:
            # Find top revenue truck
            top_revenue_truck = max(truck_details, key=lambda x: x.get('Total_Revenue', 0))
            print(f"   Top Revenue Truck: {top_revenue_truck.get('index', 'N/A')}")
            print(f"   Top Revenue Amount: {top_revenue_truck.get('Total_Revenue', 'N/A')}")
        
        # Test hourly distribution
        hourly_data = data.get('hourlyDistribution', {})
        if hourly_data:
            print(f"⏰ Hourly Distribution: {len(hourly_data)} hours")
            peak_hour = max(hourly_data.items(), key=lambda x: x[1]) if hourly_data else None
            if peak_hour:
                print(f"   Peak Hour: {peak_hour[0]} ({peak_hour[1]} operations)")
        
        print("\n✅ All tests passed! Dashboard data is properly formatted.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard data: {e}")
        return False

def test_excel_analysis():
    """Test the Excel analysis file."""
    print("\n📊 Testing Excel Analysis File")
    print("=" * 50)
    
    try:
        # Try to read the Excel file
        excel_file = 'thai_truck_weigh_analysis_simple.xlsx'
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        print(f"✅ Excel file loaded successfully: {excel_file}")
        print(f"📋 Sheets found: {list(excel_data.keys())}")
        
        # Check key sheets
        expected_sheets = ['Clean_Data', 'Daily_Statistics', 'Truck_Statistics', 'Summary_Statistics']
        for sheet in expected_sheets:
            if sheet in excel_data:
                print(f"   ✅ {sheet}: {len(excel_data[sheet])} rows")
            else:
                print(f"   ❌ {sheet}: Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Excel file: {e}")
        return False

def test_real_data():
    """Test the real data file."""
    print("\n📈 Testing Real Data File")
    print("=" * 50)
    
    try:
        # Load real data
        real_data = pd.read_excel('thai_truck_weigh_logs_real_2568.xlsx')
        
        print(f"✅ Real data loaded successfully")
        print(f"📊 Shape: {real_data.shape}")
        print(f"📋 Columns: {list(real_data.columns)}")
        
        # Check for expected columns
        expected_columns = ['วนดอปไปช', 'เลขทะเบียนรถ', 'น้ำหนักรวมรถ', 'ราคาไถ่ต่อตัน']
        for col in expected_columns:
            if col in real_data.columns:
                print(f"   ✅ {col}: {real_data[col].nunique()} unique values")
            else:
                print(f"   ❌ {col}: Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing real data: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Thai Truck Weigh Station Dashboard - Data Integrity Test")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    tests = [
        test_dashboard_data,
        test_excel_analysis,
        test_real_data
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your dashboard is ready to use.")
        print("\n📖 Next steps:")
        print("   1. Run: python3 -m http.server 8000")
        print("   2. Open: http://localhost:8000/thai_truck_dashboard.html")
        print("   3. View your real data analysis!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
