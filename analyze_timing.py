#!/usr/bin/env python3
import json
import statistics
from datetime import datetime

def analyze_timing():
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
    
    # Calculate total time span
    total_time_span = (timestamps[-1] - timestamps[0]) / 3600  # in hours
    
    print(f"Timing Analysis for {len(timestamps)} answers:")
    print(f"Total time span: {total_time_span:.2f} hours")
    print(f"Average time between answers: {avg_interval:.2f} minutes")
    print(f"Median time between answers: {median_interval:.2f} minutes")
    print(f"Minimum interval: {min_interval:.2f} minutes")
    print(f"Maximum interval: {max_interval:.2f} minutes")
    
    # Show first and last timestamps
    first_time = datetime.fromtimestamp(timestamps[0])
    last_time = datetime.fromtimestamp(timestamps[-1])
    print(f"\nFirst answer: {first_time}")
    print(f"Last answer: {last_time}")
    
    # Show some specific intervals
    print(f"\nSample intervals (first 10):")
    for i in range(min(10, len(intervals_minutes))):
        print(f"  Q{question_ids[i]} to Q{question_ids[i+1]}: {intervals_minutes[i]:.2f} minutes")
    
    # Find longest and shortest intervals
    longest_idx = intervals_minutes.index(max_interval)
    shortest_idx = intervals_minutes.index(min_interval)
    
    print(f"\nLongest interval: {max_interval:.2f} minutes (between Q{question_ids[longest_idx]} and Q{question_ids[longest_idx+1]})")
    print(f"Shortest interval: {min_interval:.2f} minutes (between Q{question_ids[shortest_idx]} and Q{question_ids[shortest_idx+1]})")

if __name__ == "__main__":
    analyze_timing() 