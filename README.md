# University Students Dataset Generator

This project generates realistic synthetic data of university students for analysis, visualization, and testing. It uses libraries like `Faker`, `Pandas`, `NumPy`, and `Matplotlib` to simulate attributes such as GPA, academic programs, scholarships, nationality, and much more.

---

##  Usage

### 1. Generate data

```bash
python data.py 1000 
```

Generates a file `output/university_data.csv` with 1000 records.

### 2. Visualize distributions

```bash
python plot2.py output/university_data.csv
```

Generates a file `output/pie_charts_and_distributions.png` with pie charts and KDE distributions.

---

##  Tests

Run the tests with:

```bash
pip install pytest pytest-cov
```

```bash
pytest test_data.py -v --cov=data --cov-report=term-missing
```

Test coverage:

```
Name           Stmts   Miss  Cover   Missing
--------------------------------------------
__init__.py        0      0   100%
data.py           82     10    88%   173-174, 195-198, 208-210, 213
test_data.py     155      4    97%   68, 89-91
--------------------------------------------
TOTAL            237     14    94%

```

---

## Generated Data


# Pie chart
![image](https://github.com/user-attachments/assets/71e8d1bb-119b-4ebb-8aff-8b9f7f316fff)

![image](https://github.com/user-attachments/assets/caf30f0b-6ba8-4b53-9715-cdcef1740b8a)

![image](https://github.com/user-attachments/assets/f207d19f-8599-4f7e-9331-0632ad8d7d65)

![image](https://github.com/user-attachments/assets/ce51c7c0-a80d-4c4c-9d7b-b595977c8407)


# Histograms

![image](https://github.com/user-attachments/assets/cac850a7-d4d9-4bd4-8bef-5f4ff7ac7585)







