"""Data preprocessing for ML models."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple

def prepare_project_data(projects: list) -> pd.DataFrame:
    """Convert project list to DataFrame for ML processing."""
    data = []
    
    for project in projects:
        # Calculate derived features
        fund_utilization = (
            (project.actual_expenditure / project.estimated_cost * 100)
            if project.estimated_cost > 0
            else 0
        )
        
        # Calculate delay days
        if project.expected_completion_date:
            from datetime import datetime
            delay_days = max(0, (datetime.utcnow() - project.expected_completion_date).days)
        else:
            delay_days = 0
        
        # Number of payments
        num_payments = len(project.payments) if hasattr(project, 'payments') else 0
        
        data.append({
            'project_id': project.id,
            'estimated_cost': project.estimated_cost,
            'sanctioned_amount': project.sanctioned_amount,
            'actual_expenditure': project.actual_expenditure,
            'amount_released': project.amount_released,
            'progress_percentage': project.progress_percentage,
            'fund_utilization': fund_utilization,
            'delay_days': delay_days,
            'num_payments': num_payments,
        })
    
    return pd.DataFrame(data)


def scale_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, StandardScaler]:
    """Scale numerical features using StandardScaler."""
    scaler = StandardScaler()
    feature_columns = [
        'estimated_cost',
        'sanctioned_amount',
        'actual_expenditure',
        'amount_released',
        'progress_percentage',
        'fund_utilization',
        'delay_days',
        'num_payments',
    ]
    
    df_scaled = df.copy()
    df_scaled[feature_columns] = scaler.fit_transform(df[feature_columns])
    
    return df_scaled, scaler


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in the dataset."""
    df_clean = df.copy()
    
    # Fill numerical columns with mean
    numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
    
    return df_clean
