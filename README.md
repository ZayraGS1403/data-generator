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

img





