#!/usr/bin/env python3
"""
List existing GCP Document AI processors and get their IDs
"""

import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import config

def list_existing_processors(project_id: str, location: str) -> None:
    """List existing processors in the project."""
    print(f"Listing existing processors for project: {project_id} in location: {location}")
    
    # Set the API endpoint for the location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # The full resource name of the location
    parent = client.common_location_path(project_id, location)
    
    try:
        # List processors
        response = client.list_processors(parent=parent)
        
        print("\nExisting processors:")
        print("-" * 80)
        
        processors_found = []
        
        for processor in response.processors:
            processor_id = processor.name.split("/")[-1]
            processors_found.append({
                'name': processor.display_name,
                'id': processor_id,
                'type': processor.type_,
                'state': processor.state.name
            })
            
            print(f"Name: {processor.display_name}")
            print(f"  ID: {processor_id}")
            print(f"  Type: {processor.type_}")
            print(f"  State: {processor.state.name}")
            print(f"  Full Name: {processor.name}")
            print()
        
        # Show recommended processor for .env
        if processors_found:
            print("=" * 80)
            print("📝 RECOMMENDED: Update your .env file with one of these processor IDs:")
            print()
            
            # Look for FORM_PARSER_PROCESSOR first (best for structured documents)
            form_parser = next((p for p in processors_found if p['type'] == 'FORM_PARSER_PROCESSOR'), None)
            if form_parser:
                print(f"✅ RECOMMENDED - FORM_PARSER_PROCESSOR (best for electoral PDFs):")
                print(f"PROCESSOR_ID={form_parser['id']}")
                print()
            
            # Show OCR processor as alternative
            ocr_processor = next((p for p in processors_found if p['type'] == 'OCR_PROCESSOR'), None)
            if ocr_processor:
                print(f"⚡ ALTERNATIVE - OCR_PROCESSOR (basic text extraction):")
                print(f"PROCESSOR_ID={ocr_processor['id']}")
                print()
            
            # Show custom extraction processor
            custom_processor = next((p for p in processors_found if p['type'] == 'CUSTOM_EXTRACTION_PROCESSOR'), None)
            if custom_processor:
                print(f"🔧 ADVANCED - CUSTOM_EXTRACTION_PROCESSOR (requires training):")
                print(f"PROCESSOR_ID={custom_processor['id']}")
                print()
                
        else:
            print("No processors found in this project/location")
            
    except Exception as e:
        print(f"Error listing processors: {e}")

def main():
    """Main function."""
    print("=== GCP Document AI Processor List ===")
    
    if not config.PROJECT_ID:
        print("❌ PROJECT_ID not found in .env file!")
        return
    
    list_existing_processors(config.PROJECT_ID, config.LOCATION)

if __name__ == "__main__":
    main()