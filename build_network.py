import pandas as pd

# Convert nodes CSV to JSON
nodes = pd.read_csv("nodes.csv", keep_default_na=False, encoding="latin1")
nodes.to_json("nodes.json", orient="records", indent=4)

# Convert edges CSV to JSON
edges = pd.read_csv("edges.csv", keep_default_na=False, encoding="latin1")
edges.to_json("edges.json", orient="records", indent=4)

print("Conversion complete.")
print(f"{len(nodes)} nodes converted.")
print(f"{len(edges)} edges converted.")
