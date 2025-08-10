import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import normalized_mutual_info_score

# Paths
param_path = "../jclust/kmod/kmodparam.csv"
wine_path = "../jclust/kmtd/wine.csv"
frog_path = "../jclust/kmtd/Frogs_MFCCs(10).csv"

# Load ground truth labels
wine_truth = pd.read_csv(wine_path, header=None).iloc[:, 0].values
frog_truth = pd.read_csv(frog_path).iloc[:, -1].values

# Load params
params = pd.read_csv(param_path)
params["RunIndex"] = params["RunIndex"].astype(int)

# Output dir
outdir = "./boxplots"
os.makedirs(outdir, exist_ok=True)

results = []

# For each Kmod config row
for _, row in params.iterrows():
    algo = row["Algorithm"]
    cfg = row["Config"]
    runidx = row["RunIndex"]
    dataset = row["DataFile"]
    
    if not isinstance(cfg, str) or pd.isna(cfg):
        continue

    cm_file = f"../jclust/CM{runidx - 1}_{algo}.csv"
    if not os.path.exists(cm_file):
        print(f"Missing: {cm_file}")
        continue

    try:
        preds = pd.read_csv(cm_file, header=None)
        for col in preds.columns:
            pred_labels = preds[col].values
            gt = wine_truth if dataset == "wine.csv" else frog_truth
            if len(pred_labels) > len(gt):
                pred_labels = pred_labels[:len(gt)]
            elif len(pred_labels) < len(gt):
                print(f"Skipping {cm_file}: predicted labels too short.")
                continue
            nmi = normalized_mutual_info_score(gt, pred_labels)
            results.append({
                "Algorithm": algo,
                "Configuration": cfg,
                "DataSet": dataset,
                "NMI": nmi
            })
    except Exception as e:
        print(f"Error reading {cm_file}: {e}")

# Convert to DataFrame
df = pd.DataFrame(results)

if df.empty:
    print("No valid NMI data collected. Exiting.")
    exit()
    
# Plot per dataset
for dataset in df["DataSet"].unique():
    plt.figure(figsize=(10, 6))
    subset = df[df["DataSet"] == dataset]
    sns.boxplot(data=subset, x="Algorithm", y="NMI", hue="Configuration")
    plt.title(f"NMI by Algorithm and Config - {dataset}")
    
    # Remove legend
    plt.legend([], [], frameon=False)
    
    # Rotate x-axis labels
    plt.xticks(rotation=30, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"NMI_{dataset}.png"))
    plt.close()
