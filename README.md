# Recycling Services Researcher

A Python application that finds and analyzes recycling services in different cities using Google Places API.

## Features

- Finds recycling services in specified cities
- Analyzes business websites for recycling materials
- Generates detailed JSON reports
- Creates SQL statements for database storage
- Supports material type identification

## Installation

1. Clone the repository:

```bash
git clone https://github.com/fitzroypet/recycling-services-researcher.git
cd recycling-services-researcher
```

2. Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate 
On Windows: .\venv\Scripts\activate

3. Install dependencies:

bash
pip install -r requirements.txt

4. Create a `.env` file with your Google API key:

plaintext
GOOGLE_API_KEY=your_api_key_here
SEARCH_RADIUS=5000
MAX_RESULTS=100

## Usage

Run the service manager with a city and country:

bash
python recycling_services_researcher.py "City_Name" "Country"

Example:
python recycling_services_researcher.py "London" "UK"

The script will:
1. Search for recycling businesses in the specified location
2. Generate JSON data with business details
3. Create SQL statements for database insertion
4. Save output files in the `output` directory

## Output

The program generates two files in the `output` directory:
- A JSON file containing detailed information about recycling services
- An SQL file with database insertion statements

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

# Run specific test file
pytest tests/test_recycling_business


## License

[MIT License](LICENSE)

## Contact

fitzroy@irecycle.world