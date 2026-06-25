import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
 
EXCEL_FILE = r"inventory.xlsx"

# LOAD DATA
 
@st.cache_data
def load_data():
 
    df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
 
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"])
    df["Manufacturing_Date"] = pd.to_datetime(df["Manufacturing_Date"])
 
    today = pd.Timestamp.today()
 
    df["Days_To_Expiry"] = (
        df["Expiry_Date"] - today
    ).dt.days
 
    conditions = [
        df["Days_To_Expiry"] < 0,
        df["Quantity"] <= df["Min_Stock"],
        df["Days_To_Expiry"] <= 60
    ]
 
    choices = [
        "🔴 Expired",
        "🟠 Low Stock",
        "🟡 Expiring Soon"
    ]
 
    df["Status"] = np.select(
        conditions,
        choices,
        default="🟢 Healthy"
    )
 
    df.insert(
        0,
        "Inventory_ID",
        range(1001, 1001 + len(df))
    )
 
    return df
 
 
# ALERTS
 
@st.cache_data
def get_inventory_alerts(df):
 
    low_stock_df = df[
        df["Quantity"] <= df["Min_Stock"]
    ]
 
    expiring_df = df[
        (df["Days_To_Expiry"] >= 0)
        &
        (df["Days_To_Expiry"] <= 60)
    ]
 
    expired_df = df[
        df["Days_To_Expiry"] < 0
    ]
 
    return (
        low_stock_df,
        expiring_df,
        expired_df
    )
 
 
# FORMATTING
 
def format_currency(value):
 
    if value >= 1_000_000_000:
        return f"₹ {value/1_000_000_000:.1f}B"
 
    elif value >= 1_000_000:
        return f"₹ {value/1_000_000:.1f}M"
 
    elif value >= 1_000:
        return f"₹ {value/1_000:.1f}K"
 
    return f"₹ {value:.0f}"
 
 
# FILTERS
 
def apply_filters(
    df,
    selected_category,
    selected_supplier,
    stock_status,
    expiry_status
):
 
    filtered_df = df.copy()
 
    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]
 
    if selected_supplier != "All":
        filtered_df = filtered_df[
            filtered_df["Supplier"] == selected_supplier
        ]
 
    if stock_status == "Low Stock":
        filtered_df = filtered_df[
            filtered_df["Quantity"] <= filtered_df["Min_Stock"]
        ]
 
    elif stock_status == "Healthy Stock":
        filtered_df = filtered_df[
            filtered_df["Quantity"] > filtered_df["Min_Stock"]
        ]
 
    if expiry_status == "Expired":
        filtered_df = filtered_df[
            filtered_df["Days_To_Expiry"] < 0
        ]
 
    elif expiry_status == "Expiring Soon":
        filtered_df = filtered_df[
            (filtered_df["Days_To_Expiry"] >= 0)
            &
            (filtered_df["Days_To_Expiry"] <= 60)
        ]
 
    elif expiry_status == "Safe":
        filtered_df = filtered_df[
            filtered_df["Days_To_Expiry"] > 60
        ]
 
    return filtered_df
 
 
# KPI CALCULATIONS
 
@st.cache_data
def calculate_kpis(filtered_df):
 
    total_items = len(filtered_df)
 
    inventory_value = (
        filtered_df["Total_Value"].sum()
    )
 
    low_stock = (
        filtered_df["Quantity"]
        <= filtered_df["Min_Stock"]
    ).sum()
 
    expiring = (
        (filtered_df["Days_To_Expiry"] >= 0)
        &
        (filtered_df["Days_To_Expiry"] <= 60)
    ).sum()
 
    expired = (
        filtered_df["Days_To_Expiry"] < 0
    ).sum()
 
    healthy_items = (
        (filtered_df["Quantity"] > filtered_df["Min_Stock"])
        &
        (filtered_df["Days_To_Expiry"] > 60)
    ).sum()
 
    return {
        "total_items": int(total_items),
        "inventory_value": float(inventory_value),
        "low_stock": int(low_stock),
        "expiring": int(expiring),
        "expired": int(expired),
        "healthy_items": int(healthy_items)
    }
 
 
# CHART DATA
 
@st.cache_data
def get_chart_data(filtered_df):
 
    category_chart = (
        filtered_df
        .groupby("Category")["Quantity"]
        .sum()
        .reset_index()
    )
 
    supplier_value = (
        filtered_df
        .groupby("Supplier")["Total_Value"]
        .sum()
        .reset_index()
    )
 
    return category_chart, supplier_value
 
 
@st.cache_data
def get_expiry_data(filtered_df):
 
    return (
        filtered_df
        .groupby("Category")["Days_To_Expiry"]
        .mean()
        .reset_index()
    )
 
 
# HEALTH SCORE
 
def calculate_health_score(
    total_items,
    low_stock,
    expired
):
 
    if total_items == 0:
        return 0
 
    return max(
        0,
        100
        - ((low_stock / total_items) * 100)
        - ((expired / total_items) * 100)
    )
 
 
# REORDER RECOMMENDATIONS
 
@st.cache_data
def get_reorder_recommendations(filtered_df):
 
    reorder_df = filtered_df[
        filtered_df["Quantity"] <= filtered_df["Min_Stock"]
    ].copy()
 
    if not reorder_df.empty:
 
        reorder_df["Recommended_Order"] = (
            reorder_df["Min_Stock"] * 2
            - reorder_df["Quantity"]
        )
 
    return reorder_df
 
 
# TOP MEDICINES
 
@st.cache_data
def get_top10_medicines(filtered_df):
 
    return (
        filtered_df
        .sort_values(
            "Total_Value",
            ascending=False
        )
        .head(10)
    )
 
 
# SUPPLIER SUMMARY
 
@st.cache_data
def get_supplier_summary(filtered_df):
 
    return (
        filtered_df
        .groupby("Supplier")
        .agg(
            Total_Inventory=("Quantity", "sum"),
            Inventory_Value=("Total_Value", "sum"),
            Product_Count=("Medicine", "count")
        )
        .reset_index()
    )
 
 
# DATABASE VIEW
 
@st.cache_data
def prepare_database_view(filtered_df):
 
    db_df = filtered_df.copy()
 
    db_df["Expiry_Date"] = (
        db_df["Expiry_Date"]
        .dt.strftime("%d-%m-%Y")
    )
 
    db_df["Stock_Percentage"] = (
        db_df["Quantity"]
        / db_df["Min_Stock"]
        * 100
    ).round(1)
 
    return db_df[
        [
            "Inventory_ID",
            "Medicine",
            "Category",
            "Supplier",
            "Quantity",
            "Min_Stock",
            "Stock_Percentage",
            "Unit_Price",
            "Total_Value",
            "Expiry_Date",
            "Status"
        ]
    ]
 
 
# CSV EXPORT
 
def generate_csv(filtered_df):
 
    return (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )
