import os
import fitz  # PyMuPDF

# Hardcoded directory path
directory = "D:\\Music"

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".pdf") and "Piano 4 Hands" in filename and "Prepared" not in filename:
        print(f"\nFound file: {filename}")
        process = input("Would you like to process this file? (y/n): ")
        if process.lower() == 'y':
            # Ask user for number of pages to skip
            while True:
                try:
                    skip_pages = int(input("How many pages would you like to skip? "))
                    if skip_pages < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid non-negative integer.")
            
            # Ask user if they want to reverse each pair of pages
            reverse_pair = input("Would you like to reverse each pair of pages? (y/n): ").lower() == 'y'
            
            # Process the PDF file
            filepath = os.path.join(directory, filename)
            doc = fitz.open(filepath)
            total_pages = doc.page_count
            print(f"Total pages in the document: {total_pages}")
            
            # Create a new PDF document for the output
            new_doc = fitz.open()
            pages_to_process = list(range(skip_pages, total_pages))
            
            # Split the pages into pairs
            pairs = [pages_to_process[i:i + 2] for i in range(0, len(pages_to_process), 2)]
            
            for pair in pairs:
                if len(pair) == 1:
                    # Only one page left; insert it as is
                    new_doc.insert_pdf(doc, from_page=pair[0], to_page=pair[0])
                else:
                    # Load the two pages
                    page1 = doc.load_page(pair[0])
                    page2 = doc.load_page(pair[1])
                    
                    # Get dimensions of each page
                    width1, height1 = page1.rect.width, page1.rect.height
                    width2, height2 = page2.rect.width, page2.rect.height
                    
                    # Calculate dimensions for the new combined page
                    new_width = width1 + width2
                    new_height = max(height1, height2)
                    
                    # Create a new page in the output document
                    new_page = new_doc.new_page(width=new_width, height=new_height)
                    
                    if reverse_pair:
                        # Place page1 on the right and page2 on the left
                        new_page.show_pdf_page(fitz.Rect(0, 0, width2, height2), doc, pair[1])
                        new_page.show_pdf_page(fitz.Rect(width2, 0, new_width, height1), doc, pair[0])
                    else:
                        # Place page1 on the left and page2 on the right
                        new_page.show_pdf_page(fitz.Rect(0, 0, width1, height1), doc, pair[0])
                        new_page.show_pdf_page(fitz.Rect(width1, 0, new_width, height2), doc, pair[1])
            
            # Save the new PDF with " Prepared" appended to the filename
            base_filename, ext = os.path.splitext(filename)
            new_filename = base_filename + " Prepared" + ext
            new_filepath = os.path.join(directory, new_filename)
            new_doc.save(new_filepath)
            print(f"Processed file saved as: {new_filename}")

# Ask if user wants to delete all files that have a "Prepared" version created
delete_prepared_files = input("\nWould you like to delete all files that have a 'Prepared' version? (y/n): ")
if delete_prepared_files.lower() == 'y':
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and "Piano 4 Hands" in filename and "Prepared" in filename:
            original_filename = filename.replace(" Prepared", "")
            original_filepath = os.path.join(directory, original_filename + ".pdf")
            if os.path.exists(original_filepath):
                os.remove(original_filepath)
                print(f"Deleted original file: {original_filepath}")