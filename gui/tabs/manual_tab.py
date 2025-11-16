"""Manual Patches Tab"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import tempfile
import os



class ManualTab:
    """Manual patch editing and templates"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = ttk.Frame(parent)
        self.current_template = None
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the manual tab"""
        # Title
        title = ttk.Label(self.frame, text="Manual Patches - Template Editor")
        title.pack()
        
        # Control frame
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Label(control_frame, text="Template:").pack(side=tk.LEFT)
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(control_frame, textvariable=self.template_var,
                                          width=30, state='readonly')
        self.template_combo['values'] = self.get_template_list()
        self.template_combo.pack(side=tk.LEFT)
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_select)
        
        ttk.Button(control_frame, text="Load Template", 
                  command=self.load_template).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Save As...", 
                  command=self.save_file).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Clear", 
                  command=self.clear_editor).pack(side=tk.LEFT)
        
        # Editor frame
        editor_frame = ttk.LabelFrame(self.frame, text="SSDT Editor")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text editor with scrollbar
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        self.editor = tk.Text(editor_container, wrap=tk.NONE, 
                             undo=True, maxundo=-1)
        
        vsb = ttk.Scrollbar(editor_container, orient="vertical", command=self.editor.yview)
        hsb = ttk.Scrollbar(editor_container, orient="horizontal", command=self.editor.xview)
        self.editor.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.editor.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        editor_container.grid_rowconfigure(0, weight=1)
        editor_container.grid_columnconfigure(0, weight=1)
        
        # Info panel
        info_frame = ttk.LabelFrame(self.frame, text="Template Information")
        info_frame.pack(fill=tk.X)
        
        self.info_label = ttk.Label(info_frame, text="Select a template to begin")
        self.info_label.pack(anchor=tk.W)
    
    def get_template_list(self):
        """Get list of available templates"""
        templates = []
        for patch in self.main_app.patch_manager.patches:
            templates.append(patch.name)
        return templates
    
    def on_template_select(self, event):
        """Handle template selection"""
        self.load_template()
    
    def load_template(self):
        """Load selected template"""
        template_name = self.template_var.get()
        if not template_name:
            messagebox.showwarning("No Selection", "Please select a template")
            return
        
        # Find patch info
        patch = None
        for p in self.main_app.patch_manager.patches:
            if p.name == template_name:
                patch = p
                break
        
        if not patch:
            return
        
        # Get template content
        content = self.get_template_content(template_name)
        
        # Load into editor
        self.editor.delete('1.0', tk.END)
        self.editor.insert('1.0', content)
        
        # Update info
        self.info_label.config(text=f"{patch.name} - {patch.description}\n"
                                   f"Category: {patch.category} | Priority: {patch.priority}")
        
        self.current_template = template_name
        self.main_app.update_status(f"Loaded template: {template_name}")
    
    def get_template_content(self, template_name):
        """Get template content"""
        from core.generators import AdvancedGenerators
        
        temp_file = tempfile.mktemp(suffix='.dsl')
        
        try:
            result = AdvancedGenerators.generate_from_template(template_name, temp_file)
            
            if result and os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                os.remove(temp_file)
                return content
            else:
                return f"// {template_name}\n// Template not found\n// Please add your ACPI code here\n"
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return f"// {template_name}\n// Error loading template: {str(e)}\n// Please add your ACPI code here\n"
    
    def save_file(self):
        """Save current content to file"""
        content = self.editor.get('1.0', tk.END)
        
        if not content.strip():
            messagebox.showwarning("Empty Content", "Nothing to save")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".dsl",
            filetypes=[("DSL Files", "*.dsl"), ("All Files", "*.*")],
            initialfile=f"{self.current_template}.dsl" if self.current_template else "SSDT.dsl"
        )
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Saved to {filepath}")
            self.main_app.update_status(f"Saved: {Path(filepath).name}")
    
    def clear_editor(self):
        """Clear the editor"""
        if messagebox.askyesno("Clear Editor", "Clear all content?"):
            self.editor.delete('1.0', tk.END)
            self.current_template = None
            self.info_label.config(text="Select a template to begin")
            self.main_app.update_status("Editor cleared")
    
    def refresh(self):
        """Refresh the tab"""
        self.template_combo['values'] = self.get_template_list()
