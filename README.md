# Traffic Signal Optimization using MILP

## Overview
This project presents a *Mixed-Integer Linear Programming (MILP)-based framework for optimizing green signal durations at an isolated intersection. Using real-world traffic data from the **Hangzhou CityFlow dataset, the model dynamically allocates green times to each signal phase to **maximize the number of vehicles served* while respecting operational constraints.

The project demonstrates how *mathematical optimization* can be applied to solve *urban traffic congestion* problems in smart city contexts.

---

## Dataset
We use the *open-source Hangzhou CityFlow dataset*, which includes:
- *roadnet_4_4.json*: Road network structure, intersection definitions, lane connections, and signal phases.
- *hangzhou_4_4.json*: Time-stamped vehicle inflow data for each lane.

### Focus Intersection
- *ID:* intersection_1_1
- *Phases:* P1–P8 (different sets of lanes receiving green light)
- *Cycle Length:* 240 seconds (also tested with 300 seconds in relaxed case)

---

## Preprocessing Steps
1. *Phase Extraction:* Identify phases for intersection_1_1 from roadnet_4_4.json.
2. *Demand Computation:* Aggregate incoming vehicles per phase over the cycle length using hangzhou_4_4.json.
3. *Saturation Flow Assignment:* Assign saturation rates (0.5–1.0 vehicles/sec) based on lane count.
4. *Filtering:* Consider only active flows during peak hours.

---

## MILP Model Formulation

*Decision Variables*
- *Continuous:*
  - \( G_p \): Green time allocated to phase \(p\)
  - \(\text{served}_p\): Vehicles served during phase \(p\)
- *Binary:*
  - \( g_{pt} \): 1 if phase \(p\) is green at time \(t\)
  - \( \gamma_{pt} \): 1 if green starts for phase \(p\) at time \(t\)

*Objective Function*
\[
\text{Maximize} \quad \sum_{p \in P} w_p \times \text{served}_p
\]
Where \(w_p\) is the weight (priority) of phase \(p\).

*Constraints*
- Total green time = cycle length
- Green time bounds per phase
- Served vehicles ≤ demand
- Served vehicles ≤ saturation flow × green time
- Logical constraints for phase sequencing

---

## Implementation
- *Language:* Python
- *Libraries:* PuLP for MILP modeling, CBC solver
- *Approach:*
  1. Parse JSON data and compute demand & saturation rates.
  2. Formulate MILP in PuLP.
  3. Solve using CBC (Branch-and-Bound + Cutting Planes).
  4. Output optimal green times and vehicles served.

---

## Results
- *Baseline:* Fixed-time control (equal green times)
- *Optimized:* MILP-based dynamic allocation
- *Outcome:* Increased vehicles served, especially for high-demand phases, while maintaining fairness.

---

## Streamlit Dashboard
A *Streamlit* app is provided for interactive experimentation with:
- Cycle length adjustments
- Demand scenarios
- Real-time visualization of green time allocation

---

## Future Work
1. Multi-intersection coordination.
2. Queue build-up and dissipation modeling.
3. Real-time integration with live traffic detectors.
4. Hybrid MILP + Reinforcement Learning approach.
5. Pedestrian phase and emergency vehicle priority handling.

---

## References
- Hangzhou CityFlow Dataset: [https://cityflow-project.github.io/](https://cityflow-project.github.io/)
- PuLP Documentation: [https://coin-or.github.io/pulp/](https://coin-or.github.io/pulp/)
- CBC Solver: [https://github.com/coin-or/Cbc](https://github.com/coin-or/Cbc)

---
