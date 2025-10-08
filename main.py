#!/usr/bin/env python3
"""
GCP-powered PDF Parser for Electoral Data Extraction
Extracts constituency information from PDF files and saves to Excel
"""

import os
import sys
from pdf_parser import PDFParser
import config

def main():
    """Main execution function."""
    print("=== GCP PDF Parser for Electoral Data ===")
    print(f"Looking for PDF files in: {config.PDF_FOLDER}")
    print(f"Output will be saved to: {config.OUTPUT_FOLDER}/{config.OUTPUT_FILE}")
    print()
    
    # Create data folder if it doesn't exist
    os.makedirs(config.PDF_FOLDER, exist_ok=True)
    
    # Initialize parser
    try:
        parser = PDFParser()
        print("✓ GCP Document AI client initialized")
    except Exception as e:
        print(f"✗ Failed to initialize GCP client: {str(e)}")
        print("\nPlease ensure:")
        print("1. Your GCP project ID is correct in config.py")
        print("2. Document AI processor is created and ID is set")
        print("3. API key has proper permissions")
        sys.exit(1)
    
    # Process all PDFs
    try:
        extracted_data = parser.process_all_pdfs()
        
        if extracted_data:
            # Save to Excel
            parser.save_to_excel(extracted_data)
            
            # Print summary
            print("\n=== Extraction Summary ===")
            successful_extractions = sum(1 for data in extracted_data 
                                       if any(data[key] for key in data.keys() if key != 'filename'))
            print(f"Files processed: {len(extracted_data)}")
            print(f"Successful extractions: {successful_extractions}")
            
            # Show sample of extracted data
            if extracted_data:
                print("\n=== Sample Data ===")
                sample = extracted_data[0]
                for key, value in sample.items():
                    print(f"{key}: {value}")
        else:
            print("No data was extracted. Please check your PDF files and configuration.")
            
    except Exception as e:
        print(f"✗ Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()