import numpy as np 
import pandas as pd 
from datetime import date, timedelta 

np.random.seed(42)  #for results to be predictable

# part 1 - declaring settings 

MACHINES = ["CNC-1", "CNC-2", "CNC-3", "CNC-4"]
SHIFTS = ["A", "B", "C"]
START_DATE  = date(2029, 9,1)
PLANNED_TIME_MIN = 480                          #at 8 hours a shift


IDEAL_CYCLE_SEC = {"CNC-1" : 30, "CNC-2" : 30, "CNC-3" : 45, "CNC-4" : 60}          #ideal cycle time for each machine 

N_DAYS = 30                                     #DATA FOR A MONTH

#considering machine 3 has issues , Average stopppages per shift

STOPS_PER_SHIFT = {"CNC-1" : 2.0, "CNC-2" : 2.5, "CNC-3" : 4.0, "CNC-4" : 2.0}

#cause of the issue with a constant probability for each 
#cause name - category - probability - mean duration 

CAUSES = [
    ("Tool breakage",       "Breakdown",    0.22, 25),
    ("Changeover",          "Setup",        0.20, 20),
    ("Material shortage",   "Material",     0.15, 15),
    ("Sensor fault",        "Breakdown",    0.12, 12),
    ("Hydraulic leak",      "Breakdown",    0.08, 40),
    ("Operator absence",    "Other",        0.08, 30),
    ("Inspection wait",     "Other",        0.08, 8),
    ("Coolant issue",       "Breakdown",    0.07, 10),
]


cause_names = [ c[0] for c in CAUSES]
cause_probs = [ c[2] for c in CAUSES]

cause_info = { c[0] : {"category" : c[1], "mean_duration" : c[3]} for c in CAUSES}


# part 2 - data generation

production_rows = []
downtime_rows = []

for day in range(N_DAYS):
    current_date = START_DATE + timedelta(days=day)

    for shift in SHIFTS:
        for machine in MACHINES:

            n_stops = np.random.poisson(STOPS_PER_SHIFT[machine])
            shift_downtime = 0

            for _ in range(n_stops):                                        #stoppage loop 
                cause = np.random.choice(cause_names, p=cause_probs)

                duration = np.random.exponential(cause_info[cause]["mean_duration"])
                duration = max(1, int(round(duration)))

                if shift_downtime + duration > 0.6 * PLANNED_TIME_MIN:
                    break
                shift_downtime += duration

                downtime_rows.append({
                    "date"          :   current_date,
                    "shift"         :   shift,
                    "machine"       :   machine,
                    "duration_min"  :   duration,
                    "cause"         :   cause,
                    "category"      :   cause_info[cause]["category"]
                })

            #production numbers
            run_time = PLANNED_TIME_MIN - shift_downtime
            ideal_ct = IDEAL_CYCLE_SEC[machine]

            #performance factor (consider machine runs slower than ideal (80-95 %))
            perf_factor = np.random.uniform(0.80, 0.95)
            total_parts = int(run_time * 60 / ideal_ct * perf_factor)

            #scrap , with 1-5% chance of each part being bad
            scrap_rate = np.random.uniform(0.01, 0.05)
            scrapped = np.random.binomial(total_parts, scrap_rate)
            good_parts = total_parts - scrapped 

            production_rows.append({
                "date" : current_date,
                "shift" : shift,
                "machine" : machine,
                "planned_time_min" : PLANNED_TIME_MIN,
                "run_time_min" : run_time,
                "ideal_cycle_time_sec" : ideal_ct,
                "total_parts" : total_parts,
                "good_parts" : good_parts,
            })

#saving data

production_df = pd.DataFrame(production_rows)
downtime_df = pd.DataFrame(downtime_rows)

production_df.to_csv("data/production_log.csv", index=False)
downtime_df.to_csv("data/downtime_log.csv", index=False)

print(f"production_log.csv: {len(production_df)} rows")
print(f"downtime_log.csv:   {len(downtime_df)} rows")
print(production_df.head())
print(downtime_df.head())
