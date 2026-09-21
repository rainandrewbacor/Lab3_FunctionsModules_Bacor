# This file contains the main processes for running the monitoring pipeline.
# This monitors, handles errors, recurses abnormal readings, and displays the final diagnostic report.
import random
from generator import generate_data 
from generator import transform_data

LAST_NAME = "Bacor"
STUDENT_ID = "TUPM-26-1879"
SEED_NUM = int(STUDENT_ID[-1])
ID_SUM = sum(int(d) for d in STUDENT_ID if d.isdigit())
NAME_LENGTH = len(LAST_NAME)
FAVORITE_ARTIST = "IVOS"
ARTIST_LENGTH = len(FAVORITE_ARTIST)

random.seed(SEED_NUM)
limits = (SEED_NUM + NAME_LENGTH + ARTIST_LENGTH) * 5

def process_monitor(func):
    def wrapper(*args, **kwargs):
        # Display prompt first, then run the function
        print(f"Monitoring Started. Logged in as {LAST_NAME}")
        print(f"Monitoring... Currently Executing: {func.__name__}")
        result = func(*args, **kwargs)
        # Once done, display prompt again
        print(f"Done Executing: {func.__name__}")
        return result
    return wrapper

def trace_abnormalities(reading, level=1):
    print(f"Entering with {reading}, at level {level}")
    if reading <= limits:
        print(f"Base case reached at: {reading} in level {level}")
        return "Done!"

    try: 
        result = trace_abnormalities(reading // 3, level  + 1)
    except:
        print(f"Exception caught at reading {reading}")
    print(f"Current entering with {reading} at level {level}")
    return result

    
    
@process_monitor
def run_pipeline():
    stream = generate_data(limit=limits, num_data=10)
    total_processed = []
    valid_results = []
    invalid_results = []
    valid_reading = []
    abnormal_reading = []
    invalid_unexpected = []

    for raw_data in stream:
        total_processed.append(raw_data)
        try:
            transform_data(raw_data)

            if raw_data < limits:
                valid_reading.append(raw_data)
                valid_results.append(raw_data)
            else:
                abnormal_reading.append(raw_data)
                invalid_results.append(raw_data)
                print("=" * 40)
                print(f"RECURSIVE ANALYSIS")
                trace_abnormalities(reading=raw_data)
                print("=" * 40)
        except TypeError:
            invalid_results.append(raw_data)
            invalid_unexpected.append(raw_data)
            print(f"Wrong/Corrupt data type detected in {raw_data}")
        except ValueError:
            invalid_results.append(raw_data)
            invalid_unexpected.append(raw_data)
            print(f"Wrong data value detected in {raw_data}")
    return total_processed, valid_results, invalid_results, valid_reading, abnormal_reading, invalid_unexpected

total, val_r, inval_r, valid, abnormal, inval_unexpected = run_pipeline()

if len(abnormal) > 4:
    abnormal_severity = "CRITICAL"
elif len(abnormal) > 2:
    abnormal_severity = "WARNING"
else:
    abnormal_severity = "OPTIMAL"

if len(inval_unexpected) > 3:
    unex_severity = "CRITICAL"
elif len(inval_unexpected) > 1:
    unex_severity = "WARNING"
else:
    unex_severity = "OPTIMAL"

if (unex_severity or abnormal_severity) == "CRITICAL":
    system_state = "CRITICAL CONDITION. PLEASE GIVE IMMEDIATE ATTENTION."
if (unex_severity or abnormal_severity) == "WARNING":
    system_state = "WARNING. ELEVATED THREAT."
if (unex_severity or abnormal_severity) == "OPTIMAL":
    system_state = "Optimal condition"

print()
print(f"--- DIAGNOSTIC SUMMARY ---")
print("=" * 40)
print(f"Total Readings: {len(total)}")
print(f"Processed Results: {', '.join(map(str, total))}")
print(f"Valid Results: {', '.join(map(str, val_r))}")
print(f"Invalid Results: {', '.join(map(str, inval_r))}")
print("=" * 40)
print(f"DATA CLASSIFICATIONS")
print(f"Valid Readings: {', '.join(map(str, valid))}")
print(f"Invalid/Unexpected Readings: {', '.join(map(str, inval_unexpected))}")
print(f"Abnormal Readings: {', '.join(map(str, abnormal))}")
print("=" * 40)
print(f"Status: {system_state}")