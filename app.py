import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import sys
import re

# Add the backend directory to the path so we can import main.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from backend.main import process_pdf

class PDFParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Page Number Parser")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
        self.status = tk.StringVar(value="Ready")
        
        self.create_widgets()
        self.setup_drop_target()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(
            main_frame, 
            text="PDF Page Number Parser", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Input PDF", padding=10)
        file_frame.pack(fill=tk.X, pady=10)
        
        # File path entry and browse button
        path_entry = ttk.Entry(file_frame, textvariable=self.pdf_path, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Output directory frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding=10)
        output_frame.pack(fill=tk.X, pady=10)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        output_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        output_btn.pack(side=tk.RIGHT)
        
        # Drop zone frame with instructions
        drop_frame = ttk.LabelFrame(main_frame, text="Drop Zone", padding=10)
        drop_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        drop_label = ttk.Label(
            drop_frame, 
            text="Drag and drop your PDF file here",
            font=("Helvetica", 12),
            anchor="center"
        )
        drop_label.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame with buttons and status
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        # Status label
        status_label = ttk.Label(bottom_frame, textvariable=self.status)
        status_label.pack(side=tk.LEFT)
        
        # Parse button
        self.parse_btn = ttk.Button(
            bottom_frame, 
            text="Parse PDF", 
            command=self.start_parsing,
            style="Accent.TButton"
        )
        self.parse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Configure style for accent button
        self.root.style = ttk.Style()
        self.root.style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))
        
    def setup_drop_target(self):
        # Configure root and frames as drop targets
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        
    def handle_drop(self, event):
        # Handle file drop event
        file_path = event.data
        
        # Clean up the file path (different OS formats)
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        
        # Handle Windows file paths with curly braces
        file_path = re.sub(r"[{}]", "", file_path)
        
        # Check if it's a PDF
        if file_path.lower().endswith('.pdf'):
            self.pdf_path.set(file_path)
            self.status.set(f"File loaded: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Invalid File", "Please select a PDF file.")
    
    def browse_file(self):
        # Open file dialog to select PDF
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.pdf_path.set(file_path)
            self.status.set(f"File loaded: {os.path.basename(file_path)}")
    
    def browse_output_dir(self):
        # Open dialog to select output directory
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir.set(dir_path)
    
    def start_parsing(self):
        # Validate input before starting
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        
        # Disable the parse button and start progress bar
        self.parse_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status.set("Processing PDF...")
        
        # Run processing in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_processing)
        thread.daemon = True
        thread.start()
    
    def run_processing(self):
        try:
            # Call the process_pdf function from main.py
            process_pdf(self.pdf_path.get(), self.output_dir.get())
            
            # Update UI when complete
            self.root.after(0, self.processing_complete, True, "PDF processing complete!")
        except Exception as e:
            # Handle errors
            self.root.after(0, self.processing_complete, False, f"Error: {str(e)}")
    
    def processing_complete(self, success, message):
        # Stop progress bar
        self.progress.stop()
        
        # Update status and re-enable parse button
        self.status.set(message)
        self.parse_btn.config(state=tk.NORMAL)
        
        # Show message box with result
        if success:
            messagebox.showinfo("Success", f"{message}\nOutput saved to: {self.output_dir.get()}")
        else:
            messagebox.showerror("Error", message)


if __name__ == "__main__":
    # Create TkinterDnD root (for drag and drop support)
    root = TkinterDnD.Tk()
    app = PDFParserApp(root)
    root.mainloop() 