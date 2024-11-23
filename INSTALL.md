# Installation Instructions

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

## Setup Steps

1. Clone the repository: 

bash
git clone https://github.com/fitzroypet/recycling_services_researcher.git
cd recycling-services-researcher


2. Create and activate a virtual environment (optional but recommended):

bash
On Windows
python -m venv venv
.\venv\Scripts\activate
On macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:

bash
pip install -r requirements.txt

4. Set up environment variables:

bash
Copy the example environment file
cp .env.example .env
Edit .env with your actual values
Replace the placeholder values with your actual API keys and credentials

5. Verify installation:

bash
python recycling_services_researcher.py "London" "UK"


## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are installed
2. Check that your API key is correctly set in the .env file
3. Verify that your Python version is compatible
4. Check that all required dependencies are installed

For database-related issues, ensure your database credentials are correctly set in the .env file.

## Development Setup (Optional)

For development, you might want to install additional tools:

bash
pip install black pylint


## Contact

If you encounter any issues, please open an issue on the GitHub repository.