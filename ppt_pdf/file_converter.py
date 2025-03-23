import os
import win32com.client
import pythoncom
from pathlib import Path

class FileConverter:
    def __init__(self):
        # Initialize COM for the current thread
        pythoncom.CoInitialize()
        self.powerpoint = win32com.client.Dispatch("Powerpoint.Application")
        self.word = win32com.client.Dispatch("Word.Application")
        self.excel = win32com.client.Dispatch("Excel.Application")
        
    def convert_to_pdf(self, input_file):
        file_path = Path(input_file).resolve()
        output_pdf = file_path.with_suffix('.pdf')
        
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension in ['.pptx', '.ppt']:
                presentation = self.powerpoint.Presentations.Open(str(file_path))
                presentation.SaveAs(str(output_pdf), 32)  # 32 represents PDF format
                presentation.Close()
                
            elif file_extension in ['.docx', '.doc']:
                doc = self.word.Documents.Open(str(file_path))
                doc.SaveAs(str(output_pdf), FileFormat=17)  # 17 represents PDF format
                doc.Close()
                
            elif file_extension in ['.xlsx', '.xls']:
                wb = self.excel.Workbooks.Open(str(file_path))
                wb.ExportAsFixedFormat(0, str(output_pdf))  # 0 represents PDF format
                wb.Close()
                
            return str(output_pdf)
            
        except Exception as e:
            return f"Error converting file: {str(e)}"
        
    def __del__(self):
        try:
            self.powerpoint.Quit()
            self.word.Quit()
            self.excel.Quit()
            pythoncom.CoUninitialize()
        except:
            pass