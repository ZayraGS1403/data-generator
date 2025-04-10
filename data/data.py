import csv
import sys
import pandas as pd
import numpy as np
from faker import Faker
from scipy import stats
from datetime import datetime
import os


# Use dynamic current year
current_year = datetime.now().year

fake = Faker()

def generate_university_students_data(row_count):
    """
    Generate university-related pseudorandom data
    """
    data = {
        'student_id': [f'STU{str(i).zfill(6)}' for i in range(row_count)],  # Unique key
        'first_name': [],
        'last_name': [fake.last_name() for _ in range(row_count)],
        'type_id_number': [],
        'identification_number': [],
        'date_of_birth': [fake.date_of_birth(minimum_age=16, maximum_age=25) for _ in range(row_count)],
        'email': [],
        'address': [],
        'gender': [],
        'nationality': [],
        'country_code': [],
        'phone_number': [],
        'program': [],
        'state_program': [],
        'current_semester': [],
        'Number_of_credits_approved': [],  # Will use Cauchy ("cake") distribution
        'credits_remaining': [],
        'GPA': [],
        'enrollment_date': [fake.date_between(start_date='-4y', end_date='today') for _ in range(row_count)],
        'student_status': [],
        'advisor_id': [f'ADV{str(i).zfill(4)}' for i in np.random.randint(1, 50, row_count)],
        'advisor_name': [fake.name() for _ in range(row_count)],
        'scholarship': [],
        'payment_status': np.random.choice(['Paid', 'Pending', 'Late'], row_count),
        'academic_standing': [],
        'course_load': [],
        'marital_status': [],
        'library_books_borrowed': np.random.poisson(lam=3, size=row_count)
    }

    # Generate gender and corresponding first name using np.random.choice
    genders = np.random.choice(['Male', 'Female', 'Other'], size=row_count, p=[0.45, 0.45, 0.1])
    data['gender'] = genders
    for i in range(row_count):
        gender = data['gender'][i]
        if gender == 'Male':
            data['first_name'].append(fake.first_name_male())
        elif gender == 'Female':
            data['first_name'].append(fake.first_name_female())
        else:
            data['first_name'].append(fake.first_name_nonbinary())

    # Related columns: email based on name
    for i in range(row_count):
        data['email'].append(
            f"{data['first_name'][i].lower()}.{data['last_name'][i].lower()}@university.edu.co"
        )

    # Populate remaining columns
    data['address'] = [fake.address().replace('\n', ', ') for _ in range(row_count)]

    # Type ID number and age relationship
    for i in range(row_count):
        age = current_year - data['date_of_birth'][i].year
        if 16 <= age <= 17:
            data['type_id_number'].append('TI')
        else:
            data['type_id_number'].append('CC')

    # Identification number: 8 to 10 digits
    data['identification_number'] = np.random.randint(10000000, 9999999999, size=row_count, dtype=np.int64)

    data['program'] = np.random.choice([
        'Computer Science', 'Software Engineering', 'Information Technology', 'Data Science',
        'Cybersecurity', 'Artificial Intelligence', 'Engineering', 'Mechanical Engineering',
        'Electrical Engineering', 'Civil Engineering', 'Industrial Engineering', 'Biology',
        'Chemistry', 'Biotechnology', 'Medicine', 'Nursing', 'Pharmacy', 'Psychology',
        'Sociology', 'Anthropology', 'Political Science', 'Philosophy', 'History',
        'Business Administration', 'Marketing', 'Accounting', 'Economics', 'Finance',
        'Entrepreneurship', 'Graphic Design', 'Architecture', 'Music', 'International Relations'
    ], row_count)

    # Total credits required for degree (random between 140 and 180)
    total_credits = np.random.randint(140, 181, size=row_count)

    # Current semester and Number of credits approved relationship
    data['current_semester'] = np.random.randint(1, 9, row_count)  # Assuming 8 semesters max for undergrad
    data['Number_of_credits_approved'] = [
        int(np.clip(stats.cauchy.rvs(loc=sem * 18, scale=5), 0, min(sem * 18 + 18, total_credits[i])))
        for i, sem in enumerate(data['current_semester'])
    ]

    # Credits remaining
    data['credits_remaining'] = [max(0, total_credits[i] - credits) for i, credits in enumerate(data['Number_of_credits_approved'])]

    # GPA with normal distribution (mean=3.5, std=0.5)
    data['GPA'] = np.clip(np.random.normal(loc=3.5, scale=0.5, size=row_count), 2.0, 5.0)

    # Academic standing based on GPA
    data['academic_standing'] = np.where(
        data['GPA'] >= 4.5, 'Excellent',
        np.where(data['GPA'] >= 4.0, 'Good',
                 np.where(data['GPA'] >= 3.0, 'Average', 'Poor'))
    )

    # Scholarship as boolean based on GPA
    data['scholarship'] = data['GPA'] >= 4.5

    # Course load (number of credits currently enrolled in)
    data['course_load'] = np.random.randint(15, 21, row_count)  # Typical course load per semester

    # Marital status (fixed probabilities)
    data['marital_status'] = np.random.choice(['Single', 'Married', 'Divorced'], row_count, p=[0.9, 0.08, 0.02])

    # State program
    data['state_program'] = np.random.choice(['Enrolled', 'Suspended', 'Withdrawn'], row_count, p=[0.7, 0.15, 0.15])

    # Student status based on state_program
    data['student_status'] = ['Active' if state == 'Enrolled' else 'Inactive' for state in data['state_program']]

    # Nationality: Mostly Colombian
    nationalities = ['Colombia'] * 80 + ['USA', 'Brazil', 'Argentina', 'Spain', 'Mexico', 'Peru', 'Chile', 'Ecuador', 'Venezuela'] * 2
    data['nationality'] = np.random.choice(nationalities, row_count)

    # Country code and phone number based on nationality
    country_codes = {
        'Colombia': '+57',
        'USA': '+1',
        'Brazil': '+55',
        'Argentina': '+54',
        'Spain': '+34',
        'Mexico': '+52',
        'Peru': '+51',
        'Chile': '+56',
        'Ecuador': '+593',
        'Venezuela': '+58'
    }
    phone_starts = {
        'Colombia': ['3'],
        'USA': ['2', '3', '4', '5', '6', '7', '8', '9'],
        'Brazil': ['9'],
        'Argentina': ['9'],
        'Spain': ['6', '7'],
        'Mexico': ['2', '3', '4', '5', '6', '7', '8', '9'],
        'Peru': ['9'],
        'Chile': ['9'],
        'Ecuador': ['9'],
        'Venezuela': ['4']
    }

    for i in range(row_count):
        nationality = data['nationality'][i]
        data['country_code'].append(country_codes[nationality])
        start_digit = np.random.choice(phone_starts[nationality])
        remaining_digits = np.random.randint(100000000, 999999999)  # 9 digits
        data['phone_number'].append(f"{start_digit}{remaining_digits}")

    return pd.DataFrame(data)

def main():
    # Check for correct number of arguments
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <row_count> [output_path]")
        sys.exit(1)

    try:
        # Get row count from command-line argument
        row_count = int(sys.argv[1])
        if row_count <= 0:
            raise ValueError("Row count must be positive")

        # Generate the data
        df = generate_university_students_data(row_count)

        # Determine the output path
        if len(sys.argv) == 3:
            # If output path is provided as an argument
            output_path = sys.argv[2]
            # Ensure the directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            # Default: save in an 'output' subdirectory
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, 'university_data.csv')

        # Save the DataFrame to CSV
        df.to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Generated {row_count} rows of university data and saved to '{output_path}'")
        print(f"Current working directory: {os.getcwd()}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()