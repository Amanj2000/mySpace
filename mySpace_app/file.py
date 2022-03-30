import openpyxl

def processCSV(file):
    file_data = file.read().decode('utf-8')
    lines = file_data.split('\n')

    rows = []
    for line in lines:
        rows.append(line.split(','))
    for entry in rows:
        print(entry)
    return rows

def processExcel(file):
    wb = openpyxl.load_workbook(file)
    rows = []
    for sheet in wb:
        for row in sheet.iter_rows(min_row=1):
            row_data = []
            for cell in row:
                row_data.append(str(cell.value))
            rows.append(row_data)
    return rows

