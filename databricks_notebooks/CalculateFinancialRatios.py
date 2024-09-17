# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

# COMMAND ----------

# Create a Spark session
spark = SparkSession.builder.appName("CalculateFinancialRatios").getOrCreate()

# COMMAND ----------

# Function to calculate financial ratios
def calculate_financial_ratios(df):
    return df.withColumns({
        # Profitability Ratios
        "gross_margin_ratio": col("grossProfit") / col("totalRevenue"),
        "net_profit_margin": col("netIncome") / col("totalRevenue"),
        "return_on_assets": col("netIncome") / col("totalAssets"),
        "return_on_equity": col("netIncome") / col("totalShareholderEquity"),
        
        # Liquidity Ratios
        "current_ratio": col("totalCurrentAssets") / col("totalCurrentLiabilities"),
        "quick_ratio": (col("totalCurrentAssets") - col("inventory")) / col("totalCurrentLiabilities"),
        
        # Solvency Ratios
        "debt_to_equity_ratio": col("totalLiabilities") / col("totalShareholderEquity"),
        "interest_coverage_ratio": col("ebit") / col("interestExpense"),
        
        # Efficiency Ratios
        "asset_turnover_ratio": col("totalRevenue") / col("totalAssets"),
        "inventory_turnover_ratio": col("costOfRevenue") / col("inventory"),
        
        # Valuation Ratios
        "price_to_earnings_ratio": col("marketCap") / col("netIncome"),
        "price_to_book_ratio": col("marketCap") / col("totalShareholderEquity")
    })

# COMMAND ----------

# Read the company financials data
company_symbol = dbutils.widgets.get("company_symbol")
financials_df = spark.read.parquet(f"/mnt/staging/company-financials/{company_symbol}")

# COMMAND ----------

# Calculate financial ratios
ratios_df = calculate_financial_ratios(financials_df)

# COMMAND ----------

# Write the results to the gold layer
output_path = f"/mnt/gold/financial-ratios/{company_symbol}"
ratios_df.write.mode("overwrite").parquet(output_path)

print(f"Financial ratios for {company_symbol} have been calculated and saved to {output_path}")

# COMMAND ----------

# Display a sample of the results
display(ratios_df.select("symbol", "fiscalDateEnding", "gross_margin_ratio", "net_profit_margin", "current_ratio", "debt_to_equity_ratio").limit(5))