from fillpdf import fillpdfs
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import math 

class PDFFiller:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_form_field_names(self):
        """Attempts to retrieve the names of all fillable fields in the PDF."""
        try:
            fields = fillpdfs.get_form_fields(self.pdf_path)
            print("fields",fields)
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
        print("Checks if the PDF has editable form fields")
        fields = self.get_form_field_names()
        return bool(fields)

    def fill_pdf_form(self, data_to_fill, output_pdf_path, flatten=False):
        """Fills the PDF form with the provided data using fillpdfs library."""
        print(f"Filling form from {self.pdf_path} to {output_pdf_path} with data: {data_to_fill}")
        try:
            fillpdfs.write_fillable_pdf(self.pdf_path, output_pdf_path, data_to_fill, flatten)
            print("Form filling completed.")
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
   
    def get_text_elements(self):
        """Extracts text elements and their positions from the PDF."""
        text_elements = {}
        for page_layout in extract_pages(self.pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        text = text_line.get_text().strip()
                        if text:
                            # The position of the text element (x, y)
                            x, y, _, _ = text_line.bbox
                            text_elements[text] = (x, y)
        return text_elements

    def calculate_distance(self, pos1, pos2):
        """Calculates the Euclidean distance between two positions."""
        if len(pos1) < 2 or len(pos2) < 2:
            raise ValueError("Positions must have at least two elements (x, y coordinates).")
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def automatic_field_mapping(self):
        """Automatically maps field names to the closest non-editable text."""
        text_elements = self.get_text_elements()
        form_fields = fillpdfs.get_form_fields(self.pdf_path)
        print("in automatic mapping",form_fields)
        mapping = {}

        if form_fields is None:
            print("No form fields found in the PDF.")
            return

        for field_name, field_info in form_fields.items():
            print("field_name",field_name,"field_info",field_info)
            if field_info is None or 'rect' not in field_info or len(field_info['rect']) < 4:
                print(f"Warning: Skipping field {field_name} due to missing or invalid position data.")
                continue
            field_pos = field_info['rect'][:2]  # Extracting x, y from rect
            print("field_pos",field_pos)
            closest_text, min_distance = None, float('inf')
            for text, text_pos in text_elements.items():
                print("text",text,"text_pos",text_pos)
                try:
                    distance = self.calculate_distance(field_pos, text_pos)
                    if distance < min_distance:
                        closest_text, min_distance = text, distance
                except ValueError as e:
                    print(f"Error calculating distance for field '{field_name}': {e}")
                    continue

            if closest_text:
                mapping[field_name] = closest_text

        self.field_mapping = mapping
        print("self.field_mapping",self.field_mapping)

# Example usage
file_name = 'ex.pdf'
pdf_path = './examples/'+file_name
pdf_filler = PDFFiller(pdf_path)
pdf_filler.automatic_field_mapping()
# Check for editable fields
if pdf_filler.check_for_editable_fields():
    # Fill form if editable fields are present
    user_data = {
        'Address': '27 leo Drive',
    }
    technical_data = {pdf_filler.field_mapping.get(key, key): value for key, value in user_data.items()}
    print("technical_data")
    print(technical_data)
    pdf_filler.fill_pdf_form(technical_data, './examples/'+file_name+'_output.pdf')
else:
    print("The PDF does not contain editable fields. Cannot proceed with form filling.")
