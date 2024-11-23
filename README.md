# iRecycle Digital Research

A comprehensive tool for finding and analyzing recycling businesses, generating structured data, and creating SQL statements for database integration.

## Project Structure 

bash
irecycle-digital-research/
├── output/ # Generated JSON and SQL files
├── recycling-business-finder/ # Business finding module
│ ├── init.py
│ ├── recycling_business_finder.py
│ └── requirements.txt
├── recycling-data-engineer/ # Data engineering module
│ ├── init.py
│ ├── database_definitions.py
│ ├── existing_materials.py
│ ├── reporting_engineer.py
│ └── requirements.txt
├── .env # Environment variables (not in git)
├── .env.example # Example environment variables
├── .gitignore
├── README.md
├── requirements.txt
├── recycling_service_manager.py
└── setup.py


## Features

- Find recycling businesses using Google Places API
- Analyze business websites for recycling materials
- Generate structured JSON data
- Convert data to SQL statements for database integration
- Handle business hours, materials, and services

## Prerequisites

- Python 3.8 or higher
- Google Places API key
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:

bash
git clone https://github.com/fitzroypet/irecycle-digital-research.git
cd irecycle-digital-research

2. Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate

3. Install dependencies:

bash
pip install -r requirements.txt

4. Set up environment variables:

bash
cp .env.example .env
Edit .env and add your Google API key

## Usage

Run the service manager with a city and country:

bash
python recycling_service_manager.py "London" "UK"


The script will:
1. Search for recycling businesses in the specified location
2. Generate JSON data with business details
3. Create SQL statements for database insertion
4. Save output files in the `output` directory

## Output Files

- JSON files: `output/<city>_<country>_<timestamp>.json`
- SQL files: `output/<city>_<country>.sql`

## Development

To contribute to the project:

1. Create a new branch for your feature
2. Make your changes
3. Run tests (if available)
4. Submit a pull request


## Running Tests

To run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=.

# Run with HTML coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_recycling_business


## License

MIT license

## Contact

fitzroy@irecycle.world