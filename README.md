# Sales Data Management System

A Python-based application for managing sales data with a user-friendly interface, database integration, and data visualization.

## Features

- **Data Entry**: Add sales records (product, price, quantity, date) via a `tkinter` GUI.
- **Database Integration**: Store and manage data in a PostgreSQL database.
- **CSV Import**: Load sales data from CSV files for bulk processing.
- **Data Visualization**: Generate pie charts, area charts, and interactive line charts using `matplotlib`, `seaborn`, and `plotly`.
- **Data Validation**: Ensure valid inputs (e.g., Latin-only product names, positive prices/quantities).

## Requirements

- Python 3.8+
- PostgreSQL
- Required libraries listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/enesarafatoglu/sales-data-system.git
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up a PostgreSQL database and create a *.env* file in the project root with the following variables:
```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```
4. Run the application:
```bash
    python main.py
```

## Usage
* Launch the GUI to add sales records manually.
* Use yeni_satislar.csv to import bulk data.
* View visualizations (pie, area, and interactive line charts) after data operations.
* Check the database for updated records using the GUI's table view.

## Project Structure
* main.py: Entry point for the application.
* gui.py: Tkinter-based GUI for data entry and viewing.
* data_insertion.py: Handles data validation and insertion.
* db_config.py: Database connection setup.
* visualization.py: Generates charts.
* data_operations.py: Manages updates and deletions.
* requirements.txt: Lists project dependencies.