import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Paths
seriatim_path = "../jclust/output/output_seriatim.csv"
param_path = "../jclust/kmod/kmodparam.csv"
outdir = "./boxplots"
os.makedirs(outdir, exist_ok=True)

# Load data
seriatim = pd.read_csv(seriatim_path)
params = pd.read_csv(param_path)

# Clean column names
seriatim.columns = [col.strip() for col in seriatim.columns]
params.columns = [col.strip() for col in params.columns]

# Extract numeric RunIndex from strings like "Run1"
seriatim["RunIndex"] = seriatim["RunIndex"].astype(str).str.extract("(\d+)").astype(int)
params["RunIndex"] = params["RunIndex"].astype(int)

# Merge Config into seriatim and rename
seriatim = pd.merge(
    seriatim.drop(columns=["Configuration"], errors="ignore"),
    params[["RunIndex", "Config"]],
    on="RunIndex",
    how="left"
).rename(columns={"Config": "Configuration"})


# Debug info
print("=== DEBUG INFO ===")
print("Columns in seriatim:", seriatim.columns.tolist())
print("Unique DataSet values:", seriatim["DataSet"].unique())
print("Unique Algorithm values:", seriatim["Algorithm"].unique())
print("Unique Configuration values:", seriatim["Configuration"].unique())
print("Missing in CorrectedRandIndex:", seriatim["CorrectedRandIndex"].isna().sum())
print("Missing in RunTime:", seriatim["RunTime"].isna().sum())
print("Seriatim row count:", len(seriatim))

# Metrics to plot
metrics = [
    ("CorrectedRandIndex", "ARI"),
    ("RunTime", "Runtime")
]

# Plot per dataset and metric
for dataset in seriatim["DataSet"].unique():
    subset = seriatim[seriatim["DataSet"] == dataset]

    for metric_col, metric_label in metrics:
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            data=subset,
            x="Algorithm",
            y=metric_col,
            hue="Configuration"
        )
        plt.title(f"{metric_label} by Algorithm and Config - {dataset}")
        plt.tight_layout()
        fname = f"{metric_label}_{dataset.replace('.csv','')}.png"
        plt.savefig(os.path.join(outdir, fname))
        plt.close()
