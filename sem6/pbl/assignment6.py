import pandas as pd

# Load the dataset
df = pd.read_csv('datasets/miniproject/Clean_Dataset.csv', index_col=0)

print("--- DASHBOARD VALIDATION SUITE ---")

# 1. KPI: Cheapest Route
# We create a 'Route' column first to identify the path
df['Route'] = df['source_city'] + " -> " + df['destination_city']
cheapest_route_val = df.groupby('Route')['price'].mean().idxmin()
cheapest_route_price = df.groupby('Route')['price'].mean().min()

print(f"\n[KPI] Cheapest Route (Avg): {cheapest_route_val}")
print(f"      Validation Value: {round(cheapest_route_price, 2)}")

# 2. KPI: Economy vs Business Gap
avg_economy = df[df['class'] == 'Economy']['price'].mean()
avg_business = df[df['class'] == 'Business']['price'].mean()
price_gap = avg_business - avg_economy

print(f"\n[KPI] Avg Economy Price: {round(avg_economy, 2)}")
print(f"      Avg Business Price: {round(avg_business, 2)}")
print(f"      Validation Price Gap: {round(price_gap, 2)}")

# 3. Chart Data: Route vs Price (Top 5 most expensive)
print("\n[CHART] Route vs Price (Top 5 Highest):")
print(df.groupby('Route')['price'].mean().sort_values(ascending=False).head(5))

# 4. Chart Data: Destination Popularity vs Pricing
# Popularity = Count of flights
popularity = df.groupby('destination_city').agg({'price': 'mean', 'flight': 'count'})
popularity.columns = ['Avg_Price', 'Flight_Count']
print("\n[CHART] Destination Popularity vs Pricing:")
print(popularity.sort_values(by='Flight_Count', ascending=False))

# 5. Chart Data: Price Over Time (Days Left)
# Since 'days_left' represents time until departure
print("\n[CHART] Price Trend (Price vs Days Left - First 5 entries):")
trend = df.groupby('days_left')['price'].mean().head(5)
print(trend)

# 6. Edge Case Test: Logic Check
# Verification: Is Business always more expensive than Economy?
logic_test = df.groupby(['Route', 'class'])['price'].mean().unstack()
logic_test['Error'] = logic_test['Business'] < logic_test['Economy']
errors = logic_test[logic_test['Error'] == True]

print("\n[TEST] Logic Validation (Business < Economy?):")
if errors.empty:
    print("      PASS: Business is consistently more expensive than Economy.")
else:
    print(f"      FAIL: Found inconsistencies in {len(errors)} routes.")
