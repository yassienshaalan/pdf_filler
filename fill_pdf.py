from fillpdf import fillpdfs

class PDFFiller:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_form_field_names(self):
        """Attempts to retrieve the names of all fillable fields in the PDF."""
        try:
            fields = fillpdfs.get_form_fields(self.pdf_path)
            if fields:
                print("Form Field Names:", fields)
            else:
                print("No editable form fields found in the PDF.")
            return fields
        except Exception as e:
            print(f"An error occurred while trying to read the PDF: {e}")
            return None

    def check_for_editable_fields(self):
        """Checks if the PDF has editable form fields."""
        fields = self.get_form_field_names()
        return bool(fields)

    def fill_pdf_form(self, data_to_fill, output_pdf_path):
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfFileReader(file)
                pdf_writer = PyPDF2.PdfFileWriter()
                pdf_writer.appendPagesFromReader(pdf_reader)

                for page in range(pdf_reader.getNumPages()):
                    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(page), data_to_fill)

                with open(output_pdf_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
        except Exception as e:
            print(f"An error occurred while trying to fill the PDF: {e}")

    def fill_checkbox(self, field_name, value):
        """Fills a checkbox in the form."""
        # Implement logic to fill checkbox based on the library's capabilities
        pass

    def fill_radio_button(self, field_name, value):
        """Fills a radio button in the form."""
        # Implement logic to fill radio button based on the library's capabilities
        pass

# Example usage
pdf_path = 'modf-2212en-f.pdf'
pdf_filler = PDFFiller(pdf_path)

# Check for editable fields
if pdf_filler.check_for_editable_fields():
    # Fill form if editable fields are present
    data_to_fill = {
        'Account number': '22222',
        # Add other fields as needed
    }
    pdf_filler.fill_pdf_form(data_to_fill, 'modf-2212en-f_output.pdf')
else:
    print("The PDF does not contain editable fields. Cannot proceed with form filling.")
