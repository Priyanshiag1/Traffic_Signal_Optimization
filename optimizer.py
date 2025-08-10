import json
import os
from collections import defaultdict
from pulp import LpProblem, LpVariable, lpSum, LpMaximize
import streamlit as st

def run_optimization(cycle_time, sat_rate):
    # 🌐 Use absolute path relative to this file
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.json")

    with open(config_path) as f:
        config = json.load(f)

    config["flowFile"] = "hangzhou_4_4.json"
    config["roadnetFile"] = "roadnet_4_4.json"
    flow_path = os.path.join(base_path, config["flowFile"])
    roadnet_path = os.path.join(base_path, config["roadnetFile"])

    with open(flow_path) as f:
        flow_data = json.load(f)
    with open(roadnet_path) as f:
        roadnet_data = json.load(f)

    arrival_table = defaultdict(list)
    for vehicle in flow_data:
        time = vehicle['startTime']
        start = vehicle['route'][0]
        arrival_table[start].append(time)

    arrival_demand = {road: len(times) for road, times in arrival_table.items()}
    intersection_id = "intersection_1_1"
    intersections = [i for i in roadnet_data["intersections"] if i["id"] == intersection_id]
    if not intersections:
        raise ValueError("Intersection 'intersection_1_1' not found in roadnet.")
    intersection = intersections[0]
    num_phases = len(intersection["trafficLight"]["lightphases"])
    sorted_roads = sorted(arrival_demand.items(), key=lambda x: x[1], reverse=True)
    phase_to_road = {f"P{i+1}": sorted_roads[i][0] for i in range(min(num_phases, len(sorted_roads)))}
    phase_demand = {p: arrival_demand[r] for p, r in phase_to_road.items()}

    model = LpProblem("TrafficSignalOptimization", LpMaximize)
    green_vars = {p: LpVariable(f"green_{p}", lowBound=10, upBound=60) for p in phase_to_road}
    served_vars = {p: LpVariable(f"served_{p}", lowBound=0) for p in phase_to_road}

    model += lpSum(served_vars[p] * phase_demand[p] for p in phase_to_road)
    model += lpSum(green_vars[p] for p in phase_to_road) == cycle_time

    for p in phase_to_road:
        model += served_vars[p] <= sat_rate * green_vars[p]
        model += served_vars[p] <= phase_demand[p]
    model.solve()

    opt_green = {p: green_vars[p].varValue for p in phase_to_road}
    opt_served = {p: served_vars[p].varValue for p in phase_to_road}
    return opt_green, opt_served, phase_demand, list(phase_to_road.keys())

def manual_check(opt_green, opt_served, phase_demand, green_phases, cycle_time, sat_rate):
    st.markdown("### 📋 Manual Model Checks:")
    st.markdown("---")
    total_green = sum(opt_green.get(p, 0) for p in green_phases)
    st.write(f"✅ **Total Green Time:** `{total_green:.2f}` sec (Expected: `{cycle_time}`)")
    for phase in green_phases:
        green = opt_green.get(phase, 0)
        served = opt_served.get(phase, 0)
        demand = phase_demand.get(phase, 0)
        sat_limit = sat_rate * green
        st.markdown(f"#### ⏱️ Phase: {phase}")
        st.write(f"• Green Time: `{green:.2f}` sec")
        st.write(f"• Served Vehicles: `{served:.2f}`")
        st.write(f"• Demand: `{demand}`")
        st.write(f"• Saturation Limit: `{sat_limit:.2f}`")
        if served > demand:
            st.error("⚠️ Served more vehicles than demand.")
        if served > sat_limit:
            st.error("⚠️ Served exceeds saturation limit.")
        if green < 10 or green > 60:
            st.warning("⚠️ Green time not in safe bounds (10–60 sec).")
        if demand > 0 and green <= 10:
            st.warning("⚠️ High demand but green time stuck at minimum.")
