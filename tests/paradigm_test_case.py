import pandas as pd

def analyze_data():
    # Source: pd.read_csv
    data = pd.read_csv("sales_data.csv")
    
    # Intent: Calculate (Math) + prompt stuffing + RAG keywords
    prompt = f"Find and calculate the average sales for this data in the context: {data}"
    
    print(prompt)

if __name__ == "__main__":
    analyze_data()
