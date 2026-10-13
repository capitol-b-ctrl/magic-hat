# Magic Hat 🎩✨

A modular command-line tool and interactive menu system designed to assist magicians and enthusiasts in tracking merchandise acquisition, inventory, and budgeting.

---

## 📂 Project Structure

```text
Magic_Hat/
├── .venv/                  # Isolated virtual environment (ignored by Git)
├── .gitignore              # Tells Git which files to ignore
├── README.md               # Project overview, setup, and instructions
├── pyproject.toml          # Modern central configuration for tools & dependencies
├── src/                    # Source code layout
│   └── magic_hat/          # Primary application package
│       ├── __init__.py     # Marks directory as an importable package
|	|── magic-hat.db    # Sqlite Database file for memory persistance
│       ├── magic-hat.py    # Primary entry point script
│       ├── database.py     # Sub-module for data handling
│       └── utils.py        # Sub-module for helper functions
└── tests/                  # Mirror of src/ used for automated testing
    ├── __init__.py
    └── test_database.py    # Unit tests targeting database logic

