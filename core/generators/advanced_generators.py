"""Advanced SSDT generators using Dortania templates"""

from pathlib import Path


class AdvancedGenerators:
    """Generate advanced SSDTs from templates"""
    
    TEMPLATE_DIR = Path(__file__).parent / "templates"
    
    @staticmethod
    def _load_template(template_name):
        """Load template file content"""
        template_path = AdvancedGenerators.TEMPLATE_DIR / template_name
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    @staticmethod
    def _write_template(template_name, output_path):
        """Load and write template to output"""
        content = AdvancedGenerators._load_template(template_name)
        if content:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    @staticmethod
    def generate_xosi(output_path):
        """Generate SSDT-XOSI for OS compatibility"""
        return AdvancedGenerators._write_template("SSDT-XOSI.dsl", output_path)
    
    @staticmethod
    def generate_gpu_disable(output_path):
        """Generate SSDT-GPU-DISABLE to disable discrete GPU"""
        return AdvancedGenerators._write_template("SSDT-GPU-DISABLE.dsl", output_path)
    
    @staticmethod
    def generate_gpu_spoof(output_path):
        """Generate SSDT-GPU-SPOOF to spoof GPU device ID"""
        return AdvancedGenerators._write_template("SSDT-GPU-SPOOF.dsl", output_path)
    
    @staticmethod
    def generate_dgpu_off(output_path):
        """Generate SSDT-dGPU-Off alternative discrete GPU disable"""
        return AdvancedGenerators._write_template("SSDT-dGPU-Off.dsl", output_path)
    
    @staticmethod
    def generate_nohybgfx(output_path):
        """Generate SSDT-NoHybGfx to disable hybrid graphics"""
        return AdvancedGenerators._write_template("SSDT-NoHybGfx.dsl", output_path)
    
    @staticmethod
    def generate_rhub(output_path):
        """Generate SSDT-RHUB for USB reset"""
        return AdvancedGenerators._write_template("SSDT-RHUB.dsl", output_path)
    
    @staticmethod
    def generate_rhub_prebuilt(output_path):
        """Generate SSDT-RHUB-prebuilt alternative"""
        return AdvancedGenerators._write_template("SSDT-RHUB-prebuilt.dsl", output_path)
    
    @staticmethod
    def generate_rtc0_range(output_path):
        """Generate SSDT-RTC0-RANGE for HEDT systems"""
        return AdvancedGenerators._write_template("SSDT-RTC0-RANGE-HEDT.dsl", output_path)
    
    @staticmethod
    def generate_unc(output_path):
        """Generate SSDT-UNC for HEDT uncore bridge"""
        return AdvancedGenerators._write_template("SSDT-UNC.dsl", output_path)
    
    @staticmethod
    def generate_cpur(output_path):
        """Generate SSDT-CPUR for CPU renaming"""
        return AdvancedGenerators._write_template("SSDT-CPUR.dsl", output_path)
    
    @staticmethod
    def generate_imei(output_path):
        """Generate SSDT-IMEI-S for IMEI device"""
        return AdvancedGenerators._write_template("SSDT-IMEI-S.dsl", output_path)
    
    @staticmethod
    def generate_ec_usbx_desktop(output_path):
        """Generate combined SSDT-EC-USBX for desktop"""
        return AdvancedGenerators._write_template("SSDT-EC-USBX-DESKTOP.dsl", output_path)
    
    @staticmethod
    def generate_ec_usbx_laptop(output_path):
        """Generate combined SSDT-EC-USBX for laptop"""
        return AdvancedGenerators._write_template("SSDT-EC-USBX-LAPTOP.dsl", output_path)
    
    @staticmethod
    def generate_plug_drtnia(output_path):
        """Generate SSDT-PLUG-DRTNIA alternative"""
        return AdvancedGenerators._write_template("SSDT-PLUG-DRTNIA.dsl", output_path)
    
    @staticmethod
    def generate_from_template(patch_name, output_path):
        """Generic generator that finds and uses template files"""
        # Try exact match first
        template_file = f"{patch_name}.dsl"
        if AdvancedGenerators._write_template(template_file, output_path):
            return True
        
        # Try to find similar template
        import os
        template_dir = AdvancedGenerators.TEMPLATE_DIR
        if template_dir.exists():
            # Look for files that start with the patch name
            for file in os.listdir(template_dir):
                if file.startswith(patch_name) and file.endswith('.dsl'):
                    if AdvancedGenerators._write_template(file, output_path):
                        return True
        
        # If no template found, create a basic placeholder
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"/*\n * {patch_name}\n * Template not found - Please customize\n */\n")
            f.write(f"DefinitionBlock (\"\", \"SSDT\", 2, \"ACPI\", \"{patch_name.replace('SSDT-', '')}\", 0x00000000)\n")
            f.write("{\n    // Add your ACPI code here\n}\n")
        return True
