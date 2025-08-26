import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
import warnings
warnings.filterwarnings('ignore')

class RecycledItemsAnalyzer:
    def __init__(self):
        self.sales_data = []
        self.purchase_data = []
        
        # Item pricing data
        self.item_prices = {
            'clearBottles': 2.5,
            'mixedPlastic': 1.8,
            'iron': 15.0,
            'aluminum': 45.0,
            'steelCans': 8.0,
            'beerCans': 12.0,
            'beerCrates': 25.0,
            'crates': 35.0,
            'paperScraps': 3.5,
            'usedOil': 18.0,
            'buckets': 15.0,
            'glassBottles': 1.5,
            'battery': 85.0
        }
        
        self.item_costs = {
            'clearBottles': 1.8,
            'mixedPlastic': 1.2,
            'iron': 12.0,
            'aluminum': 38.0,
            'steelCans': 6.5,
            'beerCans': 10.0,
            'beerCrates': 20.0,
            'crates': 28.0,
            'paperScraps': 2.8,
            'usedOil': 15.0,
            'buckets': 12.0,
            'glassBottles': 1.2,
            'battery': 70.0
        }
    
    def get_item_price(self, item):
        """Get the selling price for an item"""
        return self.item_prices.get(item, 0)
    
    def get_item_cost(self, item):
        """Get the cost price for an item"""
        return self.item_costs.get(item, 0)
        
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Sample sales data
        self.sales_data = [
            {
                'date': '2024-01-15',
                'customer': 'Factory A',
                'clearBottles': 150,
                'mixedPlastic': 25,
                'iron': 45.5,
                'aluminum': 12.3,
                'steelCans': 80,
                'beerCans': 120,
                'beerCrates': 15,
                'crates': 8,
                'paperScraps': 30.2,
                'usedOil': 5.5,
                'buckets': 12,
                'glassBottles': 200,
                'battery': 8,
                'totalRevenue': 8500
            },
            {
                'date': '2024-01-16',
                'customer': 'Recycling Center 1',
                'clearBottles': 200,
                'mixedPlastic': 30,
                'iron': 60.2,
                'aluminum': 18.7,
                'steelCans': 95,
                'beerCans': 150,
                'beerCrates': 20,
                'crates': 12,
                'paperScraps': 45.8,
                'usedOil': 8.2,
                'buckets': 18,
                'glassBottles': 250,
                'battery': 12,
                'totalRevenue': 12000
            },
            {
                'date': '2024-01-17',
                'customer': 'Factory B',
                'clearBottles': 180,
                'mixedPlastic': 22,
                'iron': 38.5,
                'aluminum': 15.2,
                'steelCans': 75,
                'beerCans': 110,
                'beerCrates': 18,
                'crates': 10,
                'paperScraps': 28.5,
                'usedOil': 6.8,
                'buckets': 15,
                'glassBottles': 220,
                'battery': 10,
                'totalRevenue': 9800
            },
            {
                'date': '2024-01-18',
                'customer': 'Waste Management Co',
                'clearBottles': 120,
                'mixedPlastic': 18,
                'iron': 32.1,
                'aluminum': 11.8,
                'steelCans': 65,
                'beerCans': 95,
                'beerCrates': 12,
                'crates': 6,
                'paperScraps': 22.3,
                'usedOil': 4.5,
                'buckets': 10,
                'glassBottles': 180,
                'battery': 6,
                'totalRevenue': 7200
            },
            {
                'date': '2024-01-19',
                'customer': 'Factory C',
                'clearBottles': 160,
                'mixedPlastic': 28,
                'iron': 42.8,
                'aluminum': 14.5,
                'steelCans': 85,
                'beerCans': 130,
                'beerCrates': 16,
                'crates': 9,
                'paperScraps': 35.7,
                'usedOil': 7.2,
                'buckets': 14,
                'glassBottles': 210,
                'battery': 9,
                'totalRevenue': 9200
            },
            {
                'date': '2024-01-20',
                'customer': 'Factory A',
                'clearBottles': 140,
                'mixedPlastic': 25,
                'iron': 35.2,
                'aluminum': 12.8,
                'steelCans': 70,
                'beerCans': 120,
                'beerCrates': 14,
                'crates': 8,
                'paperScraps': 30.5,
                'usedOil': 6.5,
                'buckets': 12,
                'glassBottles': 200,
                'battery': 8,
                'totalRevenue': 8500
            },
            {
                'date': '2024-01-21',
                'customer': 'Factory B',
                'clearBottles': 170,
                'mixedPlastic': 30,
                'iron': 45.1,
                'aluminum': 16.2,
                'steelCans': 90,
                'beerCans': 140,
                'beerCrates': 18,
                'crates': 11,
                'paperScraps': 38.9,
                'usedOil': 7.8,
                'buckets': 16,
                'glassBottles': 230,
                'battery': 11,
                'totalRevenue': 10500
            },
            {
                'date': '2024-01-22',
                'customer': 'Waste Management Co',
                'clearBottles': 130,
                'mixedPlastic': 20,
                'iron': 30.5,
                'aluminum': 10.5,
                'steelCans': 60,
                'beerCans': 100,
                'beerCrates': 13,
                'crates': 7,
                'paperScraps': 25.2,
                'usedOil': 5.2,
                'buckets': 11,
                'glassBottles': 190,
                'battery': 7,
                'totalRevenue': 7800
            },
            {
                'date': '2024-01-23',
                'customer': 'Factory C',
                'clearBottles': 180,
                'mixedPlastic': 32,
                'iron': 48.3,
                'aluminum': 17.8,
                'steelCans': 95,
                'beerCans': 150,
                'beerCrates': 20,
                'crates': 12,
                'paperScraps': 42.1,
                'usedOil': 8.5,
                'buckets': 18,
                'glassBottles': 250,
                'battery': 12,
                'totalRevenue': 11200
            },
            {
                'date': '2024-01-24',
                'customer': 'Factory A',
                'clearBottles': 150,
                'mixedPlastic': 27,
                'iron': 38.7,
                'aluminum': 13.9,
                'steelCans': 75,
                'beerCans': 125,
                'beerCrates': 15,
                'crates': 9,
                'paperScraps': 32.8,
                'usedOil': 6.9,
                'buckets': 13,
                'glassBottles': 205,
                'battery': 9,
                'totalRevenue': 8900
            },
            {
                'date': '2024-01-25',
                'customer': 'Factory B',
                'clearBottles': 175,
                'mixedPlastic': 31,
                'iron': 46.2,
                'aluminum': 15.7,
                'steelCans': 88,
                'beerCans': 135,
                'beerCrates': 17,
                'crates': 10,
                'paperScraps': 36.4,
                'usedOil': 7.4,
                'buckets': 15,
                'glassBottles': 225,
                'battery': 10,
                'totalRevenue': 9800
            },
            {
                'date': '2024-01-26',
                'customer': 'Waste Management Co',
                'clearBottles': 125,
                'mixedPlastic': 19,
                'iron': 29.8,
                'aluminum': 9.8,
                'steelCans': 58,
                'beerCans': 98,
                'beerCrates': 12,
                'crates': 6,
                'paperScraps': 24.1,
                'usedOil': 5.0,
                'buckets': 10,
                'glassBottles': 185,
                'battery': 6,
                'totalRevenue': 7500
            },
            {
                'date': '2024-01-27',
                'customer': 'Factory C',
                'clearBottles': 185,
                'mixedPlastic': 33,
                'iron': 49.5,
                'aluminum': 18.2,
                'steelCans': 98,
                'beerCans': 155,
                'beerCrates': 21,
                'crates': 13,
                'paperScraps': 44.7,
                'usedOil': 8.8,
                'buckets': 19,
                'glassBottles': 260,
                'battery': 13,
                'totalRevenue': 11800
            },
            {
                'date': '2024-01-28',
                'customer': 'Factory A',
                'clearBottles': 155,
                'mixedPlastic': 26,
                'iron': 39.4,
                'aluminum': 14.1,
                'steelCans': 78,
                'beerCans': 128,
                'beerCrates': 16,
                'crates': 10,
                'paperScraps': 33.9,
                'usedOil': 7.1,
                'buckets': 14,
                'glassBottles': 208,
                'battery': 9,
                'totalRevenue': 9100
            },
            {
                'date': '2024-01-29',
                'customer': 'Factory B',
                'clearBottles': 178,
                'mixedPlastic': 29,
                'iron': 44.8,
                'aluminum': 16.5,
                'steelCans': 92,
                'beerCans': 138,
                'beerCrates': 19,
                'crates': 11,
                'paperScraps': 37.6,
                'usedOil': 7.6,
                'buckets': 16,
                'glassBottles': 228,
                'battery': 11,
                'totalRevenue': 10200
            },
            {
                'date': '2024-01-30',
                'customer': 'Waste Management Co',
                'clearBottles': 128,
                'mixedPlastic': 21,
                'iron': 31.2,
                'aluminum': 11.2,
                'steelCans': 62,
                'beerCans': 102,
                'beerCrates': 14,
                'crates': 7,
                'paperScraps': 26.8,
                'usedOil': 5.4,
                'buckets': 11,
                'glassBottles': 192,
                'battery': 7,
                'totalRevenue': 7900
            }
        ]
        
        # Sample purchase data
        self.purchase_data = [
            {
                'date': '2024-01-15',
                'registration': '3795',
                'amount': 8000.00,
                'clearBottles': 80,
                'mixedPlastic': 9,
                'iron': 42,
                'aluminum': 9,
                'steelCans': 0,
                'beerCans': 0,
                'beerCrates': 0,
                'crates': 0,
                'paperScraps': 0,
                'usedOil': 0,
                'buckets': 0,
                'glassBottles': 0,
                'battery': 3,
                'supplier': 'Supplier A'
            },
            {
                'date': '2024-01-15',
                'registration': '4906',
                'amount': 8418.00,
                'clearBottles': 78,
                'mixedPlastic': 12,
                'iron': 19,
                'aluminum': 1.5,
                'steelCans': 0,
                'beerCans': 0,
                'beerCrates': 0,
                'crates': 0,
                'paperScraps': 0,
                'usedOil': 0,
                'buckets': 0,
                'glassBottles': 0,
                'battery': 10,
                'supplier': 'Supplier B'
            },
            {
                'date': '2024-01-16',
                'registration': '4349',
                'amount': 8553.00,
                'clearBottles': 65,
                'mixedPlastic': 0,
                'iron': 9,
                'aluminum': 10.5,
                'steelCans': 0,
                'beerCans': 0,
                'beerCrates': 0,
                'crates': 0,
                'paperScraps': 0,
                'usedOil': 0,
                'buckets': 0,
                'glassBottles': 0,
                'battery': 2,
                'supplier': 'Supplier C'
            },
            {
                'date': '2024-01-17',
                'registration': '4348',
                'amount': 8394.00,
                'clearBottles': 47,
                'mixedPlastic': 0,
                'iron': 19,
                'aluminum': 2,
                'steelCans': 0,
                'beerCans': 0,
                'beerCrates': 0,
                'crates': 0,
                'paperScraps': 0,
                'usedOil': 0,
                'buckets': 0,
                'glassBottles': 0,
                'battery': 0,
                'supplier': 'Local Collection'
            },
            {
                'date': '2024-01-18',
                'registration': '4351',
                'amount': 8786.00,
                'clearBottles': 117,
                'mixedPlastic': 0,
                'iron': 28,
                'aluminum': 3.5,
                'steelCans': 0,
                'beerCans': 0,
                'beerCrates': 0,
                'crates': 0,
                'paperScraps': 0,
                'usedOil': 0,
                'buckets': 0,
                'glassBottles': 0,
                'battery': 0,
                'supplier': 'Waste Pickers'
            }
        ]
    
    def analyze_sales_data(self):
        """Analyze sales data and generate insights"""
        if not self.sales_data:
            return {}
        
        df = pd.DataFrame(self.sales_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Basic statistics
        total_revenue = df['totalRevenue'].sum()
        total_transactions = len(df)
        unique_customers = df['customer'].nunique()
        
        # Item analysis
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        item_totals = {}
        for col in item_columns:
            item_totals[col] = df[col].sum()
        
        # Customer analysis
        customer_revenue = df.groupby('customer')['totalRevenue'].sum().to_dict()
        customer_transactions = df['customer'].value_counts().to_dict()
        
        # Daily trends
        daily_revenue = df.groupby('date')['totalRevenue'].sum().to_dict()
        daily_transactions = df.groupby('date').size().to_dict()
        
        # Top performing items
        item_revenue_contribution = {}
        for col in item_columns:
            # Estimate revenue contribution based on quantity (simplified)
            item_revenue_contribution[col] = df[col].sum()
        
        return {
            'total_revenue': total_revenue,
            'total_transactions': total_transactions,
            'unique_customers': unique_customers,
            'item_totals': item_totals,
            'customer_revenue': customer_revenue,
            'customer_transactions': customer_transactions,
            'daily_revenue': daily_revenue,
            'daily_transactions': daily_transactions,
            'item_revenue_contribution': item_revenue_contribution,
            'average_revenue_per_transaction': total_revenue / total_transactions if total_transactions > 0 else 0
        }
    
    def analyze_purchase_data(self):
        """Analyze purchase data and generate insights"""
        if not self.purchase_data:
            return {}
        
        df = pd.DataFrame(self.purchase_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Basic statistics
        total_cost = df['amount'].sum()
        total_purchases = len(df)
        unique_suppliers = df['supplier'].nunique()
        
        # Item analysis
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        item_totals = {}
        for col in item_columns:
            item_totals[col] = df[col].sum()
        
        # Supplier analysis
        supplier_cost = df.groupby('supplier')['amount'].sum().to_dict()
        supplier_purchases = df['supplier'].value_counts().to_dict()
        
        # Daily trends
        daily_cost = df.groupby('date')['amount'].sum().to_dict()
        daily_purchases = df.groupby('date').size().to_dict()
        
        # Registration analysis
        unique_registrations = df['registration'].nunique()
        
        return {
            'total_cost': total_cost,
            'total_purchases': total_purchases,
            'unique_suppliers': unique_suppliers,
            'unique_registrations': unique_registrations,
            'item_totals': item_totals,
            'supplier_cost': supplier_cost,
            'supplier_purchases': supplier_purchases,
            'daily_cost': daily_cost,
            'daily_purchases': daily_purchases,
            'average_cost_per_purchase': total_cost / total_purchases if total_purchases > 0 else 0
        }
    
    def calculate_profit_margin(self):
        """Calculate profit margin and financial insights"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        
        if not sales_analysis or not purchase_analysis:
            return {}
        
        total_revenue = sales_analysis['total_revenue']
        total_cost = purchase_analysis['total_cost']
        
        gross_profit = total_revenue - total_cost
        profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'gross_profit': gross_profit,
            'profit_margin': profit_margin,
            'roi': (gross_profit / total_cost * 100) if total_cost > 0 else 0
        }
    
    def generate_item_insights(self):
        """Generate insights about individual items"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        
        if not sales_analysis or not purchase_analysis:
            return {}
        
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        item_insights = {}
        for item in item_columns:
            sales_qty = sales_analysis['item_totals'].get(item, 0)
            purchase_qty = purchase_analysis['item_totals'].get(item, 0)
            
            # Calculate turnover rate
            turnover_rate = (sales_qty / purchase_qty * 100) if purchase_qty > 0 else 0
            
            # Determine item performance
            if turnover_rate > 80:
                performance = 'Excellent'
            elif turnover_rate > 60:
                performance = 'Good'
            elif turnover_rate > 40:
                performance = 'Fair'
            else:
                performance = 'Poor'
            
            item_insights[item] = {
                'sales_quantity': sales_qty,
                'purchase_quantity': purchase_qty,
                'turnover_rate': turnover_rate,
                'performance': performance
            }
        
        return item_insights
    
    def generate_predictive_analytics(self):
        """Generate comprehensive sales forecasting and predictive insights"""
        if not self.sales_data:
            return {}
        
        df = pd.DataFrame(self.sales_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Create comprehensive time-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['quarter'] = df['date'].dt.quarter
        df['year'] = df['date'].dt.year
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Create lag features for time series analysis
        df['revenue_lag1'] = df['totalRevenue'].shift(1)
        df['revenue_lag2'] = df['totalRevenue'].shift(2)
        df['revenue_lag3'] = df['totalRevenue'].shift(3)
        
        # Create rolling averages
        df['revenue_ma3'] = df['totalRevenue'].rolling(window=3).mean()
        df['revenue_ma7'] = df['totalRevenue'].rolling(window=7).mean()
        
        # Create polynomial features
        df['revenue_squared'] = df['totalRevenue'] ** 2
        df['revenue_cubed'] = df['totalRevenue'] ** 3
        
        # Remove NaN values
        df = df.dropna()
        
        if len(df) < 5:  # Need minimum data for predictions
            return self._generate_basic_predictions(df)
        
        # Prepare features for multiple models
        feature_columns = ['day_of_week', 'month', 'day', 'quarter', 'day_of_year', 
                          'week_of_year', 'revenue_lag1', 'revenue_lag2', 'revenue_lag3',
                          'revenue_ma3', 'revenue_ma7', 'revenue_squared', 'revenue_cubed']
        
        X = df[feature_columns].values
        y = df['totalRevenue'].values
        
        # Split data for validation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train multiple models
        models = self._train_multiple_models(X_train, y_train)
        
        # Evaluate models
        model_evaluations = self._evaluate_models(models, X_test, y_test)
        
        # Get best model
        best_model_name = max(model_evaluations, key=lambda k: model_evaluations[k]['r2_score'])
        best_model = models[best_model_name]
        
        # Generate predictions
        future_predictions = self._generate_future_predictions(df, best_model, feature_columns)
        
        # Advanced trend analysis
        trend_analysis = self._analyze_trends(df)
        
        # Seasonal decomposition
        seasonal_analysis = self._seasonal_decomposition(df)
        
        # Anomaly detection
        anomalies = self._detect_anomalies(df)
        
        # Demand forecasting by item
        item_forecasts = self._forecast_by_item(df)
        
        # Risk assessment
        risk_assessment = self._assess_risks(df, future_predictions)
        
        return {
            'sales_forecast': {
                'next_7_days': future_predictions['next_7_days'],
                'next_30_days': future_predictions['next_30_days'],
                'next_90_days': future_predictions['next_90_days'],
                'trend': trend_analysis['trend'],
                'trend_strength': trend_analysis['trend_strength'],
                'confidence': model_evaluations[best_model_name]['r2_score'],
                'best_model': best_model_name
            },
            'model_performance': model_evaluations,
            'seasonal_analysis': seasonal_analysis,
            'anomaly_detection': anomalies,
            'item_forecasts': item_forecasts,
            'risk_assessment': risk_assessment,
            'trend_analysis': trend_analysis
        }
    
    def _generate_basic_predictions(self, df):
        """Generate basic predictions when limited data is available"""
        if len(df) == 0:
            return {
                'sales_forecast': {
                    'next_7_days': [0] * 7,
                    'trend': 'Unknown',
                    'trend_strength': 0,
                    'confidence': 0
                },
                'seasonal_analysis': {
                    'peak_month': 1,
                    'peak_revenue': 0,
                    'monthly_pattern': {}
                }
            }
        
        # Simple linear regression
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['totalRevenue'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_days = np.arange(len(df), len(df) + 7).reshape(-1, 1)
        future_predictions = model.predict(future_days)
        
        trend = "Increasing" if model.coef_[0] > 0 else "Decreasing"
        
        return {
            'sales_forecast': {
                'next_7_days': future_predictions.tolist(),
                'trend': trend,
                'trend_strength': float(abs(model.coef_[0])),
                'confidence': float(model.score(X, y))
            },
            'seasonal_analysis': {
                'peak_month': int(df['month'].mode().iloc[0]) if len(df) > 0 else 1,
                'peak_revenue': float(df['totalRevenue'].max()) if len(df) > 0 else 0,
                'monthly_pattern': {}
            }
        }
    
    def _train_multiple_models(self, X_train, y_train):
        """Train multiple machine learning models"""
        models = {}
        
        # Linear models
        models['Linear Regression'] = LinearRegression()
        models['Ridge Regression'] = Ridge(alpha=1.0)
        models['Lasso Regression'] = Lasso(alpha=0.1)
        
        # Ensemble models
        models['Random Forest'] = RandomForestRegressor(n_estimators=100, random_state=42)
        models['Gradient Boosting'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        
        # Support Vector Regression
        models['SVR'] = SVR(kernel='rbf', C=1.0, gamma='scale')
        
        # Neural Network
        models['Neural Network'] = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        
        # Train all models
        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
            except Exception as e:
                print(f"Error training {name}: {e}")
                # Remove failed model
                models.pop(name, None)
        
        return models
    
    def _evaluate_models(self, models, X_test, y_test):
        """Evaluate model performance"""
        evaluations = {}
        
        for name, model in models.items():
            try:
                y_pred = model.predict(X_test)
                
                evaluations[name] = {
                    'r2_score': float(r2_score(y_test, y_pred)),
                    'mse': float(mean_squared_error(y_test, y_pred)),
                    'mae': float(mean_absolute_error(y_test, y_pred)),
                    'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred)))
                }
            except Exception as e:
                print(f"Error evaluating {name}: {e}")
                evaluations[name] = {
                    'r2_score': 0,
                    'mse': float('inf'),
                    'mae': float('inf'),
                    'rmse': float('inf')
                }
        
        return evaluations
    
    def _generate_future_predictions(self, df, model, feature_columns):
        """Generate future predictions using the best model"""
        # Create future dates
        last_date = df['date'].max()
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=90, freq='D')
        
        # Create future feature matrix
        future_df = pd.DataFrame({'date': future_dates})
        future_df['day_of_week'] = future_df['date'].dt.dayofweek
        future_df['month'] = future_df['date'].dt.month
        future_df['day'] = future_df['date'].dt.day
        future_df['quarter'] = future_df['date'].dt.quarter
        future_df['year'] = future_df['date'].dt.year
        future_df['day_of_year'] = future_df['date'].dt.dayofyear
        future_df['week_of_year'] = future_df['date'].dt.isocalendar().week
        
        # Use last known values for lag features
        last_revenue = df['totalRevenue'].iloc[-1]
        last_revenue_lag1 = df['totalRevenue'].iloc[-2] if len(df) > 1 else last_revenue
        last_revenue_lag2 = df['totalRevenue'].iloc[-3] if len(df) > 2 else last_revenue_lag1
        
        future_df['revenue_lag1'] = last_revenue
        future_df['revenue_lag2'] = last_revenue_lag1
        future_df['revenue_lag3'] = last_revenue_lag2
        future_df['revenue_ma3'] = df['totalRevenue'].tail(3).mean()
        future_df['revenue_ma7'] = df['totalRevenue'].tail(7).mean()
        future_df['revenue_squared'] = last_revenue ** 2
        future_df['revenue_cubed'] = last_revenue ** 3
        
        # Make predictions
        X_future = future_df[feature_columns].values
        predictions = model.predict(X_future)
        
        return {
            'next_7_days': predictions[:7].tolist(),
            'next_30_days': predictions[:30].tolist(),
            'next_90_days': predictions.tolist()
        }
    
    def _analyze_trends(self, df):
        """Analyze trends in the data"""
        # Linear trend
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['totalRevenue'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        trend = "Increasing" if model.coef_[0] > 0 else "Decreasing"
        trend_strength = abs(model.coef_[0])
        
        # Exponential trend
        log_y = np.log(y + 1)  # Add 1 to avoid log(0)
        exp_model = LinearRegression()
        exp_model.fit(X, log_y)
        exp_trend = "Exponential Growth" if exp_model.coef_[0] > 0 else "Exponential Decay"
        
        # Volatility analysis
        volatility = df['totalRevenue'].std()
        avg_revenue = df['totalRevenue'].mean()
        cv = volatility / avg_revenue if avg_revenue > 0 else 0
        
        return {
            'trend': trend,
            'trend_strength': float(trend_strength),
            'exponential_trend': exp_trend,
            'volatility': float(volatility),
            'coefficient_of_variation': float(cv),
            'trend_confidence': float(model.score(X, y))
        }
    
    def _seasonal_decomposition(self, df):
        """Perform seasonal decomposition analysis"""
        if len(df) < 12:  # Need at least 12 data points for seasonal analysis
            return {
                'peak_month': int(df['month'].mode().iloc[0]) if len(df) > 0 else 1,
                'peak_revenue': float(df['totalRevenue'].max()) if len(df) > 0 else 0,
                'monthly_pattern': {},
                'seasonal_strength': 0
            }
        
        # Monthly patterns
        monthly_revenue = df.groupby('month')['totalRevenue'].agg(['mean', 'std', 'count']).to_dict()
        
        # Weekly patterns
        weekly_revenue = df.groupby('day_of_week')['totalRevenue'].mean().to_dict()
        
        # Find peak periods
        peak_month = df.groupby('month')['totalRevenue'].mean().idxmax()
        peak_day = df.groupby('day_of_week')['totalRevenue'].mean().idxmax()
        
        # Seasonal strength (how much variation is seasonal)
        total_variance = df['totalRevenue'].var()
        seasonal_variance = df.groupby('month')['totalRevenue'].var().mean()
        seasonal_strength = seasonal_variance / total_variance if total_variance > 0 else 0
        
        return {
            'peak_month': int(peak_month),
            'peak_day': int(peak_day),
            'peak_revenue': float(df.groupby('month')['totalRevenue'].mean().max()),
            'monthly_pattern': monthly_revenue,
            'weekly_pattern': weekly_revenue,
            'seasonal_strength': float(seasonal_strength)
        }
    
    def _detect_anomalies(self, df):
        """Detect anomalies in the data"""
        revenue = df['totalRevenue'].values
        
        # Statistical anomaly detection (3-sigma rule)
        mean_revenue = np.mean(revenue)
        std_revenue = np.std(revenue)
        
        upper_bound = mean_revenue + 2 * std_revenue
        lower_bound = mean_revenue - 2 * std_revenue
        
        anomalies = []
        for i, value in enumerate(revenue):
            if value > upper_bound or value < lower_bound:
                anomalies.append({
                    'index': i,
                    'date': df['date'].iloc[i].strftime('%Y-%m-%d'),
                    'value': float(value),
                    'expected_range': [float(lower_bound), float(upper_bound)],
                    'severity': 'high' if abs(value - mean_revenue) > 3 * std_revenue else 'medium'
                })
        
        return {
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'anomaly_rate': len(anomalies) / len(revenue) if len(revenue) > 0 else 0,
            'upper_bound': float(upper_bound),
            'lower_bound': float(lower_bound)
        }
    
    def _forecast_by_item(self, df):
        """Generate forecasts for individual items"""
        if not self.sales_data:
            return {}
        
        item_forecasts = {}
        
        # Get unique items from sales data
        all_items = set()
        for sale in self.sales_data:
            for item, qty in sale.items():
                if item != 'date' and item != 'customer' and item != 'totalRevenue':
                    all_items.add(item)
        
        for item in all_items:
            # Calculate item-specific trends
            item_totals = []
            for sale in self.sales_data:
                item_qty = sale.get(item, 0)
                item_totals.append(item_qty)
            
            if len(item_totals) > 1:
                # Simple trend analysis for each item
                X = np.arange(len(item_totals)).reshape(-1, 1)
                y = np.array(item_totals)
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 7 days
                future_X = np.arange(len(item_totals), len(item_totals) + 7).reshape(-1, 1)
                future_predictions = model.predict(future_X)
                
                item_forecasts[item] = {
                    'trend': "Increasing" if model.coef_[0] > 0 else "Decreasing",
                    'trend_strength': float(abs(model.coef_[0])),
                    'next_7_days': future_predictions.tolist(),
                    'confidence': float(model.score(X, y))
                }
        
        return item_forecasts
    
    def _assess_risks(self, df, future_predictions):
        """Assess risks in future predictions"""
        # Calculate prediction intervals
        revenue_std = df['totalRevenue'].std()
        
        # Risk factors
        risk_factors = {
            'volatility_risk': float(revenue_std / df['totalRevenue'].mean()) if df['totalRevenue'].mean() > 0 else 0,
            'trend_risk': 1 - abs(df['totalRevenue'].corr(pd.Series(range(len(df))))),
            'seasonal_risk': 1 - self._seasonal_decomposition(df)['seasonal_strength'],
            'data_quality_risk': 1 - (len(df) / 30)  # Risk based on data quantity
        }
        
        # Overall risk score
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        
        # Risk levels
        if overall_risk < 0.3:
            risk_level = "Low"
        elif overall_risk < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'overall_risk_score': float(overall_risk),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'prediction_confidence': 1 - overall_risk
        }
    
    def calculate_advanced_metrics(self):
        """Calculate advanced business metrics"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        
        if not sales_analysis or not purchase_analysis:
            return {}
        
        # Inventory turnover rate
        total_sales_qty = sum(sales_analysis['item_totals'].values())
        total_purchase_qty = sum(purchase_analysis['item_totals'].values())
        inventory_turnover = (total_sales_qty / total_purchase_qty) if total_purchase_qty > 0 else 0
        
        # Average transaction value
        avg_transaction_value = sales_analysis['average_revenue_per_transaction']
        
        # Customer acquisition cost (simplified)
        total_customers = sales_analysis['unique_customers']
        total_cost = purchase_analysis['total_cost']
        cac = total_cost / total_customers if total_customers > 0 else 0
        
        # Customer lifetime value (simplified)
        avg_customer_revenue = sales_analysis['total_revenue'] / total_customers if total_customers > 0 else 0
        clv = avg_customer_revenue * 12  # Assume 12 months retention
        
        # Supplier performance score
        supplier_scores = {}
        for supplier, cost in purchase_analysis['supplier_cost'].items():
            # Simple scoring based on cost efficiency
            score = min(100, max(0, 100 - (cost / 1000)))  # Lower cost = higher score
            supplier_scores[supplier] = score
        
        return {
            'inventory_turnover_rate': inventory_turnover,
            'average_transaction_value': avg_transaction_value,
            'customer_acquisition_cost': cac,
            'customer_lifetime_value': clv,
            'supplier_performance_scores': supplier_scores,
            'days_sales_outstanding': 30,  # Placeholder
            'operational_efficiency': 85.5  # Placeholder
        }
    
    def generate_environmental_impact(self):
        """Calculate environmental impact metrics"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        
        if not sales_analysis or not purchase_analysis:
            return {}
        
        # Environmental impact calculations (simplified)
        total_items_recycled = sum(sales_analysis['item_totals'].values())
        
        # Carbon footprint reduction (kg CO2 equivalent)
        # Rough estimates: 1kg of recycled material saves ~2kg CO2
        carbon_saved = total_items_recycled * 2
        
        # Waste diversion rate
        total_waste_processed = sum(purchase_analysis['item_totals'].values())
        diversion_rate = (total_items_recycled / total_waste_processed * 100) if total_waste_processed > 0 else 0
        
        # Water savings (liters)
        water_saved = total_items_recycled * 100  # Rough estimate
        
        # Energy savings (kWh)
        energy_saved = total_items_recycled * 5  # Rough estimate
        
        return {
            'total_items_recycled': total_items_recycled,
            'carbon_footprint_reduction': carbon_saved,
            'waste_diversion_rate': diversion_rate,
            'water_savings_liters': water_saved,
            'energy_savings_kwh': energy_saved,
            'environmental_score': min(100, diversion_rate)
        }
    
    def generate_market_analysis(self):
        """Generate market and competitive analysis"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        
        if not sales_analysis or not purchase_analysis:
            return {}
        
        # Market share analysis (simplified)
        total_market_size = 1000000  # Placeholder - total market in THB
        market_share = (sales_analysis['total_revenue'] / total_market_size) * 100
        
        # Price analysis
        avg_price_per_item = sales_analysis['total_revenue'] / sum(sales_analysis['item_totals'].values()) if sum(sales_analysis['item_totals'].values()) > 0 else 0
        
        # Growth rate
        # This would normally compare current period vs previous period
        growth_rate = 15.5  # Placeholder percentage
        
        # Competitive positioning
        competitive_advantages = [
            "Diverse item portfolio",
            "Strong supplier network",
            "Efficient processing",
            "Quality control"
        ]
        
        return {
            'market_share_percentage': market_share,
            'average_price_per_item': avg_price_per_item,
            'growth_rate': growth_rate,
            'competitive_advantages': competitive_advantages,
            'market_position': "Market Leader" if market_share > 10 else "Established Player"
        }
    
    def generate_advanced_analytics(self):
        """Generate advanced analytics and insights"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        financial_analysis = self.calculate_profit_margin()
        item_insights = self.generate_item_insights()
        
        # Profitability by item analysis
        profitability_by_item = self.calculate_item_profitability()
        
        # Sales forecasting
        sales_forecast = self.generate_sales_forecast()
        
        # Seasonal analysis
        seasonal_analysis = self.analyze_seasonal_patterns()
        
        # Customer analysis
        customer_analysis = self.analyze_customer_behavior()
        
        # Supplier analysis
        supplier_analysis = self.analyze_supplier_performance()
        
        # Inventory optimization
        inventory_optimization = self.optimize_inventory_levels()
        
        # Performance metrics
        performance_metrics = self.calculate_performance_metrics()
        
        return {
            'profitability_by_item': profitability_by_item,
            'sales_forecast': sales_forecast,
            'seasonal_analysis': seasonal_analysis,
            'customer_analysis': customer_analysis,
            'supplier_analysis': supplier_analysis,
            'inventory_optimization': inventory_optimization,
            'performance_metrics': performance_metrics
        }
    
    def calculate_item_profitability(self):
        """Calculate profitability metrics for each item"""
        if not self.sales_data or not self.purchase_data:
            return {}
        
        sales_df = pd.DataFrame(self.sales_data)
        purchase_df = pd.DataFrame(self.purchase_data)
        
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        profitability = {}
        for item in item_columns:
            # Calculate average revenue per unit (simplified)
            total_sales_qty = sales_df[item].sum()
            total_revenue = sales_df['totalRevenue'].sum()
            avg_revenue_per_unit = total_revenue / total_sales_qty if total_sales_qty > 0 else 0
            
            # Calculate average cost per unit (simplified)
            total_purchase_qty = purchase_df[item].sum()
            total_cost = purchase_df['amount'].sum()
            avg_cost_per_unit = total_cost / total_purchase_qty if total_purchase_qty > 0 else 0
            
            # Calculate profit margin
            profit_margin = ((avg_revenue_per_unit - avg_cost_per_unit) / avg_revenue_per_unit * 100) if avg_revenue_per_unit > 0 else 0
            
            # Calculate ROI
            roi = ((avg_revenue_per_unit - avg_cost_per_unit) / avg_cost_per_unit * 100) if avg_cost_per_unit > 0 else 0
            
            profitability[item] = {
                'avg_revenue_per_unit': avg_revenue_per_unit,
                'avg_cost_per_unit': avg_cost_per_unit,
                'profit_margin': profit_margin,
                'roi': roi,
                'total_sales_qty': total_sales_qty,
                'total_purchase_qty': total_purchase_qty,
                'profitability_score': self.calculate_profitability_score(profit_margin, roi)
            }
        
        return profitability
    
    def calculate_profitability_score(self, profit_margin, roi):
        """Calculate a profitability score from 0-100"""
        # Weight profit margin 60% and ROI 40%
        score = (profit_margin * 0.6) + (min(roi, 100) * 0.4)
        return max(0, min(100, score))
    
    def generate_sales_forecast(self):
        """Generate sales forecast for next 30 days"""
        if not self.sales_data:
            return {}
        
        df = pd.DataFrame(self.sales_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate daily average revenue
        daily_avg_revenue = df['totalRevenue'].mean()
        
        # Calculate growth trend (simplified)
        df_sorted = df.sort_values('date')
        if len(df_sorted) > 1:
            first_revenue = df_sorted.iloc[0]['totalRevenue']
            last_revenue = df_sorted.iloc[-1]['totalRevenue']
            growth_rate = (last_revenue - first_revenue) / first_revenue if first_revenue > 0 else 0
        else:
            growth_rate = 0
        
        # Generate forecast for next 30 days
        forecast = []
        current_date = df['date'].max() + pd.Timedelta(days=1)
        
        for i in range(30):
            forecast_revenue = daily_avg_revenue * (1 + growth_rate * (i / 30))
            forecast.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'predicted_revenue': forecast_revenue,
                'confidence': max(0.7, 1 - (i * 0.01))  # Decreasing confidence over time
            })
            current_date += pd.Timedelta(days=1)
        
        return {
            'forecast_data': forecast,
            'daily_avg_revenue': daily_avg_revenue,
            'growth_rate': growth_rate,
            'total_forecast_revenue': sum(f['predicted_revenue'] for f in forecast)
        }
    
    def analyze_seasonal_patterns(self):
        """Analyze seasonal patterns in the data"""
        if not self.sales_data:
            return {}
        
        df = pd.DataFrame(self.sales_data)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        
        # Monthly patterns
        monthly_revenue = df.groupby('month')['totalRevenue'].sum().to_dict()
        monthly_avg = df.groupby('month')['totalRevenue'].mean().to_dict()
        
        # Day of week patterns
        dow_revenue = df.groupby('day_of_week')['totalRevenue'].sum().to_dict()
        dow_avg = df.groupby('day_of_week')['totalRevenue'].mean().to_dict()
        
        # Identify peak months
        peak_month = max(monthly_revenue, key=monthly_revenue.get) if monthly_revenue else None
        peak_day = max(dow_revenue, key=dow_revenue.get) if dow_revenue else None
        
        return {
            'monthly_revenue': monthly_revenue,
            'monthly_average': monthly_avg,
            'day_of_week_revenue': dow_revenue,
            'day_of_week_average': dow_avg,
            'peak_month': peak_month,
            'peak_day': peak_day,
            'seasonality_score': self.calculate_seasonality_score(monthly_revenue)
        }
    
    def calculate_seasonality_score(self, monthly_revenue):
        """Calculate how seasonal the data is (0-100)"""
        if not monthly_revenue or len(monthly_revenue) < 2:
            return 0
        
        values = list(monthly_revenue.values())
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        # Higher standard deviation = more seasonal
        seasonality_score = min(100, (std_dev / mean_val) * 100) if mean_val > 0 else 0
        return seasonality_score
    
    def analyze_customer_behavior(self):
        """Analyze customer behavior patterns"""
        if not self.sales_data:
            return {}
        
        df = pd.DataFrame(self.sales_data)
        
        # Customer frequency analysis
        customer_frequency = df['customer'].value_counts().to_dict()
        
        # Customer value analysis
        customer_value = df.groupby('customer')['totalRevenue'].sum().to_dict()
        customer_avg_value = df.groupby('customer')['totalRevenue'].mean().to_dict()
        
        # Customer preferences (top items per customer)
        customer_preferences = {}
        for customer in df['customer'].unique():
            customer_data = df[df['customer'] == customer]
            item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                           'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                           'buckets', 'glassBottles', 'battery']
            
            preferences = {}
            for item in item_columns:
                preferences[item] = customer_data[item].sum()
            
            # Get top 3 items
            top_items = sorted(preferences.items(), key=lambda x: x[1], reverse=True)[:3]
            customer_preferences[customer] = top_items
        
        # Customer loyalty score
        loyalty_scores = {}
        for customer in customer_value:
            frequency = customer_frequency.get(customer, 0)
            value = customer_value.get(customer, 0)
            avg_value = customer_avg_value.get(customer, 0)
            
            # Simple loyalty score based on frequency and value
            loyalty_score = min(100, (frequency * 20) + (avg_value / 100))
            loyalty_scores[customer] = loyalty_score
        
        return {
            'customer_frequency': customer_frequency,
            'customer_value': customer_value,
            'customer_avg_value': customer_avg_value,
            'customer_preferences': customer_preferences,
            'loyalty_scores': loyalty_scores,
            'top_customers': sorted(customer_value.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def analyze_supplier_performance(self):
        """Analyze supplier performance metrics"""
        if not self.purchase_data:
            return {}
        
        df = pd.DataFrame(self.purchase_data)
        
        # Supplier cost analysis
        supplier_cost = df.groupby('supplier')['amount'].sum().to_dict()
        supplier_avg_cost = df.groupby('supplier')['amount'].mean().to_dict()
        supplier_frequency = df['supplier'].value_counts().to_dict()
        
        # Supplier reliability (based on consistency of purchases)
        supplier_reliability = {}
        for supplier in df['supplier'].unique():
            supplier_data = df[df['supplier'] == supplier]
            frequency = len(supplier_data)
            avg_amount = supplier_data['amount'].mean()
            std_amount = supplier_data['amount'].std()
            
            # Reliability score based on consistency
            consistency = 1 - (std_amount / avg_amount) if avg_amount > 0 else 0
            reliability_score = min(100, (frequency * 10) + (consistency * 50))
            supplier_reliability[supplier] = reliability_score
        
        # Supplier quality (based on item variety)
        supplier_quality = {}
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        for supplier in df['supplier'].unique():
            supplier_data = df[df['supplier'] == supplier]
            item_variety = sum(1 for item in item_columns if supplier_data[item].sum() > 0)
            quality_score = min(100, item_variety * 7.7)  # 13 items max = 100 score
            supplier_quality[supplier] = quality_score
        
        return {
            'supplier_cost': supplier_cost,
            'supplier_avg_cost': supplier_avg_cost,
            'supplier_frequency': supplier_frequency,
            'supplier_reliability': supplier_reliability,
            'supplier_quality': supplier_quality,
            'top_suppliers': sorted(supplier_cost.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def optimize_inventory_levels(self):
        """Optimize inventory levels based on sales patterns"""
        if not self.sales_data or not self.purchase_data:
            return {}
        
        sales_df = pd.DataFrame(self.sales_data)
        purchase_df = pd.DataFrame(self.purchase_data)
        
        item_columns = ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                       'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                       'buckets', 'glassBottles', 'battery']
        
        inventory_recommendations = {}
        for item in item_columns:
            # Calculate daily sales rate
            total_sales = sales_df[item].sum()
            days_of_data = len(sales_df)
            daily_sales_rate = total_sales / days_of_data if days_of_data > 0 else 0
            
            # Calculate safety stock (20% of daily sales for 7 days)
            safety_stock = daily_sales_rate * 7 * 0.2
            
            # Calculate reorder point (7 days of sales + safety stock)
            reorder_point = daily_sales_rate * 7 + safety_stock
            
            # Calculate optimal order quantity (14 days of sales)
            optimal_order_qty = daily_sales_rate * 14
            
            # Calculate current inventory (simplified - purchase - sales)
            total_purchased = purchase_df[item].sum()
            current_inventory = total_purchased - total_sales
            
            # Determine action needed
            if current_inventory <= reorder_point:
                action = 'Reorder'
                urgency = 'High' if current_inventory <= safety_stock else 'Medium'
            else:
                action = 'Hold'
                urgency = 'Low'
            
            inventory_recommendations[item] = {
                'daily_sales_rate': daily_sales_rate,
                'safety_stock': safety_stock,
                'reorder_point': reorder_point,
                'optimal_order_qty': optimal_order_qty,
                'current_inventory': current_inventory,
                'action': action,
                'urgency': urgency,
                'days_of_inventory': current_inventory / daily_sales_rate if daily_sales_rate > 0 else 0
            }
        
        return inventory_recommendations
    
    def calculate_performance_metrics(self):
        """Calculate key performance indicators"""
        if not self.sales_data or not self.purchase_data:
            return {}
        
        sales_df = pd.DataFrame(self.sales_data)
        purchase_df = pd.DataFrame(self.purchase_data)
        
        # Inventory turnover rate
        total_sales_qty = sum(sales_df[col].sum() for col in ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                                                             'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                                                             'buckets', 'glassBottles', 'battery'])
        total_purchase_qty = sum(purchase_df[col].sum() for col in ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                                                                   'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                                                                   'buckets', 'glassBottles', 'battery'])
        
        avg_inventory = (total_purchase_qty - total_sales_qty) / 2 if total_purchase_qty > total_sales_qty else 0
        inventory_turnover = total_sales_qty / avg_inventory if avg_inventory > 0 else 0
        
        # Days sales outstanding (simplified)
        total_revenue = sales_df['totalRevenue'].sum()
        days_of_data = len(sales_df)
        daily_revenue = total_revenue / days_of_data if days_of_data > 0 else 0
        dso = 30  # Simplified assumption
        
        # Customer acquisition cost (simplified)
        total_cost = purchase_df['amount'].sum()
        unique_customers = sales_df['customer'].nunique()
        cac = total_cost / unique_customers if unique_customers > 0 else 0
        
        # Customer lifetime value (simplified)
        avg_customer_revenue = total_revenue / unique_customers if unique_customers > 0 else 0
        clv = avg_customer_revenue * 12  # Assume 12 months retention
        
        return {
            'inventory_turnover': inventory_turnover,
            'days_sales_outstanding': dso,
            'customer_acquisition_cost': cac,
            'customer_lifetime_value': clv,
            'avg_customer_revenue': avg_customer_revenue,
            'total_sales_quantity': total_sales_qty,
            'total_purchase_quantity': total_purchase_qty,
            'avg_inventory': avg_inventory
        }
    
    def generate_profit_margin_data(self):
        """Generate profit margin data for charts"""
        profit_margin_data = {}
        
        # Calculate profit margins for each item
        for item in ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                    'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                    'buckets', 'glassBottles', 'battery']:
            total_revenue = sum(sale.get(item, 0) * self.get_item_price(item) for sale in self.sales_data)
            total_cost = sum(sale.get(item, 0) * self.get_item_cost(item) for sale in self.sales_data)
            
            if total_revenue > 0:
                profit_margin = ((total_revenue - total_cost) / total_revenue) * 100
            else:
                profit_margin = 0
                
            profit_margin_data[item] = {
                'revenue': total_revenue,
                'cost': total_cost,
                'profit': total_revenue - total_cost,
                'margin': profit_margin
            }
        
        return profit_margin_data
    
    def generate_growth_rate_data(self):
        """Generate growth rate data for charts"""
        daily_revenue = {}
        
        # Calculate daily revenue
        for sale in self.sales_data:
            date = sale['date']
            if date not in daily_revenue:
                daily_revenue[date] = 0
            daily_revenue[date] += sale['totalRevenue']
        
        # Calculate growth rates
        dates = sorted(daily_revenue.keys())
        growth_rates = {}
        
        for i in range(1, len(dates)):
            current_revenue = daily_revenue[dates[i]]
            previous_revenue = daily_revenue[dates[i-1]]
            
            if previous_revenue > 0:
                growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100
            else:
                growth_rate = 0
                
            growth_rates[dates[i]] = growth_rate
        
        return {
            'daily_revenue': daily_revenue,
            'growth_rates': growth_rates,
            'avg_growth_rate': np.mean(list(growth_rates.values())) if growth_rates else 0
        }
    
    def generate_inventory_turnover_data(self):
        """Generate inventory turnover data for charts"""
        turnover_data = {}
        
        for item in ['clearBottles', 'mixedPlastic', 'iron', 'aluminum', 'steelCans', 
                    'beerCans', 'beerCrates', 'crates', 'paperScraps', 'usedOil', 
                    'buckets', 'glassBottles', 'battery']:
            # Calculate total quantity sold
            total_quantity = sum(sale.get(item, 0) for sale in self.sales_data)
            
            # Estimate average inventory (simplified calculation)
            avg_inventory = total_quantity * 0.3  # Assume 30% of total sales as average inventory
            
            if avg_inventory > 0:
                turnover_rate = total_quantity / avg_inventory
            else:
                turnover_rate = 0
                
            turnover_data[item] = {
                'total_quantity': total_quantity,
                'avg_inventory': avg_inventory,
                'turnover_rate': turnover_rate
            }
        
        return turnover_data
    
    def generate_cash_flow_data(self):
        """Generate cash flow data for charts"""
        daily_revenue = {}
        daily_cost = {}
        
        # Calculate daily revenue
        for sale in self.sales_data:
            date = sale['date']
            if date not in daily_revenue:
                daily_revenue[date] = 0
            daily_revenue[date] += sale['totalRevenue']
        
        # Calculate daily cost
        for purchase in self.purchase_data:
            date = purchase['date']
            if date not in daily_cost:
                daily_cost[date] = 0
            daily_cost[date] += purchase['amount']
        
        # Calculate cumulative cash flow
        dates = sorted(set(list(daily_revenue.keys()) + list(daily_cost.keys())))
        cumulative_cash_flow = {}
        running_total = 0
        
        for date in dates:
            revenue = daily_revenue.get(date, 0)
            cost = daily_cost.get(date, 0)
            net_cash_flow = revenue - cost
            running_total += net_cash_flow
            cumulative_cash_flow[date] = running_total
        
        return {
            'daily_revenue': daily_revenue,
            'daily_cost': daily_cost,
            'daily_net_cash_flow': {date: daily_revenue.get(date, 0) - daily_cost.get(date, 0) for date in dates},
            'cumulative_cash_flow': cumulative_cash_flow
        }
    
    def generate_daily_heatmap_data(self):
        """Generate daily heatmap data for charts"""
        daily_revenue = {}
        
        # Calculate daily revenue
        for sale in self.sales_data:
            date = sale['date']
            if date not in daily_revenue:
                daily_revenue[date] = 0
            daily_revenue[date] += sale['totalRevenue']
        
        # Create heatmap data structure
        heatmap_data = {}
        for date, revenue in daily_revenue.items():
            dt = datetime.strptime(date, '%Y-%m-%d')
            day_of_week = dt.weekday()  # 0=Monday, 6=Sunday
            week_number = dt.isocalendar()[1]
            
            if week_number not in heatmap_data:
                heatmap_data[week_number] = {}
            heatmap_data[week_number][day_of_week] = revenue
        
        return {
            'daily_revenue': daily_revenue,
            'heatmap_data': heatmap_data,
            'max_revenue': max(daily_revenue.values()) if daily_revenue else 0
        }
    
    def generate_dashboard_data(self):
        """Generate comprehensive dashboard data"""
        sales_analysis = self.analyze_sales_data()
        purchase_analysis = self.analyze_purchase_data()
        financial_analysis = self.calculate_profit_margin()
        item_insights = self.generate_item_insights()
        predictive_analytics = self.generate_predictive_analytics()
        advanced_metrics = self.calculate_advanced_metrics()
        environmental_impact = self.generate_environmental_impact()
        market_analysis = self.generate_market_analysis()
        
        # Prepare chart data
        chart_data = {
            'daily_revenue': sales_analysis.get('daily_revenue', {}),
            'daily_cost': purchase_analysis.get('daily_cost', {}),
            'customer_revenue': sales_analysis.get('customer_revenue', {}),
            'supplier_cost': purchase_analysis.get('supplier_cost', {}),
            'item_performance': item_insights,
            'sales_forecast': predictive_analytics.get('sales_forecast', {}),
            'monthly_pattern': predictive_analytics.get('seasonal_analysis', {}).get('monthly_pattern', {}),
            'profit_margin_data': self.generate_profit_margin_data(),
            'growth_rate_data': self.generate_growth_rate_data(),
            'inventory_turnover_data': self.generate_inventory_turnover_data(),
            'cash_flow_data': self.generate_cash_flow_data(),
            'daily_heatmap_data': self.generate_daily_heatmap_data()
        }
        
        # Prepare summary statistics
        summary_stats = {
            'total_revenue': financial_analysis.get('total_revenue', 0),
            'total_cost': financial_analysis.get('total_cost', 0),
            'gross_profit': financial_analysis.get('gross_profit', 0),
            'profit_margin': financial_analysis.get('profit_margin', 0),
            'total_transactions': sales_analysis.get('total_transactions', 0),
            'total_purchases': purchase_analysis.get('total_purchases', 0),
            'unique_customers': sales_analysis.get('unique_customers', 0),
            'unique_suppliers': purchase_analysis.get('unique_suppliers', 0),
            'unique_registrations': purchase_analysis.get('unique_registrations', 0)
        }
        
        return {
            'summary_stats': summary_stats,
            'chart_data': chart_data,
            'sales_analysis': sales_analysis,
            'purchase_analysis': purchase_analysis,
            'financial_analysis': financial_analysis,
            'item_insights': item_insights,
            'predictive_analytics': predictive_analytics,
            'advanced_metrics': advanced_metrics,
            'environmental_impact': environmental_impact,
            'market_analysis': market_analysis
        }
    
    def export_json_for_dashboard(self):
        """Export data in JSON format for dashboard consumption"""
        dashboard_data = self.generate_dashboard_data()
        
        # Convert datetime objects to strings for JSON serialization
        def convert_datetime(obj):
            if isinstance(obj, dict):
                return {str(k): convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            elif isinstance(obj, (datetime, pd.Timestamp)):
                return obj.isoformat()
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            else:
                return obj
        
        dashboard_data = convert_datetime(dashboard_data)
        
        # Save to JSON file
        with open('../html_dashboards/recycled_items_dashboard_data.json', 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, ensure_ascii=False, indent=2, default=str)
        
        print("✅ Recycled items dashboard data exported successfully!")
        return dashboard_data

def main():
    """Main function to run the analyzer"""
    print("🔄 Starting Recycled Items Analysis...")
    
    analyzer = RecycledItemsAnalyzer()
    analyzer.load_sample_data()
    
    print("📊 Analyzing sales data...")
    sales_analysis = analyzer.analyze_sales_data()
    print(f"   - Total Revenue: ฿{sales_analysis['total_revenue']:,.2f}")
    print(f"   - Total Transactions: {sales_analysis['total_transactions']}")
    print(f"   - Unique Customers: {sales_analysis['unique_customers']}")
    
    print("📥 Analyzing purchase data...")
    purchase_analysis = analyzer.analyze_purchase_data()
    print(f"   - Total Cost: ฿{purchase_analysis['total_cost']:,.2f}")
    print(f"   - Total Purchases: {purchase_analysis['total_purchases']}")
    print(f"   - Unique Suppliers: {purchase_analysis['unique_suppliers']}")
    
    print("💰 Calculating financial metrics...")
    financial_analysis = analyzer.calculate_profit_margin()
    print(f"   - Gross Profit: ฿{financial_analysis['gross_profit']:,.2f}")
    print(f"   - Profit Margin: {financial_analysis['profit_margin']:.1f}%")
    print(f"   - ROI: {financial_analysis['roi']:.1f}%")
    
    print("📈 Generating item insights...")
    item_insights = analyzer.generate_item_insights()
    print(f"   - Items Analyzed: {len(item_insights)}")
    
    print("🔮 Generating predictive analytics...")
    predictive_analytics = analyzer.generate_predictive_analytics()
    print(f"   - Sales Trend: {predictive_analytics.get('sales_forecast', {}).get('trend', 'Unknown')}")
    print(f"   - Best Model: {predictive_analytics.get('sales_forecast', {}).get('best_model', 'Unknown')}")
    print(f"   - Confidence: {predictive_analytics.get('sales_forecast', {}).get('confidence', 0):.2f}")
    print(f"   - Anomalies Detected: {predictive_analytics.get('anomaly_detection', {}).get('anomaly_count', 0)}")
    print(f"   - Risk Level: {predictive_analytics.get('risk_assessment', {}).get('risk_level', 'Unknown')}")
    
    print("📊 Calculating advanced metrics...")
    advanced_metrics = analyzer.calculate_advanced_metrics()
    print(f"   - Inventory Turnover: {advanced_metrics.get('inventory_turnover_rate', 0):.2f}")
    
    print("🌱 Calculating environmental impact...")
    environmental_impact = analyzer.generate_environmental_impact()
    print(f"   - Carbon Saved: {environmental_impact.get('carbon_footprint_reduction', 0):.0f} kg CO2")
    
    print("🏭 Generating market analysis...")
    market_analysis = analyzer.generate_market_analysis()
    print(f"   - Market Share: {market_analysis.get('market_share_percentage', 0):.2f}%")
    
    print("💾 Exporting dashboard data...")
    dashboard_data = analyzer.export_json_for_dashboard()
    
    print("✅ Recycled Items Analysis Complete!")
    return dashboard_data

if __name__ == "__main__":
    main()
