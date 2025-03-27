## StoreManagement

A simple desktop billing application built with Python and Tkinter, capable of generating PDF invoices. It includes a first-time setup screen to capture store information and uses an `.env` file for configuration.

---

## Features

- Graphical user interface for adding items, prices, and quantities.
- First-run setup to collect store details (saved in `.env`).
- Stores customer and item information in a local SQLite database.
- Generates PDF invoices and saves them in the `invoices/` folder.
- Easy configuration via `.env` and environment variables.

---

## Requirements

- Python 3.7+ recommended
- All dependencies listed in `requirements.txt`

Install dependencies:
```bash
pip install -r requirements.txt
