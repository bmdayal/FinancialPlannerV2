#!/usr/bin/env python3
"""
Financial Planner Web Application Setup Script
Automated setup wizard for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class SetupWizard:
    def __init__(self):
        self.web_app_dir = Path(__file__).parent
        self.venv_dir = self.web_app_dir / 'venv'
        self.env_file = self.web_app_dir / '.env'
        self.env_example = self.web_app_dir / '.env.example'
        
    def print_header(self, text):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")
    
    def print_step(self, step_num, text):
        print(f"\n[{step_num}] {text}")
        print("-" * 60)
    
    def print_success(self, text):
        print(f"✅ {text}")
    
    def print_warning(self, text):
        print(f"⚠️  {text}")
    
    def print_error(self, text):
        print(f"❌ {text}")
    
    def run_command(self, command, description=""):
        """Run a shell command"""
        try:
            if description:
                print(f"→ {description}...")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.web_app_dir)
            )
            if result.returncode != 0:
                self.print_error(f"Command failed: {result.stderr}")
                return False
            if result.stdout:
                print(result.stdout.strip())
            return True
        except Exception as e:
            self.print_error(f"Error running command: {e}")
            return False
    
    def check_python(self):
        """Check if Python is installed"""
        self.print_step(1, "Checking Python installation")
        
        try:
            result = subprocess.run(
                [sys.executable, '--version'],
                capture_output=True,
                text=True
            )
            version = result.stdout.strip()
            self.print_success(f"Python {version} found")
            return True
        except Exception as e:
            self.print_error(f"Python not found: {e}")
            self.print_warning("Please install Python 3.8+ from https://www.python.org")
            return False
    
    def create_venv(self):
        """Create virtual environment"""
        self.print_step(2, "Setting up virtual environment")
        
        if self.venv_dir.exists():
            self.print_success("Virtual environment already exists")
            return True
        
        print(f"Creating virtual environment at {self.venv_dir}...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'venv', str(self.venv_dir)],
                check=True,
                cwd=str(self.web_app_dir)
            )
            self.print_success("Virtual environment created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_step(3, "Installing dependencies")
        
        # Determine pip command based on OS
        if sys.platform == 'win32':
            pip_cmd = str(self.venv_dir / 'Scripts' / 'pip.exe')
        else:
            pip_cmd = str(self.venv_dir / 'bin' / 'pip')
        
        requirements_file = self.web_app_dir / 'requirements.txt'
        
        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            return False
        
        try:
            subprocess.run(
                [pip_cmd, 'install', '-r', str(requirements_file)],
                check=True,
                cwd=str(self.web_app_dir)
            )
            self.print_success("Dependencies installed successfully")
            return True
        except Exception as e:
            self.print_error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_env_file(self):
        """Setup .env file"""
        self.print_step(4, "Setting up environment configuration")
        
        if self.env_file.exists():
            self.print_success(f".env file already exists at {self.env_file}")
            return True
        
        if not self.env_example.exists():
            self.print_error(".env.example not found")
            return False
        
        try:
            shutil.copy(self.env_example, self.env_file)
            self.print_success(f".env file created from template")
            
            # Read and display the file
            print("\nPlease edit .env and add your configuration:")
            print("-" * 60)
            with open(self.env_file, 'r') as f:
                print(f.read())
            print("-" * 60)
            
            return True
        except Exception as e:
            self.print_error(f"Failed to create .env file: {e}")
            return False
    
    def verify_api_key(self):
        """Verify OpenAI API key is configured"""
        self.print_step(5, "Verifying API configuration")
        
        try:
            with open(self.env_file, 'r') as f:
                content = f.read()
                if 'sk-' in content and 'OPENAI_API_KEY=' in content:
                    self.print_success("OpenAI API key appears to be configured")
                    return True
                else:
                    self.print_warning("OPENAI_API_KEY not configured in .env")
                    print("\nTo get an API key:")
                    print("1. Go to https://platform.openai.com/api-keys")
                    print("2. Create a new API key")
                    print("3. Copy the key and paste it in .env")
                    print("4. Run this script again")
                    return False
        except Exception as e:
            self.print_error(f"Failed to verify API key: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create platform-specific startup scripts"""
        self.print_step(6, "Creating startup scripts")
        
        # PowerShell script
        ps_script = self.web_app_dir / 'run.ps1'
        self.print_success("PowerShell script: run.ps1")
        
        # Batch script for Windows
        if sys.platform == 'win32':
            bat_script = self.web_app_dir / 'run.bat'
            self.print_success("Batch script: run.bat")
        
        # Shell script for Unix
        sh_script = self.web_app_dir / 'run.sh'
        if sh_script.exists():
            self.print_success("Shell script: run.sh")
        
        return True
    
    def print_next_steps(self):
        """Print instructions for running the app"""
        self.print_header("Setup Complete! 🎉")
        
        print("Next steps:")
        print("\n1. Edit .env file and add your OpenAI API key (if not already done):")
        print(f"   {self.env_file}")
        
        print("\n2. Run the web application:")
        
        if sys.platform == 'win32':
            print("\n   Option A (PowerShell):")
            print(f"   .\\run.ps1")
            print("\n   Option B (Command Prompt):")
            print(f"   run.bat")
        else:
            print("\n   chmod +x run.sh")
            print("   ./run.sh")
        
        print("\n3. Open your browser to:")
        print("   http://localhost:5000")
        
        print("\n" + "=" * 60)
        print("Documentation: See README.md for detailed information")
        print("=" * 60 + "\n")
    
    def run(self):
        """Run the complete setup"""
        self.print_header("Financial Planner Web Application Setup")
        
        steps = [
            ("Check Python", self.check_python),
            ("Create Virtual Environment", self.create_venv),
            ("Install Dependencies", self.install_dependencies),
            ("Setup Environment File", self.setup_env_file),
            ("Verify API Configuration", self.verify_api_key),
            ("Create Startup Scripts", self.create_startup_scripts),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                self.print_error(f"Setup failed at: {step_name}")
                return False
        
        self.print_next_steps()
        return True


if __name__ == '__main__':
    wizard = SetupWizard()
    success = wizard.run()
    sys.exit(0 if success else 1)
