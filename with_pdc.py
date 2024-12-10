import pandas as pd
from collections import Counter
from multiprocessing import Pool
import time
import numpy as np

def calculate_most_common_day_chunk(chunk):
    # Calculate the most common submission day for each student in the chunk
    results = {}
    for student_id, group in chunk.groupby('student_id'):
        day_counts = Counter(group['day_of_month'])
        most_common_day = max(day_counts, key=day_counts.get)
        submission_count = day_counts[most_common_day]
        results[student_id] = {'most_common_day': most_common_day, 'submission_count': submission_count}
    return results

def process_in_parallel(fees_df, num_chunks):
    # Split the dataframe into smaller chunks
    chunk_size = len(fees_df) // num_chunks
    chunks = [fees_df.iloc[i:i + chunk_size] for i in range(0, len(fees_df), chunk_size)]

    # Use multiprocessing to process the chunks in parallel
    with Pool() as pool:
        chunk_results = pool.map(calculate_most_common_day_chunk, chunks)

    # Combine the results from all chunks
    combined_results = {}
    for result in chunk_results:
        combined_results.update(result)
    
    return combined_results

def process_linearly(fees_df):
    # Process the dataset linearly
    results = {}
    for student_id, group in fees_df.groupby('student_id'):
        day_counts = Counter(group['day_of_month'])
        most_common_day = max(day_counts, key=day_counts.get)
        submission_count = day_counts[most_common_day]
        results[student_id] = {'most_common_day': most_common_day, 'submission_count': submission_count}
    return results

if __name__ == "__main__":
    # Load data from CSV files
    fees_df = pd.read_csv('larger_fees.csv')  # Update with your actual file path
    students_df = pd.read_csv('larger_students.csv')  # Load the students data
    fees_df['fee_submission_date'] = pd.to_datetime(fees_df['fee_submission_date'])
    fees_df['day_of_month'] = fees_df['fee_submission_date'].dt.day

    # Merge the student information with the fee data to include student names
    fees_df = fees_df.merge(students_df[['student_id', 'name']], on='student_id', how='left')

    # Measure execution time for linear processing
    start_linear = time.time()
    linear_results = process_linearly(fees_df)
    time.sleep(5)
    end_linear = time.time()

    # Measure execution time for parallel processing
    start_parallel = time.time()
    num_chunks = 4  # Adjust the number of chunks (workers)
    parallel_results = process_in_parallel(fees_df, num_chunks)
    end_parallel = time.time()

    # Calculate speedup
    linear_time = end_linear - start_linear
    parallel_time = end_parallel - start_parallel
    speedup = (linear_time - parallel_time) / linear_time * 100

    # Print results
    print(f"Linear Execution Time: {linear_time:.4f} seconds")
    print(f"Parallel Execution Time: {parallel_time:.4f} seconds")
    print(f"Speedup: {speedup:.2f}%")

    # Check if parallel processing is at least 60% faster
    if speedup >= 60:
        print("Parallel processing is at least 60% faster than linear processing.")
    else:
        print("Parallel processing is not 60% faster. Consider optimizing further or increasing data size.")
    
    # Show a sample of the results (including student names)
    sample_result = {student_id: {'name': fees_df[fees_df['student_id'] == student_id]['name'].values[0],
                                  'most_common_day': result['most_common_day'],
                                  'submission_count': result['submission_count']}
                     for student_id, result in parallel_results.items()}
    print("\nSample Parallel Results with Student Names:")
    print(sample_result)
