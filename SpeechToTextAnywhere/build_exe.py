"""
Script to build standalone executable
Run: python build_exe.py
"""

from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = [
        'global_voice_input.py',           # Your script name
        '--onefile',                        # Single exe file
        '--windowed',                       # No console window
        '--name=VoiceInput',               # Name of the exe
        '--hidden-import=pystray._win32',  # Include hidden imports
        '--hidden-import=PIL._tkinter_finder',
        '--clean',                          # Clean build
    ]
    
    run(opts)
    
    print("\n" + "="*50)
    print("✅ Build complete!")
    print("📁 Find your exe in: dist/VoiceInput.exe")
    print("="*50)