#!/usr/bin/env python3
import json
import statistics
from datetime import datetime
import matplotlib.pyplot as plt

def detailed_timing_analysis():
    timestamps = []
    question_ids = []
    
    # Read the JSONL file
    with open('output/answers.jsonl', 'r') as f:
        for line_num, line in enumerate(f):
            try:
                data = json.loads(line.strip())
                timestamp = data.get('timestamp')
                question_id = data.get('question_id')
                
                if timestamp is not None:
                    timestamps.append(timestamp)
                    question_ids.append(question_id)
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num + 1}: {e}")
                continue
    
    if len(timestamps) < 2:
        print("Not enough timestamps to calculate intervals")
        return
    
    # Calculate time intervals between consecutive answers
    intervals = []
    for i in range(1, len(timestamps)):
        interval = timestamps[i] - timestamps[i-1]
        intervals.append(interval)
    
    # Convert to minutes for easier reading
    intervals_minutes = [interval / 60 for interval in intervals]
    
    # Calculate statistics
    avg_interval = statistics.mean(intervals_minutes)
    median_interval = statistics.median(intervals_minutes)
    min_interval = min(intervals_minutes)
    max_interval = max(intervals_minutes)
    
    # Calculate percentiles
    p25 = statistics.quantiles(intervals_minutes, n=4)[0]
    p75 = statistics.quantiles(intervals_minutes, n=4)[2]
    
    print(f"=== DETAILED TIMING ANALYSIS ===")
    print(f"Total answers: {len(timestamps)}")
    print(f"Total intervals: {len(intervals_minutes)}")
    print(f"\n=== STATISTICS ===")
    print(f"Average time between answers: {avg_interval:.2f} minutes ({avg_interval*60:.1f} seconds)")
    print(f"Median time between answers: {median_interval:.2f} minutes ({median_interval*60:.1f} seconds)")
    print(f"25th percentile: {p25:.2f} minutes")
    print(f"75th percentile: {p75:.2f} minutes")
    print(f"Minimum interval: {min_interval:.2f} minutes ({min_interval*60:.1f} seconds)")
    print(f"Maximum interval: {max_interval:.2f} minutes ({max_interval*60:.1f} seconds)")
    
    # Calculate total time span
    total_time_span = (timestamps[-1] - timestamps[0]) / 3600  # in hours
    print(f"\nTotal time span: {total_time_span:.2f} hours ({total_time_span*60:.1f} minutes)")
    
    # Show first and last timestamps
    first_time = datetime.fromtimestamp(timestamps[0])
    last_time = datetime.fromtimestamp(timestamps[-1])
    print(f"\nFirst answer: {first_time}")
    print(f"Last answer: {last_time}")
    
    # Analyze intervals by ranges
    print(f"\n=== INTERVAL DISTRIBUTION ===")
    ranges = [
        (0, 0.5, "0-30 seconds"),
        (0.5, 1, "30-60 seconds"),
        (1, 2, "1-2 minutes"),
        (2, 5, "2-5 minutes"),
        (5, 10, "5-10 minutes"),
        (10, float('inf'), "10+ minutes")
    ]
    
    for min_val, max_val, label in ranges:
        count = sum(1 for x in intervals_minutes if min_val <= x < max_val)
        percentage = (count / len(intervals_minutes)) * 100
        print(f"{label}: {count} intervals ({percentage:.1f}%)")
    
    # Find longest and shortest intervals
    longest_idx = intervals_minutes.index(max_interval)
    shortest_idx = intervals_minutes.index(min_interval)
    
    print(f"\n=== EXTREME INTERVALS ===")
    print(f"Longest interval: {max_interval:.2f} minutes (between Q{question_ids[longest_idx]} and Q{question_ids[longest_idx+1]})")
    print(f"Shortest interval: {min_interval:.2f} minutes (between Q{question_ids[shortest_idx]} and Q{question_ids[shortest_idx+1]})")
    
    # Show intervals that are significantly longer than average (> 2x median)
    long_intervals = [(i, interval) for i, interval in enumerate(intervals_minutes) if interval > 2 * median_interval]
    if long_intervals:
        print(f"\n=== LONG INTERVALS (> 2x median) ===")
        for idx, interval in long_intervals:
            print(f"Q{question_ids[idx]} to Q{question_ids[idx+1]}: {interval:.2f} minutes")
    
    # Calculate average time per answer (assuming each answer took roughly the same time)
    # This is a rough estimate since we only have completion timestamps
    estimated_time_per_answer = total_time_span * 60 / len(timestamps)  # in minutes
    print(f"\n=== ESTIMATED TIME PER ANSWER ===")
    print(f"Estimated average time per answer: {estimated_time_per_answer:.2f} minutes ({estimated_time_per_answer*60:.1f} seconds)")
    
    # Show sample of recent intervals
    print(f"\n=== RECENT INTERVALS (last 10) ===")
    for i in range(max(0, len(intervals_minutes)-10), len(intervals_minutes)):
        print(f"Q{question_ids[i]} to Q{question_ids[i+1]}: {intervals_minutes[i]:.2f} minutes")

if __name__ == "__main__":
    detailed_timing_analysis() 