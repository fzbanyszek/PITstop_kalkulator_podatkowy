# PITstop Tax Calculator

PITstop is a Streamlit-based tax calculator designed to support Polish investors who trade on the U.S. stock market through Interactive Brokers.

The application automates the process of calculating realized profit or loss in PLN based on Interactive Brokers activity statement CSV files. It applies FIFO logic, determines settlement dates, retrieves appropriate NBP exchange rates, and presents the final results in a clear, user-friendly interface.

## Purpose

Manually calculating taxable profit from foreign brokerage transactions can be time-consuming and error-prone. PITstop was created to simplify this process by automating the most important calculation steps required for Polish tax reporting.

The tool is especially useful for investors who need to convert USD-denominated trades into PLN and determine realized gains or losses for a selected tax year.

## Main Features

- Upload one or more CSV files exported from Interactive Brokers
- Extract and clean transaction data from IBKR activity statements
- Calculate realized profit or loss using the FIFO method
- Determine settlement dates using exchange calendar rules
- Automatically fetch NBP exchange rates for currency conversion
- Convert proceeds and commissions into PLN
- Display total realized profit for a selected tax year
- Show profit or loss grouped by stock symbol
- Present transaction history in a readable table
- Generate a PDF tax report for the selected year
- Support Polish and English interface translations
- Allow custom exchange calendar upload
- Include test CSV files for quick application testing

## How It Works

1. The user uploads CSV activity statement files exported from Interactive Brokers.
2. The application extracts trade-related rows from the files.
3. Transaction data is cleaned and standardized.
4. Settlement dates are calculated based on the configured exchange calendar.
5. The application retrieves the relevant average NBP exchange rate.
6. Trade values and commissions are converted into PLN.
7. Realized profit or loss is calculated using FIFO matching.
8. Results are displayed by year and by instrument.
9. A PDF report can be downloaded for documentation purposes.

## Project Structure

```text
PITstop_kalkulator_podatkowy/
│
├── main.py                  # Main Streamlit application entry point
├── pages/                   # Streamlit pages
│   ├── home.py              # Home page and project introduction
│   ├── calculator.py        # File upload and processing page
│   ├── results.py           # Results, charts, history and PDF export
│   └── settings.py          # Application settings and calendar configuration
│
├── ibkr_classes/            # Core calculation and data processing logic
│   ├── ibkrCalculator.py    # FIFO profit calculation logic
│   ├── ibkrDataOperations.py# Data cleaning, exchange rates and settlement dates
│   ├── ibkrPortfolio.py     # Portfolio creation and processing workflow
│   ├── ibkrPosition.py      # Position representation
│   ├── ibkrTrade.py         # Trade representation
│   └── pdf_report.py        # PDF report generation
│
├── translations/            # Polish and English interface translations
├── calendar_files/          # Exchange calendar data
├── test_files/              # Sample CSV files for testing
├── assets/                  # Application images and branding
├── LICENSE                  # Apache-2.0 license
└── README.md
