# GCP PDF Parser for Electoral Data

A Python application that uses Google Cloud Document AI to extract electoral data from PDF files and save the results to Excel.

## Features

- Processes 234+ PDF files automatically
- Extracts specific electoral data:
  - Constituency Name
  - Total number of electors
  - Total number of valid votes polled
  - Total number of votes for 'None of the Above'
- Saves all data to a single Excel file
- Uses Google Cloud Document AI for accurate text extraction

## Setup

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure GCP settings in `.env` file:**
   - Set your GCP project ID
   - Set your Document AI processor ID
   - API key is already configured

3. **Create Document AI Processor:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable Document AI API
   - Create a new processor (General processor type)
   - Copy the processor ID to `.env` file

4. **Add PDF files:**
   - Place all PDF files in the `data/` folder

## Usage

**Activate virtual environment:**
```bash
source venv/bin/activate
```

**Run the parser:**
```bash
python main.py
```

**Test with sample data:**
```bash
python test_sample.py
```

The extracted data will be saved to `output/extracted_data.xlsx`

## Project Structure

```
├── main.py              # Main execution script
├── pdf_parser.py        # Core parsing logic
├── config.py           # Configuration settings
├── requirements.txt    # Dependencies
├── data/              # PDF files folder
└── output/            # Excel output folder
```

## Configuration

Edit `config.py` to customize:
- GCP project settings
- File paths
- Data extraction patterns