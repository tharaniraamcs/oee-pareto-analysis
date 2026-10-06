OVERALL EQUIPMENT EFFECTIVENESS TRACKER AND PARETO ANALYSIS

This python project calculates overall equipment effectiveness (OEE) for a CNC machine shop and uses Pareto analysis to find the time loss in production using **pandas, numpy and matplotlib**

Note: The data in this project is simulated. The parameters are assumed to look realistic. The overall findings below describes a model, not a real scenario.

**1. PROBLEM:**

A factory wants to understands its machine utilisation and which losses to attack first. OEE answers the first question with a single number. Pareto analysis answers the second by ranking downtime causes by size, as smaller causes account for most of the lost time.

**2. OBJECTIVE:**

  a.  This model generates a 30 days of production and downtime logs for 4 CNC machines, across 3 shifts per day (generate_machine_data.py)
  b.  The OEE, Availability, Performance, Quality is calculated in categories such as plant wide, per machine, per shift and per day (analysis.py)
  c.  The downtime loss is ranked with the help of pareto chart at categorized such as plant wide by cause, plant wide by category, and one chart per machine.

**3. STRUCTURE:**

OEE_PROJECT/
  generate_machine_data.py  #creates the simulated CSV logs
  analysis.py               #OEE calculations and pareto charts
  data/
      production_log.csv    #one row per machine per shift
      downtime_log.csv      #one row per stoppage
  outputs/                  #generated charts (PNG)

**4.REQUIREMENTS:**

1. requires Python 3.9+ with numpy, pandas and matplotlib
2. python generate_machine_data.py #writes the data to CSVs
3. python analysis.py              #prints results and saves charts to output folder

**5. METHODOLOGY:**

|  **Metric**    |  **Formula**                                  |  **Loss Captured**                          |
|  ============  |  ===========================================  |  =========================================  |
|  Availability  |  run time / planned time                      |  breakdown, changeover, material shortages  |
|  Performance   |  (ideal cycle time * total parts) / run time  |  slow cycle, minor stops                    |
|  Quality       |  good parts / total parts                     |  scrap and rework                           |
|  **OEE**       |  Availability * performance * Quality         |                   -                         |

**NOTE:** OEE is calculated by summing up raw times and parts count first. Average per shift percentages are not considered in calculation as different machines have different volumes.
The OEE function was verified by hand against a three rows of production logs.

Pareto analysis
  1. Sum downtime (minutes) for each cause/category/machine-specific-cause
  2. Sorted from largest to smallest
  3. Percentage = (group total / grand total) * 100
  4. cumulative percentage = running sum of percentage column
  5. Totals are plotted in bars, cumulative percentage is plotted as line with reference line at 80%.

**6. ASSUMPTIONS**

  a. 



