"""
Setup script to auto-start Voice Input with Windows
Run: python setup_autostart.py
"""

import os
import sys
import winreg as reg

def add_to_startup(exe_path=None):
    """Add application to Windows startup"""
    
    if exe_path is None:
        # Use current directory
        exe_path = os.path.join(os.getcwd(), "VoiceInput.exe")
    
    if not os.path.exists(exe_path):
        print(f"❌ Error: Could not find {exe_path}")
        print(f"💡 Make sure to build the exe first or provide the correct path")
        return False
    
    try:
        # Open registry key
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        # Open the key with write access
        registry_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        
        # Add the application
        reg.SetValueEx(registry_key, "VoiceInput", 0, reg.REG_SZ, exe_path)
        
        # Close the key
        reg.CloseKey(registry_key)
        
        print("✅ Voice Input added to Windows startup!")
        print(f"📁 Path: {exe_path}")
        print("\n💡 The app will now start automatically when Windows boots")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def remove_from_startup():
    """Remove application from Windows startup"""
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        registry_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        reg.DeleteValue(registry_key, "VoiceInput")
        reg.CloseKey(registry_key)
        
        print("✅ Voice Input removed from Windows startup")
        return True
        
    except FileNotFoundError:
        print("ℹ️ Voice Input was not in startup")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Voice Input - Startup Configuration")
    print("=" * 50)
    print("\n1. Add to startup")
    print("2. Remove from startup")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Check if custom path provided
        if len(sys.argv) > 1:
            exe_path = sys.argv[1]
        else:
            exe_path = None
        add_to_startup(exe_path)
    elif choice == "2":
        remove_from_startup()
    else:
        print("Exiting...")
    
    input("\nPress Enter to close...")