import re
import pandas as pd
import numpy as np

# Flipkart price cleaner
def clean_price_list(series):
    clean_prices = []
    for price in series:
        price = str(price)
        cleaned = re.sub(r"[₹,]", "", price).strip()   # remove ₹ and commas
        cleaned = cleaned.rstrip(".")                 # remove dot at end (130900. → 130900)

        if cleaned == "" or cleaned.lower() == "nan":
            clean_prices.append(np.nan)
        else:
            clean_prices.append(int(cleaned))
    return clean_prices



# Amazon rating cleaner -> "4.5 out of 5 stars" -> 4.5
def clean_amazon_rating(ratings):
    clean_ratings = []
    for r in ratings:
        r = str(r)
        match = re.search(r"\d+\.\d|\d", r)
        if match:
            clean_ratings.append(float(match.group(0)))
        else:
            clean_ratings.append(np.nan)
    return clean_ratings



# -------- Read CSV --------
df_flipkart = pd.read_csv("flipkard.csv")
df_amazon = pd.read_csv("amazom.csv")

# remove extra spaces from column names
df_amazon.columns = df_amazon.columns.str.strip()
df_flipkart.columns = df_flipkart.columns.str.strip()

print("\nAmazon Columns:", df_amazon.columns.tolist())
print("Flipkart Columns:", df_flipkart.columns.tolist())

# -------- Detect Price column --------
amazon_price_col = [col for col in df_amazon.columns if "price" in col.lower()]
if amazon_price_col:
    amazon_price_col = amazon_price_col[0]     # use first match
else:
    raise Exception("❌ 'Price' column not found in amazon.csv")

flipkart_price_col = [col for col in df_flipkart.columns if "price" in col.lower()]
if flipkart_price_col:
    flipkart_price_col = flipkart_price_col[0]
else:
    raise Exception("❌ 'Price' column not found in flipkard.csv")


# -------- Apply Cleaning --------
df_flipkart[flipkart_price_col] = clean_price_list(df_flipkart[flipkart_price_col])
df_amazon[amazon_price_col] = clean_price_list(df_amazon[amazon_price_col])

# Clean Amazon Rating (if exists)
if "Rating" in df_amazon.columns:
    df_amazon["Rating"] = clean_amazon_rating(df_amazon["Rating"])



# -------- Save back to same CSV files --------
df_flipkart.to_csv("flipkard.csv", index=False)
df_amazon.to_csv("amazom.csv", index=False)

print("\nCSV cleaned and saved successfully!\n")
# print(df_flipkart.head())
# print(df_amazon.head())
