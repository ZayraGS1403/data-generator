import csv

import pandas as pd
import numpy as np
from datetime import datetime
from data.data import generate_university_students_data, main  # Import the functions from data.py
from unittest.mock import patch, MagicMock
import os
import sys

# Use dynamic current year for age calculations
current_year = datetime.now().year

class TestUniversityStudentsData:
    def test_unique_student_id(self):
        df = generate_university_students_data(100)
        assert len(df['student_id'].unique()) == len(df), "Student IDs should be unique"

    def test_row_count(self):
        row_count = 50
        df = generate_university_students_data(row_count)
        assert len(df) == row_count, "Row count does not match the input"

    def test_email_format(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            expected_email = f"{df['first_name'][i].lower()}.{df['last_name'][i].lower()}@university.edu.co"
            assert df['email'][i] == expected_email, "Email should match first_name.last_name@university.edu.co"

    def test_academic_standing(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            if df['GPA'][i] >= 4.5:
                assert df['academic_standing'][i] == 'Excellent', "Academic standing should be 'Excellent' for GPA >= 4.5"
            elif df['GPA'][i] >= 4.0:
                assert df['academic_standing'][i] == 'Good', "Academic standing should be 'Good' for 4.0 <= GPA < 4.5"
            elif df['GPA'][i] >= 3.0:
                assert df['academic_standing'][i] == 'Average', "Academic standing should be 'Average' for 3.0 <= GPA < 4.0"
            else:
                assert df['academic_standing'][i] == 'Poor', "Academic standing should be 'Poor' for GPA < 3.0"

    def test_scholarship(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            if df['GPA'][i] >= 4.5:
                assert df['scholarship'][i] == True, "Scholarship should be True for GPA >= 4.5"
            else:
                assert df['scholarship'][i] == False, "Scholarship should be False for GPA < 4.5"


    def test_identification_number(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            assert 8 <= len(str(df['identification_number'][i])) <= 10, "Identification number should be 8 to 10 digits"

    def test_phone_number_and_country_code(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            nationality = df['nationality'][i]
            country_code = df['country_code'][i]
            phone = df['phone_number'][i]
            assert len(phone) == 10, "Phone number should be 10 digits"
            assert phone.isdigit(), "Phone number should contain only digits"
            if nationality == 'Colombia':
                assert country_code == '+57', "Colombian students should have country code +57"
                assert phone.startswith('3'), "Colombian phone numbers should start with 3"
            elif nationality == 'USA':
                assert country_code == '+1', "USA students should have country code +1"
            elif nationality == 'Brazil':
                assert country_code == '+55', "Brazilian students should have country code +55"
                assert phone.startswith('9'), "Brazilian phone numbers should start with 9"
            elif nationality == 'Argentina':
                assert country_code == '+54', "Argentinian students should have country code +54"
                assert phone.startswith('9'), "Argentinian phone numbers should start with 9"
            elif nationality == 'Spain':
                assert country_code == '+34', "Spanish students should have country code +34"
                assert phone.startswith(('6', '7')), "Spanish phone numbers should start with 6 or 7"
            elif nationality == 'Mexico':
                assert country_code == '+52', "Mexican students should have country code +52"
            elif nationality == 'Peru':
                assert country_code == '+51', "Peruvian students should have country code +51"
                assert phone.startswith('9'), "Peruvian phone numbers should start with 9"
            elif nationality == 'Chile':
                assert country_code == '+56', "Chilean students should have country code +56"
                assert phone.startswith('9'), "Chilean phone numbers should start with 9"
            elif nationality == 'Ecuador':
                assert country_code == '+593', "Ecuadorian students should have country code +593"
                assert phone.startswith('9'), "Ecuadorian phone numbers should start with 9"
            elif nationality == 'Venezuela':
                assert country_code == '+58', "Venezuelan students should have country code +58"
                assert phone.startswith('4'), "Venezuelan phone numbers should start with 4"

    def test_state_program_and_student_status(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            if df['state_program'][i] == 'Enrolled':
                assert df['student_status'][i] == 'Active', "Students with state_program 'Enrolled' should have student_status 'Active'"
            else:
                assert df['student_status'][i] == 'Inactive', "Students with state_program not 'Enrolled' should have student_status 'Inactive'"

    def test_gender_distribution(self):
        df = generate_university_students_data(100)
        male_count = len(df[df['gender'] == 'Male'])
        female_count = len(df[df['gender'] == 'Female'])
        other_count = len(df[df['gender'] == 'Other'])
        assert 0 < male_count < 100, "There should be some male students"
        assert 0 < female_count < 100, "There should be some female students"
        assert 0 <= other_count <= 20, "There should be a small number of 'Other' gender students"

    def test_type_id_number_and_age(self):
        df = generate_university_students_data(100)
        for i in range(len(df)):
            age = current_year - df['date_of_birth'][i].year
            if 16 <= age <= 17:
                assert df['type_id_number'][i] == 'TI', "Students aged 16-17 should have type_id_number 'TI'"
            else:
                assert df['type_id_number'][i] == 'CC', "Students over 18 should have type_id_number 'CC'"

    def test_nationality_distribution(self):
        df = generate_university_students_data(100)
        colombian_count = len(df[df['nationality'] == 'Colombia'])
        assert colombian_count >= 70, "At least 70% of students should be Colombian"

    def test_gpa_range(self):
        df = generate_university_students_data(100)
        assert df['GPA'].min() >= 2.0, "GPA should be at least 2.0"
        assert df['GPA'].max() <= 5.0, "GPA should be at most 5.0"

    def test_course_load_range(self):
        df = generate_university_students_data(100)
        assert df['course_load'].min() >= 15, "Course load should be at least 15"
        assert df['course_load'].max() <= 20, "Course load should be at most 20"

    def test_payment_status_values(self):
        df = generate_university_students_data(100)
        valid_values = {'Paid', 'Pending', 'Late'}
        assert all(status in valid_values for status in df['payment_status']), "Payment status should be 'Paid', 'Pending', or 'Late'"

    def test_library_books_borrowed(self):
        df = generate_university_students_data(100)
        assert df['library_books_borrowed'].min() >= 0, "Library books borrowed should be non-negative"

    def test_marital_status_values(self):
        df = generate_university_students_data(100)
        valid_values = {'Single', 'Married', 'Divorced'}
        assert all(status in valid_values for status in df['marital_status']), "Marital status should be 'Single', 'Married', or 'Divorced'"

    # New tests to increase coverage
    def test_advisor_id_format(self):
        df = generate_university_students_data(100)
        for advisor_id in df['advisor_id']:
            assert advisor_id.startswith('ADV'), "Advisor ID should start with 'ADV'"
            assert len(advisor_id) == 7, "Advisor ID should be 7 characters long (ADV + 4 digits)"
            assert advisor_id[3:].isdigit(), "Advisor ID should have 4 digits after 'ADV'"

    def test_advisor_name_not_empty(self):
        df = generate_university_students_data(100)
        assert all(name != '' for name in df['advisor_name']), "Advisor name should not be empty"

    def test_enrollment_date_range(self):
        df = generate_university_students_data(100)
        start_date = datetime.now().year - 4
        end_date = datetime.now().year
        for date in df['enrollment_date']:
            assert start_date <= date.year <= end_date, "Enrollment date should be within the last 4 years"


    def test_main_with_invalid_row_count(self):
        with patch('sys.argv', ['data.py', '0']):
            with patch('sys.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    main()
                    mock_print.assert_called_with("Error: Row count must be positive")
                    mock_exit.assert_called_with(1)


    def test_main_with_custom_output_path(self):
        with patch('sys.argv', ['data.py', '10', 'custom/path/data.csv']):
            with patch('pandas.DataFrame.to_csv') as mock_to_csv:
                with patch('os.makedirs') as mock_makedirs:
                    with patch('os.path.exists', return_value=False) as mock_exists:
                        with patch('builtins.print') as mock_print:
                            main()
                            mock_to_csv.assert_called_once_with('custom/path/data.csv', index=False, quoting=csv.QUOTE_ALL)
                            mock_makedirs.assert_called_once()
                            mock_print.assert_any_call("Generated 10 rows of university data and saved to 'custom/path/data.csv'")
                            mock_print.assert_any_call(f"Current working directory: {os.getcwd()}")

