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

| Metric | Formula | Losses Captured |
|---|---|---|
| **Availability** | Run time / Planned time | Breakdown<br>Changeover<br>Material shortages |
| **Performance** | (Ideal cycle time × Total parts) / Run time | Slow cycle<br>Minor stops |
| **Quality** | Good parts / Total parts | Scrap<br>Rework |
| **OEE** | Availability × Performance × Quality | — |

**NOTE:** OEE is calculated by summing up raw times and parts count first. Average per shift percentages are not considered in calculation as different machines have different volumes.
The OEE function was verified by hand against a three rows of production logs.

Pareto analysis
  1. Sum downtime (minutes) for each cause/category/machine-specific-cause
  2. Sorted from largest to smallest
  3. Percentage = (group total / grand total) * 100
  4. cumulative percentage = running sum of percentage column
  5. Totals are plotted in bars, cumulative percentage is plotted as line with reference line at 80%.

**6. ASSUMPTIONS**

  a. 4 machines (CNC-1 to CNC-4), 3 Shifts (A,B,C), 30 days, 480 planned minutes per shift
  b. Ideal cycle times are : 30 s, 30 s, 45 s and 60 s.
  c. Number of stops per shift follows a Poisson distribution, where mean stops per shifts are : 2.0, 2.5, 4.0, and 2.0 for CNC-1 to CNC-4 respectively. CNC-3 is deliberately modelled as a problematic machine.
  d. Stop duration follows an exponential distribution with a different mean for each cause from 8 to 40 minutes.
  e. Eight downtime causes with skewed probabilities, grouped into four categories: Breakdown, Setup, Material and other.
  f. each shift runs at 80-95% of ideal speed at random.
  g. Each shift has a random scrap rate of 1% to 5%.
  h. No shift effect was built into the data

**7. RESULTS**

A. OVERALL EQUIPMENT EFFECTIVENESS

	             	 Availability	  Performance	    Quality	      OEE
                
	Plant overall	    89.1%	          87.2%	          97.1%	    75.4%

	CNC-1	            92.8%	          87.5%	          97.0%	    78.8%
	CNC-2	            88.2%	          87.1%	          97.2%	    74.7%
	CNC-3	            83.0%	          87.3%	          96.9%	    70.3%
	CNC-4	            92.5%	          87.0%	          97.1%	    78.1%

	Shift A        	 	89.2%	          87.3%	          97.0%	    75.6%
	Shift B	         	89.5%	          87.0%	          97.0%	    75.6%
	Shift C	          	88.6%	          87.4%	          97.1%	    75.2%


B. DOWNTIME PARETO (PLANT WIDE, BY CAUSE)

	Cause	                    Minutes	      %	      Cumulative %
	Tool breakage          	    4835	    25.7	        25.7
	Changeover	                3664	    19.5	        45.2
	Hydraulic leak	            3313	    17.6	        62.8
	Operator absence	        2297	    12.2	        75.0
	Material shortage	        1881	    10.0	        85.0
	Sensor fault	            1406	     7.5	        92.5
	Coolant issue              	 718	     3.8	        96.3
	Inspection wait	             694	     3.7	       100.0


C. DOWNTIME PARETO (BY CATEGORY)

	Category	                Minutes	      %	      Cumulative %
	Breakdown	                 10272	    54.6	        54.6
	Setup        	              3664	    19.5	        74.1
	Other	                      2991	    15.9	        90.0
	Material	                  1881	    10.0	       100.0



**8. KEY FINDINGS**

  A. Plant OEE is 75.4%, which lies below ~85%, which is commonly quoted as world-class. The largest loss is performance (87.2%), followed by availability (89.1%). Quality loss is small.
  B. CNC-3 is the weakest machine with (70.3% OEE), almost entirely due to the loss of availability (83.0% for CNC-3 vs 92.8% for CNC-1). But, the performance and quality are similar to that of other machines.
  C. Tool breakage is the largest single cause of downtime accounting for 25.7%. However, Downtime due to breakdown is 54.6% indicating that developing a broader maintenance strategy offers improvement potential.
  D. In CNC-3, the second largest single downtime cause is hydraulic leaks at 22.7% which is almost as large as tool breakage at 24.2% of the total downtime. In a real environment, this would help pointing out to an equipment specific problem.

**9. LIMITATIONS**

  A. The data is simulated. The conclusion only shows that the analysis works and behaves sensibly and do not represent any information about a real production plant.
  B. Performance loss is a single random factor per shift. It is not broken down into minor stops versus reduced speed. 
  C. Scheduled breaks and planned maintenance were not modelled separately from unplanned downtime. 
  D. Every machines shares the same cause probabilities, only the stop rate differs.

**Author**
Tharaniraam Sakthimurugan | https://www.linkedin.com/in/tharaniraam/ | tharaniraamcs@gmail.com
