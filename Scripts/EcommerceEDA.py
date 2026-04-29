
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "e63ae36b-2474-4e58-af0a-c3452d32f130",
   "metadata": {},
   "source": [
    "# E-Commerce Sales & Profitability Analysis\n",
    "\n",
    "## Objective\n",
    "Analyze sales, profitability, and customer behavior to identify business improvement opportunities."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "388792c3-2ee5-4972-beb5-a6ce349bf723",
   "metadata": {},
   "source": [
    "## 🔹 Step 1: Importing Libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d25fcda2-eb46-4d83-8bcb-ad03446b27a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "plt.style.use('default')\n",
    "sns.set_theme()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ed437a78-d54c-4180-9f7a-39eb122b1202",
   "metadata": {},
   "source": [
    "## 🔹 Step 2: Data Loading"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f943032-7949-4af1-89e1-ca4c3383771c",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load the CLEANED file from SQL\n",
    "df = pd.read_csv(r'C:\\Users\\ASUS\\Desktop\\DA PROJECTS\\POWERBI\\MasterDashboard\\E-Commerce Profitability & Sales Performance Dashboard\\DATA\\Cleaned_Ecommerce_Data.csv')\n",
    "\n",
    "# Since it's a CSV, we still ensure the date is recognized correctly\n",
    "df['order_date'] = pd.to_datetime(df['order_date'])\n",
    "\n",
    "# Look at the first 5 rows to ensure it loaded correctly\n",
    "df.head()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c0a3693c-447b-4a79-a788-2254bdc2d617",
   "metadata": {},
   "source": [
    "## 🔹 Step 3: Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "abee9839-c193-41e1-b6fd-52b0becb1a95",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.info()\n",
    "df.describe()\n",
    "df.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "216b1268-9302-418c-88b2-46d3f537eb74",
   "metadata": {},
   "source": [
    "## 🔹 Step 4: Data Quality Check"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ed769545-4568-4675-82dd-f8878d6e7571",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 4: Data Quality Check\n",
    "\n",
    "print(\"Duplicate rows:\", df.duplicated().sum())\n",
    "\n",
    "# Missing values heatmap                                                        \n",
    "plt.figure(figsize=(8,5))                                                      \n",
    "sns.heatmap(df.isnull(), cbar=False, cmap='viridis')                           \n",
    "plt.title(\"Missing Values Heatmap (Yellow = Missing)\")\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3e3bc75f-df88-4c28-bcd2-a07a18190650",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "The dataset contains no significant missing values or duplicate records. Data types are correctly formatted, especially the order_date.\n",
    "\n",
    " Why it matters:\n",
    "Clean and reliable data ensures that all downstream analysis and KPIs are accurate and trustworthy.\n",
    "\n",
    " Business Recommendation:\n",
    "No immediate data cleaning actions required. The dataset is ready for advanced analysis and decision-making."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4e70b601-06dd-41fe-9654-e02a342c38bd",
   "metadata": {},
   "source": [
    "## 🔹 Step 5: Feature Engineering"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "32384a1a-96b7-41d5-af7d-0d8114f9aa3f",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['profit_margin_%'] = np.where(df['amount'] != 0,\n",
    "                                (df['profit'] / df['amount']) * 100,\n",
    "                                0)\n",
    "\n",
    "df['month'] = df['order_date'].dt.month_name()\n",
    "df['day_of_week'] = df['order_date'].dt.day_name()\n",
    "df['year_month'] = df['order_date'].dt.to_period('M')\n",
    "\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f05910ca-103c-416e-8134-93c12b92b3bf",
   "metadata": {},
   "source": [
    "## 🔹 Step 6: Executive KPI Summary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7c6ef181-057a-4c91-8e7f-c6957edb15b3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Calculate high-level KPIs\n",
    "total_revenue = df['amount'].sum()\n",
    "total_profit = df['profit'].sum()\n",
    "total_orders = df['order_id'].nunique()\n",
    "avg_order_value = total_revenue / total_orders\n",
    "overall_profit_margin = (total_profit / total_revenue) * 100\n",
    "\n",
    "# Displaying the Summary Table\n",
    "kpi_summary = pd.DataFrame({\n",
    "    'Metric': ['Total Revenue', 'Total Profit', 'Total Orders', 'Avg Order Value', 'Profit Margin %'],\n",
    "    'Value': [f\"₹{total_revenue:,.2f}\", \n",
    "              f\"₹{total_profit:,.2f}\", \n",
    "              f\"{total_orders:,}\", \n",
    "              f\"₹{avg_order_value:,.2f}\", \n",
    "              f\"{overall_profit_margin:.2f}%\"]\n",
    "})\n",
    "\n",
    "print(\"--- EXECUTIVE KPI SUMMARY ---\")\n",
    "print(kpi_summary.to_string(index=False))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7d72ae36-9686-43ca-9260-10c7cc9216a5",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "The business generated strong total revenue, but the overall profit margin is relatively moderate/low.\n",
    "\n",
    " Why it matters:\n",
    "High revenue does not necessarily indicate a healthy business if profit margins are thin.\n",
    "\n",
    " Business Recommendation:\n",
    "Focus on improving margins by optimizing pricing, reducing discounts, and controlling operational costs rather than only increasing sales."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "723eb4af-de8e-4ef0-99ad-1ddda808736e",
   "metadata": {},
   "source": [
    "## 🔹 Step 7: Exploratory Data Analysis (EDA)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "32d39ef6-f079-4e0d-b605-fd88dabfa786",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.1: Customer Analysis\n",
    "\n",
    "# 7.1.1: Top 10 Customers by Revenue\n",
    "top_customers = df.groupby('customer_name')['amount'].sum().sort_values(ascending=False).head(10)\n",
    "print(top_customers)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5c864450-10a9-43a7-ae60-e3198c87ccba",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "A small group of customers contributes a large portion of total revenue (high-value customers).\n",
    "\n",
    " Why it matters:\n",
    "Revenue dependency on a small customer base increases business risk and highlights the importance of customer retention.\n",
    "\n",
    " Business Recommendation:\n",
    "Introduce a VIP loyalty program and personalized offers to retain high-value customers and increase repeat purchases."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "907c05b2-0d57-4749-a9a0-bcc77b1cf79a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.1.2: Customer segmentation based on revenue\n",
    "\n",
    "customer_sales = df.groupby('customer_name')['amount'].sum()\n",
    "\n",
    "segments = pd.qcut(customer_sales, q=3, labels=['Low Value', 'Mid Value', 'High Value'])\n",
    "\n",
    "segment_df = pd.DataFrame({\n",
    "    'Revenue': customer_sales,\n",
    "    'Segment': segments\n",
    "})\n",
    "\n",
    "print(segment_df['Segment'].value_counts())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "54e79f60-b90c-401f-8b09-2d4689c3dae3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.2: Loss Analysis \n",
    "\n",
    "loss_df = df[df['profit'] < 0]\n",
    "\n",
    "loss_by_category = loss_df.groupby('category')['profit'].sum()\n",
    "print(loss_by_category)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1065b286-2208-46f2-aabb-9783c6968801",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Certain product categories consistently generate negative profit.\n",
    "\n",
    " Why it matters:\n",
    "Selling loss-making products reduces overall profitability and may indicate pricing or cost inefficiencies.\n",
    "\n",
    " Business Recommendation:\n",
    "Re-evaluate pricing, supplier costs, and discount strategies for these categories. Consider discontinuing or bundling them with profitable products."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9a8f9775-7a6e-46aa-9cdd-13d905035e76",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.3: Univariate Analysis (Individual Variables)\n",
    "\n",
    "# 7.3.1: Sales Distribution (Amount)\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.histplot(df['amount'], kde=True, color='blue')\n",
    "plt.title('Distribution of Order Amounts')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "811bba0d-92a4-4f6e-bfc9-3f72e05f23d1",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Sales distribution is right-skewed, with most orders being low-value and a few high-value transactions.\n",
    "\n",
    " Why it matters:\n",
    "A small number of high-value orders significantly impact total revenue.\n",
    "\n",
    " Business Recommendation:\n",
    "Segment customers into retail vs bulk buyers and create targeted strategies for each group."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "93cfaf2c-5e45-4e2e-a3af-c578872c592a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.3.2: Profit Outliers\n",
    "\n",
    "# Boxplot to identify outliers in Profit\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.boxplot(x=df['profit'])\n",
    "plt.title('Profit Outlier Detection')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "65d58f14-54b7-48d3-85e3-ed68edba51a2",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "There are extreme negative and positive profit values (outliers).\n",
    "\n",
    " Why it matters:\n",
    "These outliers may indicate heavy discounts, returns, or high shipping costs.\n",
    "\n",
    " Business Recommendation:\n",
    "Investigate extreme loss transactions and implement controls on discounting and logistics costs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e1d2c3bb-d454-4c85-ae64-ca05c0c09bcd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.3.3: Bottom Products\n",
    "\n",
    "# Find loss-making sub-categories\n",
    "bottom_products = df.groupby('sub_category')['profit'].sum().nsmallest(10)\n",
    "\n",
    "bottom_products.sort_values().plot(kind='barh', figsize=(5,5))\n",
    "plt.title(\"Top Loss-Making Sub-Categories\")\n",
    "plt.xlabel(\"Profit(₹)\")\n",
    "plt.ylabel(\"Sub-Category\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b2362756-9ea8-40cf-842f-24fc3a0fa863",
   "metadata": {},
   "source": [
    " 📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Certain sub-categories consistently generate losses.\n",
    "\n",
    " Why it matters:\n",
    "These products are directly impacting profitability despite contributing to sales volume.\n",
    "\n",
    " Business Recommendation:\n",
    "Optimize pricing, reduce discounts, or bundle these products with high-margin items to recover losses."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "97fbbf3e-e5fa-4aba-9619-a8ece49ae052",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.4: Category Analysis\n",
    "\n",
    "# Profit by Category\n",
    "category_analysis = df.groupby('category')['profit'].sum().sort_values(ascending=False)\n",
    "category_analysis.plot(kind='bar', color='teal', figsize=(10,5))\n",
    "plt.ylabel('Total Profit')\n",
    "plt.title('Profitability by Product Category')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6befacb6-cce6-4697-a7d6-c8ceb7029348",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    " \n",
    " Observation:\n",
    "Some categories generate high profit while others underperform.\n",
    "\n",
    " Why it matters:\n",
    "Not all product categories contribute equally to business success.\n",
    "\n",
    " Business Recommendation:\n",
    "Focus marketing and inventory investment on high-performing categories while re-evaluating underperforming ones."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fcee1596-b449-4da5-9bec-9d2d963b2249",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.5: Bivariate Analysis (Relationships)\n",
    "\n",
    "# Relationship between Quantity and Profit\n",
    "sns.scatterplot(data=df, x='quantity', y='profit', hue='category')\n",
    "plt.title('Quantity vs Profit by Category')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "67d1b5de-f8c9-4832-b8f0-da91f4f54b77",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Higher quantity sold does not always lead to higher profit.\n",
    "\n",
    " Why it matters:\n",
    "This indicates inconsistent profit margins across products.\n",
    "\n",
    " Business Recommendation:\n",
    "Shift focus from volume-driven sales to margin-driven sales strategy."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9eea2382-5316-43d7-b5a7-340748c8dedf",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.6: State Analysis (Identify loss-making states)\n",
    "\n",
    "state_profit = df.groupby('state')['profit'].sum().sort_values()\n",
    "\n",
    "plt.figure(figsize=(12, 8))\n",
    "sns.barplot(x=state_profit.values, y=state_profit.index, palette='RdYlGn')\n",
    "plt.title('Total Profit/Loss by State')\n",
    "plt.xlabel('profit (₹)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e6041650-2753-4668-9b34-2c4a2b7a8101",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Certain states are consistently generating losses.\n",
    "\n",
    " Why it matters:\n",
    "Regional inefficiencies such as high shipping costs or return rates may be affecting profitability.\n",
    "\n",
    " Business Recommendation:\n",
    "Optimize logistics, adjust delivery pricing, or reconsider operations in loss-making regions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "27a330c2-c4d7-4ae4-833e-c056bd00758f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.7: Profit Margin Analysis\n",
    "\n",
    "category_margin = df.groupby('category').apply(\n",
    "    lambda x: (x['profit'].sum() / x['amount'].sum()) * 100\n",
    ")\n",
    "\n",
    "category_margin.plot(kind='bar', figsize=(10,5))\n",
    "plt.title(\"Profit Margin % by Category\")\n",
    "plt.ylabel(\"Profit Margin (%)\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5ec7836e-4a15-4f9e-989a-b2c83684824a",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Some categories have high revenue but low profit margins.\n",
    "\n",
    " Why it matters:\n",
    "Revenue alone is misleading without considering profitability.\n",
    "\n",
    " Business Recommendation:\n",
    "Promote high-margin categories and reduce dependency on low-margin products."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "39720ffb-27a2-455b-b23c-f8fafdf6f21e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.8: Time-Series Analysis (Seasonality)\n",
    "\n",
    "# 7.8.1: Monthly Sales Trend\n",
    "monthly_sales = df.groupby('year_month')['amount'].sum()\n",
    "plt.figure(figsize=(12, 6))\n",
    "monthly_sales.plot(marker='o', linestyle='-')\n",
    "plt.title('Total Sales Trend Over Time')\n",
    "plt.ylabel('Revenue')\n",
    "plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54024052-f232-4e68-9519-5254d3b78f67",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Sales peak during specific months (likely festive/holiday season) and drop afterward.\n",
    "\n",
    " Why it matters:\n",
    "Business is highly seasonal.\n",
    "\n",
    " Business Recommendation:\n",
    "Plan inventory and marketing campaigns around peak seasons and introduce offers during low-demand months."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "93e21e99-e03d-466a-9701-ecd0708ab5ba",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.8.2: Revenue vs Profit Trend\n",
    "\n",
    "monthly_data = df.groupby('year_month').agg({\n",
    "    'amount': 'sum',\n",
    "    'profit': 'sum'\n",
    "})\n",
    "\n",
    "plt.figure(figsize=(12,6))\n",
    "plt.plot(monthly_data.index.astype(str), monthly_data['amount'], marker='o', label='Revenue')\n",
    "plt.plot(monthly_data.index.astype(str), monthly_data['profit'], marker='o', label='Profit')\n",
    "\n",
    "plt.xticks(rotation=45)\n",
    "plt.title(\"Revenue vs Profit Trend Over Time\")\n",
    "plt.legend()\n",
    "plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ab6f3427-c94d-4954-a2b1-882066acae94",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Revenue and profit trends are not perfectly aligned.\n",
    "\n",
    " Why it matters:\n",
    "Increasing revenue does not always result in increased profitability.\n",
    "\n",
    " Business Recommendation:\n",
    "Monitor profit alongside revenue and avoid aggressive discounting during high-sales periods."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "11d118b3-a254-4e5f-8890-92558299a1b4",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.9: Pareto Analysis\n",
    "\n",
    "customer_revenue = df.groupby('customer_name')['amount'].sum().sort_values(ascending=False)\n",
    "\n",
    "cumulative = customer_revenue.cumsum() / customer_revenue.sum()\n",
    "\n",
    "plt.figure(figsize=(10,5))\n",
    "plt.plot(cumulative.values)\n",
    "plt.axhline(0.8, linestyle='--')\n",
    "\n",
    "plt.title(\"Pareto Analysis (80/20 Rule)\")\n",
    "plt.xlabel(\"Customers\")\n",
    "plt.ylabel(\"Cumulative Revenue %\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "de81606d-5469-4c0f-a6e8-cf036061f918",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Approximately 20% of customers contribute to around 80% of total revenue.\n",
    "\n",
    " Why it matters:\n",
    "Business heavily depends on a small group of customers.\n",
    "\n",
    " Business Recommendation:\n",
    "Focus on retaining top customers and increasing their lifetime value."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f664541b-0f5a-4854-87eb-e33e008263e5",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 7.10: The Correlation Heatmap\n",
    "\n",
    "# Select only numeric columns for correlation\n",
    "numeric_df = df.select_dtypes(include=[np.number])\n",
    "plt.figure(figsize=(10, 8))\n",
    "corr = numeric_df.corr()\n",
    "plt.figure(figsize=(10,8))\n",
    "sns.heatmap(corr, annot=True, fmt=\".2f\", linewidths=0.5)\n",
    "plt.title('Correlation Heatmap of Metrics')\n",
    "plt.show()\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6e20c582-5f48-4e27-8b42-2d1a0141665a",
   "metadata": {},
   "source": [
    "📊 Business Insight\n",
    "\n",
    " Observation:\n",
    "Strong correlation between Quantity and Amount, but weaker correlation between Amount and Profit.\n",
    "\n",
    " Why it matters:\n",
    "Higher sales volume does not guarantee higher profit.\n",
    "\n",
    " Business Recommendation:\n",
    "Analyze cost structure and focus on improving profit margins rather than just increasing sales volume."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a4eb2ef8-7f3b-41f5-9d27-5dfee091c39a",
   "metadata": {},
   "source": [
    "## 🔹 Step 6: Business Insights & Recommendations\n",
    "\n",
    "\n",
    "### Key Findings\n",
    "\n",
    "1. A small group of customers contributes majority of revenue (Pareto effect)\n",
    "2. Certain sub-categories consistently generate losses\n",
    "3. High sales volume does not always translate to high profit\n",
    "4. Business shows strong seasonality with peak sales in specific months\n",
    "5. Some states are consistently loss-making\n",
    "\n",
    "### Strategic Recommendations\n",
    "\n",
    "- Introduce VIP loyalty programs for high-value customers  \n",
    "- Optimize pricing and reduce discounts on loss-making products  \n",
    "- Focus on high-margin categories rather than high-volume sales  \n",
    "- Plan seasonal marketing campaigns to maximize peak periods  \n",
    "- Improve logistics and pricing strategies in loss-making regions  "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4368b88f-7b52-4d80-ae31-e0dac7044d02",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (TensorFlow)",
   "language": "python",
   "name": "tf_env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
