"""ACPI Analysis Tab"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json



class AnalysisTab:
    """ACPI analysis and device listing"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = ttk.Frame(parent)
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the analysis tab"""
        # Title
        title = ttk.Label(self.frame, text="ACPI Analysis - Device Discovery & Inspection")
        title.pack()
        
        # Control frame
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Refresh Analysis", 
                  command=self.refresh).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Export to JSON", 
                  command=self.export_json).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Show Statistics", 
                  command=self.show_stats).pack(side=tk.LEFT)
        
        # Device list
        list_frame = ttk.LabelFrame(self.frame, text="Discovered Devices")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('Name', 'HID', 'ADR', 'Type')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        # Configure columns
        self.tree.heading('#0', text='Path')
        self.tree.heading('Name', text='Name')
        self.tree.heading('HID', text='Hardware ID')
        self.tree.heading('ADR', text='Address')
        self.tree.heading('Type', text='Type')
        
        self.tree.column('#0', width=200)
        self.tree.column('Name', width=150)
        self.tree.column('HID', width=150)
        self.tree.column('ADR', width=100)
        self.tree.column('Type', width=100)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Info panel
        info_frame = ttk.LabelFrame(self.frame, text="Device Information")
        info_frame.pack(fill=tk.X)
        
        self.info_text = tk.Text(info_frame, height=6, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_device_select)
    
    def refresh(self):
        """Refresh device list"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add devices
        if self.main_app.acpi_entries:
            for device in self.main_app.acpi_entries:
                self.tree.insert('', 'end', 
                               text=f"Device: {device.get('name', 'Unknown')}",
                               values=(
                                   device.get('name', ''),
                                   device.get('hid', ''),
                                   device.get('adr', ''),
                                   'Device'
                               ))
            
            self.main_app.update_status(f"Analysis: {len(self.main_app.acpi_entries)} devices found")
        else:
            self.tree.insert('', 'end', text='No ACPI data loaded',
                           values=('', '', '', ''))
    
    def on_device_select(self, event):
        """Handle device selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            info = f"""Device Information:
            
Name: {values[0]}
Hardware ID: {values[1]}
Address: {values[2]}
Type: {values[3]}

This device was discovered in the ACPI tables.
"""
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', info)
    
    def export_json(self):
        """Export analysis to JSON"""
        if not self.main_app.acpi_entries:
            messagebox.showwarning("No Data", "No ACPI data to export")
            return
        
        data = self.main_app.acpi_parser.export_to_dict()
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", f"Exported to {filepath}")
    
    def show_stats(self):
        """Show analysis statistics"""
        if not self.main_app.acpi_entries:
            messagebox.showinfo("Statistics", "No ACPI data loaded")
            return
        
        data = self.main_app.acpi_parser.export_to_dict()
        stats = data.get('stats', {})
        
        message = f"""ACPI Analysis Statistics:

Devices: {stats.get('device_count', 0)}
Methods: {stats.get('method_count', 0)}
Scopes: {stats.get('scope_count', 0)}

File: {self.main_app.current_file.name if self.main_app.current_file else 'None'}
"""
        messagebox.showinfo("Statistics", message)
