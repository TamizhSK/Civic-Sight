#!/usr/bin/env python3
"""
GCP Document AI Setup Script
This script helps you:
1. List available processor types
2. Create a new processor
3. Get the processor ID for your .env file
"""

import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import config

def fetch_processor_types(project_id: str, location: str) -> None:
    """Fetch and display available processor types."""
    print(f"Fetching processor types for project: {project_id} in location: {location}")
    
    # Set the API endpoint for the location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # The full resource name of the location
    parent = client.common_location_path(project_id, location)
    
    try:
        # Fetch all processor types
        response = client.fetch_processor_types(parent=parent)
        
        print("\nAvailable processor types:")
        print("-" * 50)
        
        for processor_type in response.processor_types:
            if processor_type.allow_creation:
                print(f"Type: {processor_type.type_}")
                print(f"  Category: {processor_type.category}")
                print(f"  Available Locations: {list(processor_type.available_locations)}")
                print()
                
    except Exception as e:
        print(f"Error fetching processor types: {e}")
        print("\nPlease ensure:")
        print("1. Your project ID is correct")
        print("2. Document AI API is enabled")
        print("3. You have proper authentication set up")

def create_processor(project_id: str, location: str, processor_type: str = "FORM_PARSER_PROCESSOR") -> str:
    """Create a new Document AI processor."""
    print(f"Creating processor of type: {processor_type}")
    
    # Set the API endpoint for the location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # The full resource name of the location
    parent = client.common_location_path(project_id, location)
    
    try:
        # Create processor request
        processor = documentai.Processor(
            display_name="PDF Electoral Data Parser",
            type_=processor_type
        )
        
        request = documentai.CreateProcessorRequest(
            parent=parent,
            processor=processor
        )
        
        # Create the processor
        operation = client.create_processor(request=request)
        print("Waiting for processor creation...")
        
        result = operation.result()
        
        # Extract processor ID from the name
        processor_id = result.name.split("/")[-1]
        
        print(f"✓ Processor created successfully!")
        print(f"Processor ID: {processor_id}")
        print(f"Full name: {result.name}")
        
        return processor_id
        
    except Exception as e:
        print(f"Error creating processor: {e}")
        return ""

def list_existing_processors(project_id: str, location: str) -> None:
    """List existing processors in the project."""
    print(f"Listing existing processors for project: {project_id}")
    
    # Set the API endpoint for the location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # The full resource name of the location
    parent = client.common_location_path(project_id, location)
    
    try:
        # List processors
        response = client.list_processors(parent=parent)
        
        print("\nExisting processors:")
        print("-" * 50)
        
        for processor in response.processors:
            processor_id = processor.name.split("/")[-1]
            print(f"Name: {processor.display_name}")
            print(f"  ID: {processor_id}")
            print(f"  Type: {processor.type_}")
            print(f"  State: {processor.state.name}")
            print()
            
    except Exception as e:
        print(f"Error listing processors: {e}")

def main():
    """Main setup function."""
    print("=== GCP Document AI Setup ===")
    
    # Check if we have project ID
    if not config.PROJECT_ID:
        print("❌ PROJECT_ID not found in .env file!")
        print("Please update your .env file with your GCP project ID")
        return
    
    print(f"Project ID: {config.PROJECT_ID}")
    print(f"Location: {config.LOCATION}")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. List available processor types")
        print("2. List existing processors")
        print("3. Create a new processor")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            fetch_processor_types(config.PROJECT_ID, config.LOCATION)
            
        elif choice == "2":
            list_existing_processors(config.PROJECT_ID, config.LOCATION)
            
        elif choice == "3":
            print("\nAvailable processor types for PDF parsing:")
            print("1. FORM_PARSER_PROCESSOR (recommended for structured documents)")
            print("2. OCR_PROCESSOR (basic text extraction)")
            print("3. GENERAL_PROCESSOR (general document processing)")
            
            type_choice = input("Choose processor type (1-3): ").strip()
            
            processor_types = {
                "1": "FORM_PARSER_PROCESSOR",
                "2": "OCR_PROCESSOR", 
                "3": "GENERAL_PROCESSOR"
            }
            
            if type_choice in processor_types:
                processor_id = create_processor(
                    config.PROJECT_ID, 
                    config.LOCATION, 
                    processor_types[type_choice]
                )
                
                if processor_id:
                    print(f"\n✓ Success! Add this to your .env file:")
                    print(f"PROCESSOR_ID={processor_id}")
            else:
                print("Invalid choice")
                
        elif choice == "4":
            break
            
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()