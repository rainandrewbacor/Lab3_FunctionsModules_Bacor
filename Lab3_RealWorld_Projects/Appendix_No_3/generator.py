# This file generates and transforms the telemetry data.
import random
## DEFINING OF VARIABLES
LAST_NAME = "Bacor"
STUDENT_ID = "TUPM-26-1879"
SEED_NUM = int(STUDENT_ID[-1])
ID_SUM = sum(int(d) for d in STUDENT_ID if d.isdigit())
NAME_LENGTH = len(LAST_NAME)
FAVORITE_ARTIST = "IVOS"
ARTIST_LENGTH = len(FAVORITE_ARTIST)

random.seed(SEED_NUM)
limit = (SEED_NUM + NAME_LENGTH + ARTIST_LENGTH) * 5

def process_monitor(func):
    def wrapper(*args, **kwargs):
        # Display prompt first, then run the function
        print(f"Monitoring... Currently Executing: {func.__name__}")
        result = func(*args, **kwargs)
        # Once done, display prompt again
        print(f"Done Executing: {func.__name__}")
        return result
    return wrapper

@process_monitor
def generate_data(limit, num_data):
    for _ in range(num_data):
        # Generate Random Input
        output = random.randint(1, limit)

        # Perform error roll. 
        error_roll = random.random()

        ## INVALID/UNEXPECTED NUMBERS
        if error_roll < 0.05:
            # 5% chance to output invalid data type (str)
            yield "INVALID DATA"
        elif error_roll < 0.10:
            # 10% chance to output. 
            # Simulate missing values in stream.
            yield None

        ## ABNORMAL NUMBERS
        if error_roll < 0.15:
            # 15% chance to output out of bounds.
            yield random.randint(100, 500)

        # no need for negative since we only generated from 1 to the limit.
        yield output

# Transforms the data by dividing to 10 and rounding off to 2 decimals, if it is a float.
transform_data = lambda x: round(x / 10.0, 2) if isinstance(x, (float)) else x
        
