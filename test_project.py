import pytest
import os
import csv
import shutil
import datetime
import logging
from project import *

DATA_FILE = "test_transactions.csv"
BACKUP_FOLDER = "test_backups"
LOG_FILE = "test_financial_assistant.log"

@pytest.fixture(scope="session")
def initialize_test_data_file():
    """Initialize the test data file."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category", "Amount", "Type"])

@pytest.fixture(scope="session")
def initialize_test_backup_folder():
    """Initialize the test backup folder."""
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

@pytest.fixture(scope="session")
def initialize_test_log_file():
    """Initialize the test log file."""
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def initialize_test_environment(initialize_test_data_file, initialize_test_backup_folder, initialize_test_log_file):
    """Initialize the test environment."""
    yield
    os.remove(DATA_FILE)
    shutil.rmtree(BACKUP_FOLDER)
    os.remove(LOG_FILE)

@pytest.fixture
def mock_input(monkeypatch):
    """Mock input function."""
    mock_inputs = []

    def mock_input_func(prompt):
        nonlocal mock_inputs
        if len(mock_inputs) == 0:
            raise ValueError("No more inputs provided.")
        return mock_inputs.pop(0)

    monkeypatch.setattr('builtins.input', mock_input_func)

@pytest.fixture
def mock_datetime_now(monkeypatch):
    """Mock datetime.now() function."""
    mock_now = datetime.datetime(2024, 5, 14, 12, 0, 0)

    class MockDateTime:
        @classmethod
        def now(cls):
            return mock_now

    monkeypatch.setattr('datetime.datetime', MockDateTime)

def test_initialize_data_file(initialize_test_data_file):
    initialize_data_file()
    assert os.path.exists(DATA_FILE)

def test_backup_data(initialize_test_backup_folder, initialize_test_data_file):
    backup_data()
    backup_files = os.listdir(BACKUP_FOLDER)
    assert len(backup_files) == 1
    assert backup_files[0].startswith("transactions_backup_")

def test_recover_data(initialize_test_backup_folder, initialize_test_data_file, capsys, mock_input):
    mock_inputs = ["1"]
    backup_data()
    recover_data()
    captured = capsys.readouterr()
    assert "Data recovered successfully." in captured.out

def test_add_transaction(initialize_test_data_file, capsys, mock_input):
    mock_inputs = ["Income", "2024-05-14", "Test Description", "Test Category", "100"]
    add_transaction()
    captured = capsys.readouterr()
    assert "Transaction added successfully." in captured.out

def test_view_transactions(initialize_test_data_file, capsys):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Test Category", "100", "Income"])
    view_transactions()
    captured = capsys.readouterr()
    assert "2024-05-14" in captured.out

def test_edit_transaction(initialize_test_data_file, capsys, mock_input):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Test Category", "100", "Income"])
    mock_inputs = ["1", "2024-05-15", "Updated Description", "Updated Category", "200", "Expense"]
    edit_transaction()
    captured = capsys.readouterr()
    assert "Transaction updated successfully." in captured.out

def test_categorize_transactions(initialize_test_data_file):
    category_mapping = {"Groceries": ["food", "grocery"], "Travel": ["travel", "transport"]}
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Grocery shopping", "Other", "-50", "Expense"])
        writer.writerow(["2024-05-15", "Flight ticket", "Other", "-200", "Expense"])
    categorize_transactions(category_mapping, "Expense")
    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            assert row[2] in ["Groceries", "Travel", "Other"]

def test_search_transactions(initialize_test_data_file, capsys):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Test Category", "100", "Income"])
    with pytest.raises(SystemExit):
        with pytest.raises(ValueError):
            search_transactions()
    captured = capsys.readouterr()
    assert "2024-05-14" in captured.out

def test_generate_report(initialize_test_data_file, capsys):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Test Category", "100", "Income"])
    generate_report()
    captured = capsys.readouterr()
    assert "Total Income: 100.0" in captured.out

def test_analyze_report(initialize_test_data_file, capsys):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Groceries", "-50", "Expense"])
        writer.writerow(["2024-05-15", "Test Description", "Travel", "-200", "Expense"])
    analyze_report()
    captured = capsys.readouterr()
    assert "Groceries: -50.0" in captured.out

def test_manage_debt(initialize_test_data_file, capsys):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        writer.writerow(["2024-05-14", "Test Description", "Debt", "-500", "Expense"])
    manage_debt()
    captured = capsys.readouterr()
    assert "Total debt: -500.0" in captured.out

def test_retirement_planning(capsys, mock_input):
    mock_inputs = ["30", "65", "3000", "85"]
    retirement_planning()
    captured = capsys.readouterr()
    "assert " "Total savings needed: $XXX,XXX.XX" in captured.out

