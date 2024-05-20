# Creating pixel perfect reports

- Data are coming from GoodData's universal semantic layer.
- Desired parts are loaded into frames using pandas factory.
- All put together in HTML format and generated into PDF.

Disclaimer: libraries used to achieve this functionality are picked based on ease of use, if you prefer any other library feel free to consult with last chapter.

## Installation

1. Prepare python virtual environment (or install system-wide = leave out this step)

```shell
python -m venv venv
source venv/bin/activate
```

2. Install dependent libraries

```shell
pip install gooddata-pandas  # access semantic layer
pip install plotly kaleido  # exporting visuals to PNG
pip install jinja2  # templating system for HTML
pip install weasyprint  # generate PDF from HTML
```

alternatively install from requirements file:

```shell
pip install -r requirements.txt
```

3. Generate the PDF report

```shell
python report.py
```

###  Options to consider

- Multiple visualization libraries options:
    - [Plotly: Low-Code Data App Development](https://plotly.com/)
    - [seaborn: statistical data visualization](https://seaborn.pydata.org/index.html)
    - [Save Matplotlib Figure as SVG and PDF using Python - GeeksforGeeks](https://www.geeksforgeeks.org/save-matplotlib-figure-as-svg-and-pdf-using-python/)
- HTML to PDF generation library ([overview](https://dev.to/bowmanjd/python-pdf-generation-from-html-with-weasyprint-538h)):
    - [pyPDF](https://pypi.org/project/pypdf/)
    - [ReportLab](https://pypi.org/project/reportlab/)
    - [WeasyPrint](https://weasyprint.org/) (tool of choice)
- https://stackoverflow.com/questions/70384455/how-to-arrange-objects-in-rows-and-columns-and-export-in-svg
