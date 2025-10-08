#!/usr/bin/env python3
"""
Create GCP Document AI processors for PDF parsing
"""

import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import config

def create_processor(project_id: str, location: str, processor_type: str, display_name: str) -> str:
    """Create a new Document AI processor."""
    print(f"Creating {processor_type} processor...")
    
    # Set the API endpoint for the location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # The full resource name of the location
    parent = client.common_location_path(project_id, location)
    
    try:
        # Create processor request
        processor = documentai.Processor(
            display_name=display_name,
            type_=processor_type
        )
        
        request = documentai.CreateProcessorRequest(
            parent=parent,
            processor=processor
        )
        
        # Create the processor
        result = client.create_processor(request=request)
        print(f"  ✓ {processor_type} creation initiated...")
        
        # Extract processor ID from the name
        processor_id = result.name.split("/")[-1]
        
        print(f"  ✓ {processor_type} created successfully!")
        print(f"  Processor ID: {processor_id}")
        print(f"  Full name: {result.name}")
        print()
        
        return processor_id
        
    except Exception as e:
        print(f"  ❌ Error creating {processor_type}: {e}")
        return ""

def main():
    """Create all necessary processors."""
    print("=== Creating GCP Document AI Processors ===")
    print(f"Project: {config.PROJECT_ID}")
    print(f"Location: {config.LOCATION}")
    print()
    
    if not config.PROJECT_ID:
        print("❌ PROJECT_ID not found in .env file!")
        return
    
    # Create processors
    processors_to_create = [
        ("FORM_PARSER_PROCESSOR", "PDF Electoral Data Parser - Form Parser"),
        ("OCR_PROCESSOR", "PDF Electoral Data Parser - OCR"),
        ("CUSTOM_EXTRACTION_PROCESSOR", "PDF Electoral Data Parser - Custom Extraction")
    ]
    
    created_processors = {}
    
    for processor_type, display_name in processors_to_create:
        processor_id = create_processor(
            config.PROJECT_ID,
            config.LOCATION,
            processor_type,
            display_name
        )
        
        if processor_id:
            created_processors[processor_type] = processor_id
    
    # Show results
    print("=== Results ===")
    if created_processors:
        print("✓ Successfully created processors:")
        for proc_type, proc_id in created_processors.items():
            print(f"  {proc_type}: {proc_id}")
        
        print("\n📝 Update your .env file with one of these processor IDs:")
        print("For best results with electoral PDFs, use FORM_PARSER_PROCESSOR:")
        if "FORM_PARSER_PROCESSOR" in created_processors:
            print(f"PROCESSOR_ID={created_processors['FORM_PARSER_PROCESSOR']}")
        
    else:
        print("❌ No processors were created successfully")

if __name__ == "__main__":
    main()