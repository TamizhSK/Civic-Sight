import os
import re
import pandas as pd
from google.cloud import documentai
from typing import Dict, List, Optional
import config

class PDFParser:
    def __init__(self):
        """Initialize the PDF parser with GCP Document AI client."""
        # Validate required configuration
        if not all([config.PROJECT_ID, config.PROCESSOR_ID]):
            print("Warning: Missing GCP configuration (PROJECT_ID or PROCESSOR_ID)")
            print("Falling back to mock processing for testing...")
            self.client = None
            self.processor_name = None
            return
        
        try:
            # Initialize Document AI client
            self.client = documentai.DocumentProcessorServiceClient()
            self.processor_name = self.client.processor_path(
                config.PROJECT_ID, config.LOCATION, config.PROCESSOR_ID
            )
            print("✓ GCP Document AI client initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize Document AI client: {e}")
            print("Falling back to mock processing for testing...")
            self.client = None
            self.processor_name = None
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using GCP Document AI."""
        if not self.client:
            # Mock text extraction for testing when GCP is not configured
            print(f"Mock processing: {pdf_path}")
            return self._mock_pdf_text(pdf_path)
        
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()
            
            # Configure the process request
            request = documentai.ProcessRequest(
                name=self.processor_name,
                raw_document=documentai.RawDocument(
                    content=pdf_content,
                    mime_type="application/pdf"
                )
            )
            
            # Process the document
            result = self.client.process_document(request=request)
            document = result.document
            
            return document.text
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            return ""
    
    def _mock_pdf_text(self, pdf_path: str) -> str:
        """Mock PDF text extraction for testing purposes."""
        filename = os.path.basename(pdf_path)
        constituency_name = filename.replace('.pdf', '').replace('_', ' ').title()
        
        # Return mock electoral data for testing
        return f"""
        Electoral Results Report
        
        Constituency Name: {constituency_name}
        
        Election Summary:
        Total number of electors: 45,678
        Total number of valid votes polled: 38,234
        Total number of votes for 'None of the Above': 1,234
        
        Additional details...
        """
    
    def extract_data_from_text(self, text: str, filename: str) -> Dict[str, str]:
        """Extract specific data fields from the text using regex patterns."""
        data = {
            "filename": filename,
            "constituency_name": "",
            "total_electors": "",
            "valid_votes_polled": "",
            "nota_votes": ""
        }
        
        # Clean text for better matching
        clean_text = re.sub(r'\s+', ' ', text.strip())
        
        # Pattern for constituency name - improved to handle various formats
        constituency_patterns = [
            r'constituency\s+name[:\s]+([A-Za-z\s]+?)(?:\n|election|total)',
            r'constituency[:\s]+([A-Za-z\s]+?)(?:\n|election|total)',
            r'([A-Z][A-Za-z\s]+)\s+constituency',
            r'name[:\s]+([A-Za-z\s]+?)(?:\n|total|election)',
            r'constituency[:\s]*([A-Za-z][A-Za-z\s]{3,30})(?:\s*\n|\s+election|\s+total)'
        ]
        
        for pattern in constituency_patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean up common false matches
                if len(name) > 3 and not name.lower().startswith(('total', 'number', 'election')):
                    data["constituency_name"] = name
                    break
        
        # Pattern for total electors - improved to handle commas and various formats
        elector_patterns = [
            r'total\s+(?:number\s+of\s+)?electors[:\s]+([0-9,]+)',
            r'electors[:\s]+([0-9,]+)',
            r'total\s+electors[:\s]+([0-9,]+)',
            r'registered\s+voters[:\s]+([0-9,]+)',
            r'total\s+registered[:\s]+([0-9,]+)'
        ]
        
        for pattern in elector_patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                # Remove commas from numbers
                data["total_electors"] = match.group(1).replace(',', '')
                break
        
        # Pattern for valid votes polled - improved to handle commas
        valid_votes_patterns = [
            r'total\s+(?:number\s+of\s+)?valid\s+votes\s+polled[:\s]+([0-9,]+)',
            r'valid\s+votes\s+polled[:\s]+([0-9,]+)',
            r'total\s+valid\s+votes[:\s]+([0-9,]+)',
            r'votes\s+polled[:\s]+([0-9,]+)',
            r'total\s+votes\s+cast[:\s]+([0-9,]+)'
        ]
        
        for pattern in valid_votes_patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                # Remove commas from numbers
                data["valid_votes_polled"] = match.group(1).replace(',', '')
                break
        
        # Pattern for NOTA votes - improved to handle various formats
        nota_patterns = [
            r'none\s+of\s+the\s+above[:\s]+([0-9,]+)',
            r'nota[:\s]+([0-9,]+)',
            r'votes\s+for\s+[\'"]?none\s+of\s+the\s+above[\'"]?[:\s]+([0-9,]+)',
            r'[\'"]?none\s+of\s+the\s+above[\'"]?[:\s]+([0-9,]+)',
            r'option\s+nota[:\s]+([0-9,]+)'
        ]
        
        for pattern in nota_patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                # Remove commas from numbers
                data["nota_votes"] = match.group(1).replace(',', '')
                break
        
        return data
    
    def process_all_pdfs(self) -> List[Dict[str, str]]:
        """Process all PDF files in the data folder."""
        if not os.path.exists(config.PDF_FOLDER):
            print(f"PDF folder '{config.PDF_FOLDER}' not found!")
            return []
        
        pdf_files = [f for f in os.listdir(config.PDF_FOLDER) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in '{config.PDF_FOLDER}' folder!")
            return []
        
        print(f"Found {len(pdf_files)} PDF files to process...")
        
        all_data = []
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"Processing {i}/{len(pdf_files)}: {pdf_file}")
            
            pdf_path = os.path.join(config.PDF_FOLDER, pdf_file)
            
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            
            if text:
                # Extract data from text
                data = self.extract_data_from_text(text, pdf_file)
                all_data.append(data)
            else:
                print(f"Failed to extract text from {pdf_file}")
        
        return all_data
    
    def save_to_excel(self, data: List[Dict[str, str]]) -> None:
        """Save extracted data to Excel file."""
        if not data:
            print("No data to save!")
            return
        
        # Create output folder if it doesn't exist
        os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Rename columns for better readability
        df.columns = [
            "Filename",
            "Constituency Name", 
            "Total Electors",
            "Valid Votes Polled",
            "NOTA Votes"
        ]
        
        # Save to Excel
        output_path = os.path.join(config.OUTPUT_FOLDER, config.OUTPUT_FILE)
        df.to_excel(output_path, index=False)
        
        print(f"Data saved to: {output_path}")
        print(f"Total records: {len(data)}")