
import pandas as pd
import matplotlib.pyplot as plt

#data loading
prod = pd.read_csv("data/production_log.csv", parse_dates=["date"])
down = pd.read_csv("data/downtime_log.csv", parse_dates=["date"])


#function to calculate oee
def calc_oee(df):

    planned = df["planned_time_min"].sum()
    run = df["run_time_min"].sum()
    total = df["total_parts"].sum()
    good = df["good_parts"].sum()

    
    ideal_time_min = (df["ideal_cycle_time_sec"] * df["total_parts"]).sum() / 60

    availability = run / planned
    performance = ideal_time_min / run
    quality = good / total
    oee = availability * performance * quality

    return pd.Series({
        "Availability": availability,
        "Performance": performance,
        "Quality": quality,
        "OEE": oee,
    })
#pareto formula
def make_pareto(df, group_col):
    p = (df.groupby(group_col)["duration_min"]
        .sum()
        .sort_values(ascending=False)
        .to_frame("total_min")
    )
    p["percent"] = p["total_min"] / p["total_min"].sum() * 100
    p["cumulative_percent"] = p["percent"].cumsum()
    return p

#plot pareto
def plot_pareto(p, title, filename):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(p.index, p["total_min"], color="steelblue")
    ax1.set_ylabel("Total downtime (min)")
    ax1.set_xticks(range(len(p)))
    ax1.set_xticklabels(p.index, rotation=35, ha="right")
 
    ax2 = ax1.twinx()  
    ax2.plot(p.index, p["cumulative_percent"], color="crimson", marker="o")
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1)  
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("Cumulative %")
 
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

#pareto for each machine
def pareto_for_machine(down_df, machine):
    d = down_df[down_df["machine"] == machine]
    p = make_pareto(d, "cause")
    print(f"\n=== PARETO TABLE: {machine} ONLY ===")
    print(p.round(1))
    plot_pareto(p, f"{machine} Downtime Causes", f"outputs/pareto_{machine}.png")
    return p


#overall oee 

overall = calc_oee(prod)
by_machine = prod.groupby("machine").apply(calc_oee, include_groups=False)
by_day = prod.groupby("date").apply(calc_oee, include_groups=False)
by_shift = prod.groupby("shift").apply(calc_oee, include_groups=False)

print("=== OVERALL ===")
print((overall * 100).round(1))
print("\n=== PER MACHINE (%) ===")
print((by_machine * 100).round(1))
print("\n=== PER SHIFT (%) ===")
print((by_shift * 100).round(1))

#pareto graphs

    #plant wide
pareto = make_pareto(down, "cause")
print("\n=== PARETO TABLE BY CAUSE ===")
print(pareto.round(1))
plot_pareto(pareto, "Pareto chart of downtime causes", "outputs/downtime_pareto.png")

    #by category
pareto = make_pareto(down, "category")
print("\n=== PARETO TABLE BY CATEGORY ===")
print(pareto.round(1))
plot_pareto(pareto, "downtime by categories", "outputs/category_pareto.png")

    #by each machine
machine_paretos = {}
for m in sorted(down["machine"].unique()):
    machine_paretos[m] = pareto_for_machine(down, m)



#oee plot per machine with availability, performance, quality 
(by_machine * 100).plot(kind="bar", figsize=(10, 6))
plt.ylabel("%")
plt.title("A / P / Q / OEE per Machine")
plt.xticks(rotation=0)
plt.axhline(85, color="gray", linestyle="--", linewidth=1)  # world-class OEE line
plt.tight_layout()
plt.savefig("outputs/oee_by_machine.png", dpi=150)
plt.close()

#daily oee trend
plt.figure(figsize=(10, 5))
plt.plot(by_day.index, by_day["OEE"] * 100, marker=".")
plt.ylabel("OEE (%)")
plt.title("Daily OEE Trend")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/oee_daily.png", dpi=150)
plt.close()

print("\nCharts saved in outputs/")
print(calc_oee(prod.iloc[[0]]))