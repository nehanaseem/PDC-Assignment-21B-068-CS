import pandas as pd
from collections import Counter

# Load the CSV files
fees_df = pd.read_csv('fees.csv')  # Replace with the path to your 'fees.csv' file
students_df = pd.read_csv('students.csv')  # Replace with the path to your 'students.csv' file

# Convert 'fee_submission_date' to datetime format
fees_df['fee_submission_date'] = pd.to_datetime(fees_df['fee_submission_date'])

# Extract the day of the month from the 'fee_submission_date'
fees_df['day_of_month'] = fees_df['fee_submission_date'].dt.day

# Group the data by student and analyze each student's fee submission days
results = {}
for student_id, group in fees_df.groupby('student_id'):
    # Count the frequency of each day for the student
    day_counts = Counter(group['day_of_month'])
    # Find the most common day and the number of submissions
    most_common_day = max(day_counts, key=day_counts.get)
    submission_count = day_counts[most_common_day]
    # Store the results for the student
    results[student_id] = {
        'most_common_day': most_common_day,
        'submission_count': submission_count
    }

# Display results for each student
print("Analysis of Fee Submission Days (Individual Students):")
for student_id, data in results.items():
    print(f"Student ID: {student_id}")
    print(f"  Most common fee submission day: {data['most_common_day']}")
    print(f"  Number of submissions on that day: {data['submission_count']}")
    print()
