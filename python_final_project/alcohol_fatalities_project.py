"""
File name: alcohol_fatalities_project.py
Name: Lahari Bathula (Section A)
Project: Python Final Project
Title: Global Alcohol-Related Road Fatalities Analysis Using Python
Dataset: global_alcohol_fatalities_1970_2024.csv

# Description:
    This program analyzes alcohol-related road traffic fatalities
across six countries: USA, Canada, Great Britain, Australia,
Germany, and India.

# Topics:
  Functions, Lists, Loops, Decisions, Dictionaries,
Classes, Objects, Recursion, File Handling, Exception Handling,
Pandas, Statistics and Plots

"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "global_alcohol_fatalities_1970_2024.csv"

COUNTRIES = [
    "USA",
    "Canada",
    "Great_Britain",
    "Australia",
    "Germany",
    "India"
]


# ----------------------------------------
# RECURSION
# ----------------------------------------

def recursive_total(numbers):
    # Base case
    if len(numbers) == 0:
        return 0

    # Recursive case
    return numbers[0] + recursive_total(numbers[1:])


# ----------------------------------------
# CLASS AND OBJECTS
# ----------------------------------------

class FatalityAnalyzer:

    def __init__(self, filename=FILE_NAME):
        self.file_path = Path(__file__).resolve().parent / filename
        self.df = None

    # ------------------------------------
    # 1. LOAD CSV DATA
    # ------------------------------------

    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)

            required = ["Year"]

            for country in COUNTRIES:
                required.extend([
                    country + "_Total_Road_Deaths",
                    country + "_Alcohol_Related_Deaths",
                    country + "_Male_Alcohol_Deaths",
                    country + "_Female_Alcohol_Deaths",
                    country + "_Alcohol_Rate_Percent"
                ])

            missing = [
                column for column in required
                if column not in df.columns
            ]

            if missing:
                print("Missing columns:", missing)
                return False

            for column in required:
                df[column] = pd.to_numeric(
                    df[column], errors="raise"
                )

            if df.empty:
                print("Dataset is empty.")
                return False

            if df[required].isna().any().any():
                print("Dataset contains missing values.")
                return False

            if df["Year"].duplicated().any():
                print("Dataset contains duplicate years.")
                return False

            if (df[required[1:]] < 0).any().any():
                print("Dataset contains negative values.")
                return False

            for country in COUNTRIES:
                total = df[country + "_Total_Road_Deaths"]
                alcohol = df[country + "_Alcohol_Related_Deaths"]
                male = df[country + "_Male_Alcohol_Deaths"]
                female = df[country + "_Female_Alcohol_Deaths"]
                rate = df[country + "_Alcohol_Rate_Percent"]

                if (male + female != alcohol).any():
                    print("Inconsistent gender totals:", country)
                    return False

                if (alcohol > total).any():
                    print("Invalid fatality totals:", country)
                    return False

                if ((rate < 0) | (rate > 100)).any():
                    print("Invalid alcohol percentage:", country)
                    return False

            self.df = df.sort_values(
                "Year"
            ).reset_index(drop=True)

            print("\nDataset loaded successfully!")
            print("Total rows:", len(self.df))
            print("Total columns:", len(self.df.columns))

            return True

        except FileNotFoundError:
            print("\nError: CSV file not found.")
            print("Expected file:", self.file_path)
            print("Place the CSV beside the Python program.")

        except (ValueError, TypeError) as error:
            print("Invalid dataset:", error)

        except (OSError, pd.errors.ParserError,
                pd.errors.EmptyDataError) as error:
            print("Unable to read CSV:", error)

        return False

    # ------------------------------------
    # SELECT COUNTRY
    # ------------------------------------

    def choose_country(self):
        print("\nAvailable Countries:")

        for i, country in enumerate(COUNTRIES, 1):
            print(i, ".", country.replace("_", " "))

        try:
            choice = int(input("Choose country (1-6): "))

            if 1 <= choice <= len(COUNTRIES):
                return COUNTRIES[choice - 1]

            print("Invalid country number.")

        except ValueError:
            print("Please enter a valid number.")

        return None

    # ------------------------------------
    # SELECT YEAR
    # ------------------------------------

    def choose_year(self):
        try:
            year = int(input("Enter year: "))

            if year in self.df["Year"].values:
                return year

            print("Year not found in dataset.")

        except ValueError:
            print("Please enter a valid year.")

        return None

    # ------------------------------------
    # 1. SHOW FIRST FIVE ROWS
    # ------------------------------------
    def show_data(self):
        print("\nFIRST FIVE ROWS")
        print("-----------------------------------")
        country = self.choose_country()
        if country is None:
            return
        columns = [
            "Year",
            country + "_Total_Road_Deaths",
            country + "_Alcohol_Related_Deaths",
            country + "_Male_Alcohol_Deaths",
            country + "_Female_Alcohol_Deaths",
            country + "_Alcohol_Rate_Percent"
        ]
        data = self.df[columns].head().copy()
        data.columns = [
            "Year",
            "Total Deaths",
            "Alcohol Deaths",
            "Male Deaths",
            "Female Deaths",
            "Alcohol Rate (%)"
        ]
        print("\nCountry:", country.replace("_", " "))
        print(data.to_string(index=False))



    # ------------------------------------
    # 2. DATASET INFORMATION
    # ------------------------------------

    def show_info(self):
        print("\nDATASET INFORMATION")

        print("Rows:", len(self.df))
        print("Columns:", len(self.df.columns))

        print(
            "Years:",
            int(self.df["Year"].min()),
            "to",
            int(self.df["Year"].max())
        )

        print("Countries:")

        for country in COUNTRIES:
            print(country.replace("_", " "))

        print(
            "Missing values:",
            int(self.df.isna().sum().sum())
        )

    # ------------------------------------
    # 3. COUNTRY STATISTICS
    # DICTIONARY CONCEPT
    # ------------------------------------

    def country_statistics(self):
        country = self.choose_country()

        if country is None:
            return

        column = country + "_Alcohol_Related_Deaths"

        values = self.df[column]

        maximum = values.idxmax()
        minimum = values.idxmin()

        # Dictionary stores statistics
        statistics = {
            "Total Deaths": int(values.sum()),
            "Average Annual Deaths": round(values.mean(), 2),
            "Maximum Deaths": int(values.loc[maximum]),
            "Maximum Year": int(
                self.df.loc[maximum, "Year"]
            ),
            "Minimum Deaths": int(values.loc[minimum]),
            "Minimum Year": int(
                self.df.loc[minimum, "Year"]
            )
        }

        print("\nCOUNTRY STATISTICS")
        print("Country:", country.replace("_", " "))

        for key, value in statistics.items():
            print(key, ":", value)

    # ------------------------------------
    # 4. YEARLY INCREASES AND DECREASES
    # ------------------------------------

    def yearly_changes(self):
        country = self.choose_country()

        if country is None:
            return

        column = country + "_Alcohol_Related_Deaths"

        data = self.df[["Year", column]].copy()

        data["Change"] = data[column].diff()

        data["Change_Percent"] = (
            data[column].pct_change() * 100
        )

        print("\nYEARLY CHANGES")
        print(data.round(2).to_string(index=False))

    # ------------------------------------
    # 5. MALE VS FEMALE COMPARISON
    # ------------------------------------

    def gender_comparison(self):
        country = self.choose_country()

        if country is None:
            return

        male = self.df[
            country + "_Male_Alcohol_Deaths"
        ].sum()

        female = self.df[
            country + "_Female_Alcohol_Deaths"
        ].sum()

        print("\nGENDER COMPARISON")
        print("Country:", country.replace("_", " "))
        print("Male Deaths:", int(male))
        print("Female Deaths:", int(female))

        if male > female:
            print("Higher Deaths: Male")

        elif female > male:
            print("Higher Deaths: Female")

        else:
            print("Male and Female Deaths are Equal")

    # ------------------------------------
    # 6. SEARCH DATA BY YEAR
    # ------------------------------------

    def search_year(self):
        year = self.choose_year()

        if year is None:
            return

        data = self.df[
            self.df["Year"] == year
        ].iloc[0]

        print("\nALCOHOL-RELATED DEATHS IN", year)

        for country in COUNTRIES:
            column = country + "_Alcohol_Related_Deaths"

            print(
                country.replace("_", " "),
                ":",
                int(data[column])
            )

    # ------------------------------------
    # 7. SORT COUNTRIES BY DEATHS
    # DICTIONARY AND SORTING
    # ------------------------------------

    def sorted_countries(self):
        year = self.choose_year()

        if year is None:
            return

        data = self.df[
            self.df["Year"] == year
        ].iloc[0]

        country_deaths = {}

        for country in COUNTRIES:
            column = country + "_Alcohol_Related_Deaths"

            country_deaths[
                country.replace("_", " ")
            ] = int(data[column])

        sorted_data = sorted(
            country_deaths.items(),
            key=lambda item: item[1],
            reverse=True
        )

        print("\nCOUNTRY RANKING FOR", year)

        for country, deaths in sorted_data:
            print(country, ":", deaths)

        print("Note: These are counts, not population-adjusted rates.")

    # ------------------------------------
    # 8. RECURSION DEMONSTRATION
    # ------------------------------------

    def recursion_demo(self):
        country = self.choose_country()

        if country is None:
            return

        column = country + "_Alcohol_Related_Deaths"

        values = self.df[column].astype(int).tolist()

        total = recursive_total(values)

        print("\nRECURSION RESULT")

        print("Country:", country.replace("_", " "))

        print("Total using Recursion:", total)

        print(
            "Total using Pandas:",
            int(self.df[column].sum())
        )

    # ------------------------------------
    # 9. LINE GRAPH
    # YEARLY FATALITY TREND
    # ------------------------------------

    def plot_trend(self):
        country = self.choose_country()

        if country is None:
            return

        column = country + "_Alcohol_Related_Deaths"

        plt.figure(figsize=(10, 5))

        plt.plot(
            self.df["Year"],
            self.df[column],
            marker="o",
            markersize=3
        )

        plt.title(
            "Alcohol-Related Fatalities - " +
            country.replace("_", " ")
        )

        plt.xlabel("Year")
        plt.ylabel("Alcohol-Related Deaths")

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 10. BAR GRAPH
    # COUNTRY COMPARISON
    # ------------------------------------

    def plot_country_comparison(self):
        year = self.choose_year()

        if year is None:
            return

        data = self.df[
            self.df["Year"] == year
        ].iloc[0]

        names = []
        deaths = []

        for country in COUNTRIES:
            names.append(country.replace("_", " "))

            deaths.append(
                data[country + "_Alcohol_Related_Deaths"]
            )

        plt.figure(figsize=(10, 5))

        plt.bar(names, deaths)

        plt.title(
            "Alcohol-Related Deaths by Country - " +
            str(year)
        )

        plt.xlabel("Country")
        plt.ylabel("Number of Deaths")

        plt.xticks(rotation=20)

        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 11. PIE CHART
    # MALE VS FEMALE
    # ------------------------------------

    def plot_gender_pie(self):
        country = self.choose_country()

        if country is None:
            return

        male = self.df[
            country + "_Male_Alcohol_Deaths"
        ].sum()

        female = self.df[
            country + "_Female_Alcohol_Deaths"
        ].sum()

        if male + female == 0:
            print("No deaths available to plot.")
            return

        plt.figure(figsize=(7, 6))

        plt.pie(
            [male, female],
            labels=["Male", "Female"],
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title(
            "Male vs Female Alcohol-Related Deaths - " +
            country.replace("_", " ")
        )

        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 12. MULTIPLE LINE GRAPH
    # ALL SIX COUNTRIES
    # ------------------------------------

    def plot_six_country_trends(self):
        plt.figure(figsize=(11, 6))

        for country in COUNTRIES:
            column = country + "_Alcohol_Related_Deaths"

            plt.plot(
                self.df["Year"],
                self.df[column],
                label=country.replace("_", " ")
            )

        plt.title(
            "Alcohol-Related Fatality Trends - Six Countries"
        )

        plt.xlabel("Year")
        plt.ylabel("Number of Deaths")

        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 13. YEARLY PERCENTAGE CHANGE GRAPH
    # ------------------------------------

    def plot_yearly_change(self):
        country = self.choose_country()

        if country is None:
            return

        column = country + "_Alcohol_Related_Deaths"

        changes = (
            self.df[column].pct_change() * 100
        )

        changes = changes.replace(
            [float("inf"), -float("inf")],
            float("nan")
        )

        plt.figure(figsize=(10, 5))

        plt.bar(
            self.df["Year"].iloc[1:],
            changes.iloc[1:]
        )

        plt.axhline(0)

        plt.title(
            "Yearly Percentage Change - " +
            country.replace("_", " ")
        )

        plt.xlabel("Year")
        plt.ylabel("Percentage Change (%)")

        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 14. ALCOHOL PERCENTAGE BAR GRAPH
    # ------------------------------------

    def plot_alcohol_percentage(self):
        year = self.choose_year()

        if year is None:
            return

        data = self.df[
            self.df["Year"] == year
        ].iloc[0]

        names = []
        rates = []

        for country in COUNTRIES:
            names.append(country.replace("_", " "))

            rates.append(
                data[country + "_Alcohol_Rate_Percent"]
            )

        plt.figure(figsize=(10, 5))

        plt.bar(names, rates)

        plt.title(
            "Alcohol-Related Share of Road Deaths - " +
            str(year)
        )

        plt.xlabel("Country")
        plt.ylabel("Alcohol-Related Share (%)")

        plt.ylim(0, 100)
        plt.xticks(rotation=20)

        plt.tight_layout()
        plt.show()

    # ------------------------------------
    # 15. FILE WRITING
    # SAVE SUMMARY REPORT TO CSV
    # ------------------------------------

    def export_report(self):
        report = []

        for country in COUNTRIES:
            column = country + "_Alcohol_Related_Deaths"

            values = self.df[column]

            male = self.df[
                country + "_Male_Alcohol_Deaths"
            ].sum()

            female = self.df[
                country + "_Female_Alcohol_Deaths"
            ].sum()

            report.append({
                "Country": country.replace("_", " "),
                "Total_Alcohol_Deaths": int(values.sum()),
                "Average_Annual_Deaths": round(
                    values.mean(), 2
                ),
                "Highest_Year": int(
                    self.df.loc[values.idxmax(), "Year"]
                ),
                "Lowest_Year": int(
                    self.df.loc[values.idxmin(), "Year"]
                ),
                "Male_Deaths": int(male),
                "Female_Deaths": int(female)
            })

        report_df = pd.DataFrame(report)

        output_file = (
            self.file_path.parent /
            "alcohol_fatalities_summary_report_new.csv"
        )

        try:
            report_df.to_csv(output_file, index=False)

            print("\nReport saved successfully!")
            print("File:", output_file)

        except (PermissionError, OSError) as error:
            print("Error saving report:", error)


# ----------------------------------------
# MAIN FUNCTION
# ----------------------------------------

def main():

    # Create an object
    analyzer = FatalityAnalyzer()

    # Load dataset
    if not analyzer.load_data():
        return

    print("\nGLOBAL ALCOHOL-RELATED ROAD FATALITIES")
    print("Synthetic Educational Data: 1970-2024")

    # Dictionary stores menu operations
    actions = {
        "1": analyzer.show_data,
        "2": analyzer.show_info,
        "3": analyzer.country_statistics,
        "4": analyzer.yearly_changes,
        "5": analyzer.gender_comparison,
        "6": analyzer.search_year,
        "7": analyzer.sorted_countries,
        "8": analyzer.recursion_demo,
        "9": analyzer.plot_trend,
        "10": analyzer.plot_country_comparison,
        "11": analyzer.plot_gender_pie,
        "12": analyzer.plot_six_country_trends,
        "13": analyzer.plot_yearly_change,
        "14": analyzer.plot_alcohol_percentage,
        "15": analyzer.export_report
    }

    while True:

        print("""
=============================================
GLOBAL ALCOHOL-RELATED FATALITIES MENU
=============================================

1. Show first five rows
2. Show dataset information
3. Country statistics
4. Yearly increases and decreases
5. Compare male and female deaths
6. Search fatalities by year
7. Sort countries by deaths for a year
8. Recursion demonstration
9. Plot yearly fatality trend
10. Plot country comparison
11. Plot male vs female pie chart
12. Plot all six country trends
13. Plot annual percentage changes
14. Plot alcohol-related percentages
15. Save summary report to CSV
0. Exit

=============================================
""")

        try:
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Thank you! Program ended.")
                break

            action = actions.get(choice)

            if action is not None:
                action()

            else:
                print("Invalid choice. Please try again.")

        except (EOFError, KeyboardInterrupt):
            print("\nProgram ended.")
            break

        except Exception as error:
            print("An unexpected error occurred:", error)
            print("Please try another option.")


# ----------------------------------------
# RUN PROGRAM
# ----------------------------------------

if __name__ == "__main__":
    main()
