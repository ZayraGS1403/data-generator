import csv
import sys
import pandas as pd
import numpy as np
from faker import Faker
from scipy import stats
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta

current_year = datetime.now().year

fake = Faker()

def generate_university_students_data(row_count):
    """
    Generate university-related pseudorandom data
    """
    data = {
        'student_id': [f'STU{str(i).zfill(6)}' for i in range(row_count)],
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
        'Number_of_credits_approved': [],
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

    """
    Generate random data, according the gender if the name
    """
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

    """
    Generate random data, according the first name and last name
    """
    for i in range(row_count):
        data['email'].append(
            f"{data['first_name'][i].lower()}.{data['last_name'][i].lower()}@university.edu.co"
        )

    """
    Generate random address
    """
    data['address'] = [fake.address().replace('\n', ', ') for _ in range(row_count)]

    """
    Generate random data, according the age of the student
    """
    for i in range(row_count):
        age = current_year - data['date_of_birth'][i].year
        if 16 <= age <= 17:
            data['type_id_number'].append('TI')
        else:
            data['type_id_number'].append('CC')

    """
    Generate random data, according the type of id number
    """
    data['identification_number'] = np.random.randint(10000000, 9999999999, size=row_count, dtype=np.int64)

    """
    Generate random programs
    """
    data['program'] = np.random.choice([
        'Computer Science', 'Software Engineering', 'Information Technology', 'Data Science',
        'Cybersecurity', 'Artificial Intelligence', 'Engineering', 'Mechanical Engineering',
        'Electrical Engineering', 'Civil Engineering', 'Industrial Engineering', 'Biology',
        'Chemistry', 'Biotechnology', 'Medicine', 'Nursing', 'Pharmacy', 'Psychology',
        'Sociology', 'Anthropology', 'Political Science', 'Philosophy', 'History',
        'Business Administration', 'Marketing', 'Accounting', 'Economics', 'Finance',
        'Entrepreneurship', 'Graphic Design', 'Architecture', 'Music', 'International Relations'
    ], row_count)

    """
    Generate randon number total credits
    """
    total_credits = np.random.randint(140, 181, size=row_count)

    """
    Generate random enrollment date and calculate current semester 
    """
    current_date = datetime.now()
    for i in range(row_count):
        enrollment_date = data['enrollment_date'][i] if isinstance(data['enrollment_date'][i], datetime) else datetime.strptime(str(data['enrollment_date'][i]), '%Y-%m-%d')
        delta = relativedelta(current_date, enrollment_date)
        months_passed = delta.years * 12 + delta.months
        semesters_passed = months_passed // 6
        data['current_semester'].append(min(10, max(1, semesters_passed + 1)))

    """
    Generate random number of credits approved, according the current semester
    """
    data['Number_of_credits_approved'] = [
        int(np.clip(stats.cauchy.rvs(loc=sem * 18, scale=5), 0, min(sem * 18 + 18, total_credits[i])))
        for i, sem in enumerate(data['current_semester'])
    ]

    """
    Generate random number of credits remaining, according the total credits and number of credits approved
    """
    data['credits_remaining'] = [max(0, total_credits[i] - credits) for i, credits in enumerate(data['Number_of_credits_approved'])]

    """
    Generate random GPA
    """
    data['GPA'] = np.clip(np.random.normal(loc=3.5, scale=0.5, size=row_count), 2.0, 5.0)

    """
    Generate random data, according the GPA its classification
    """
    data['academic_standing'] = np.where(
        data['GPA'] >= 4.5, 'Excellent',
        np.where(data['GPA'] >= 4.0, 'Good',
                 np.where(data['GPA'] >= 3.0, 'Average', 'Poor'))
    )

    """
    if the GPA is less than 3.0, the student is not eligible for a scholarship
    """
    data['scholarship'] = data['GPA'] >= 4.5

    """
    Generate random data about the corse load
    """
    data['course_load'] = np.random.randint(15, 21, row_count)

    """
    Generate random data about the marital status
    """
    data['marital_status'] = np.random.choice(['Single', 'Married', 'Divorced'], row_count, p=[0.9, 0.08, 0.02])

    """
    Generate random data about the state of the program
    """
    data['state_program'] = np.random.choice(['Enrolled', 'Suspended', 'Withdrawn'], row_count, p=[0.7, 0.15, 0.15])

    """
    The student status is active or inactive, according the state of the program
    """
    data['student_status'] = ['Active' if state == 'Enrolled' else 'Inactive' for state in data['state_program']]

    """
    Generate nationalities random with a higher probability of being Colombian
    """
    nationalities = ['Colombia'] * 80 + ['USA', 'Brazil', 'Argentina', 'Spain', 'Mexico', 'Peru', 'Chile', 'Ecuador', 'Venezuela'] * 2
    data['nationality'] = np.random.choice(nationalities, row_count)

    """
    Generate random data about the phone number, according the country code and the first digit
    """
    country_codes = {
        'Colombia': '+57', 'USA': '+1', 'Brazil': '+55', 'Argentina': '+54', 'Spain': '+34',
        'Mexico': '+52', 'Peru': '+51', 'Chile': '+56', 'Ecuador': '+593', 'Venezuela': '+58'
    }
    phone_starts = {
        'Colombia': ['3'], 'USA': ['2', '3', '4', '5', '6', '7', '8', '9'], 'Brazil': ['9'],
        'Argentina': ['9'], 'Spain': ['6', '7'], 'Mexico': ['2', '3', '4', '5', '6', '7', '8', '9'],
        'Peru': ['9'], 'Chile': ['9'], 'Ecuador': ['9'], 'Venezuela': ['4']
    }

    """
    Generate random phone numbers, according the country code and the first digit
    """
    for i in range(row_count):
        nationality = data['nationality'][i]
        data['country_code'].append(country_codes[nationality])
        start_digit = np.random.choice(phone_starts[nationality])
        remaining_digits = np.random.randint(100000000, 999999999)
        data['phone_number'].append(f"{start_digit}{remaining_digits}")

    return pd.DataFrame(data)

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <row_count> [output_path]")
        sys.exit(1)

    try:
        row_count = int(sys.argv[1])
        if row_count <= 0:
            raise ValueError("Row count must be positive")

        df = generate_university_students_data(row_count)

        if len(sys.argv) == 3:
            output_path = sys.argv[2]
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, 'university_data.csv')

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
