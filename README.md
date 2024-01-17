# PDFFiller

`PDFFiller` is a Python utility for interacting with PDF files, particularly for filling out form fields. It leverages the `fillpdf` library to read and write PDF form fields, making it easy to automate the process of filling out PDF forms programmatically.

## Features

- Retrieve names of fillable fields in a PDF.
- Fill out PDF forms programmatically.
- Error handling for PDFs that cannot be read or do not contain fillable fields.

## Requirements

- Python 3.x
- `fillpdf`
- `pdfrw`

You can install the required packages using pip:

```bash
pip install fillpdf pdfrw
```

## Usage
To use PDFFiller, first initialize it with the path to your PDF file:
```
from fill_pdf import PDFFiller

pdf_path = 'path_to_your_pdf.pdf'
pdf_filler = PDFFiller(pdf_path)
```
### Retrieving Form Field Names
To get the names of fillable fields in the PDF:
```
fields = pdf_filler.get_form_field_names()
```
Filling a PDF Form
To fill out the form:
```
data_to_fill = {
    'field_name_1': 'value_1',
    'field_name_2': 'value_2',
    # Add other fields as needed
}
pdf_filler.fill_pdf_form(data_to_fill, 'output_pdf_path.pdf')
```
Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

License
MIT
```
This README provides a clear overview of what your project does, how to set it up, and how to use it. You can further customize it to add more details such as a background for the project, more in-depth usage examples, screenshots (if applicable), and any other information that you think might be helpful for users. 

Remember to replace placeholder text like `path_to_your_pdf.pdf` and `output_pdf_path.pdf` with relevant information or examples.
```

