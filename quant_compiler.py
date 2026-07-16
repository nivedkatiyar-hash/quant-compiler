import os
import subprocess
import sys
import argparse

def compile_bot(target_file, standalone=True, optimize_math=True):
    print(f"[*] Initializing Quant Compiler for: {target_file}")
    
    if not os.path.exists(target_file):
        print(f"[!] Error: {target_file} not found.")
        sys.exit(1)

    # Base Nuitka command
    command = [
        sys.executable, "-m", "nuitka",
        "--assume-yes-for-downloads",
        target_file
    ]

    if standalone:
        # Bundles the Python runtime so it can run on servers without Python installed
        command.append("--standalone")
        command.append("--onefile")

    if optimize_math:
        # Crucial for quant bots: enables Link Time Optimization for faster math
        command.append("--lto=yes") 

    print("[*] Translating Python to C and compiling binary...")
    print("[*] This may take a few minutes for complex trading algorithms...")
    
    try:
        subprocess.run(command, check=True)
        # Nuitka generates a binary with the same name as the script (e.g., bot.exe or bot.bin)
        base_name = os.path.splitext(target_file)[0]
        print(f"\n[+] Success! Highly optimized binary created for {base_name}")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Compilation failed. Check your C compiler setup: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quant Bot Compiler App")
    parser.add_argument("script", help="The Python bot script to compile (e.g., my_bot.py)")
    args = parser.parse_args()
    
    compile_bot(args.script)
