import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import seaborn as sns

def plot_pie_charts_and_distributions(csv_path):
    """
    Generate pie charts for categorical columns and histograms with KDE for numerical columns.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    categorical_columns = [
        'gender', 'nationality', 'state_program', 'student_status',
        'academic_standing', 'payment_status', 'marital_status', 'scholarship'
    ]

    numerical_columns = [
        'GPA', 'library_books_borrowed'
    ]

    fig, axes = plt.subplots(3, 4, figsize=(24, 18))
    axes = axes.flatten()

    for idx, column in enumerate(categorical_columns):
        value_counts = df[column].value_counts()
        labels = value_counts.index
        sizes = value_counts.values
        percentages = 100. * sizes / sizes.sum()

        axes[idx].pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            labeldistance=1.1,
            pctdistance=0.85,
            textprops={'fontsize': 10}
        )
        axes[idx].set_title(f'Distribution of {column}')
        axes[idx].axis('equal')

    for idx, column in enumerate(numerical_columns, start=len(categorical_columns)):
        sns.histplot(
            df[column],
            kde=True,
            stat="density",
            linewidth=0,
            color='skyblue',
            ax=axes[idx]
        )
        if column == 'GPA':
            mean_gpa = 3.5
            std_gpa = 0.5
            x = np.linspace(2.0, 5.0, 100)
            p = norm.pdf(x, loc=mean_gpa, scale=std_gpa)
            axes[idx].plot(x, p, 'r-', lw=2, label=f'Theoretical Normal\n(μ={mean_gpa}, σ={std_gpa})')
            axes[idx].legend()
        axes[idx].set_title(f'Distribution of {column}')
        axes[idx].set_xlabel(column)
        axes[idx].set_ylabel('Density')
        axes[idx].grid(True, alpha=0.3)

    for ax in axes[10:]:
        ax.axis('off')

    plt.tight_layout()
    output_path = 'output/pie_charts_and_distributions.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Charts saved to '{output_path}'")

def main():
    if len(sys.argv) != 2:
        print("Usage: python plot.py <csv_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    plot_pie_charts_and_distributions(csv_path)

if __name__ == "__main__":
    main()
