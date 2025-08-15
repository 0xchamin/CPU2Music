#!/usr/bin/env python3
"""
Simple CPU instruction tracer using GDB commands
"""
import subprocess
import json
import os

def trace_cpu_instructions(program_name, name_input):
    """Trace CPU instructions using GDB subprocess"""
    
    # Create GDB command script
    gdb_commands = f"""
set logging file cpu_instructions.log
set logging overwrite on
set logging on
set args "{name_input}"
break process_name
run
set logging off
quit
"""
    
    # Write commands to file
    with open('trace_commands.gdb', 'w') as f:
        f.write(gdb_commands)
    
    # Run GDB with commands
    try:
        result = subprocess.run([
            'gdb', '-batch', '-x', 'trace_commands.gdb', program_name
        ], capture_output=True, text=True)
        
        print("GDB output:")
        print(result.stdout)
        if result.stderr:
            print("GDB errors:")
            print(result.stderr)
            
        return True
    except Exception as e:
        print(f"Error running GDB: {e}")
        return False

def create_mock_trace_data(name_input):
    """Create mock CPU trace data for testing"""
    
    # Simulate CPU instructions based on name
    instructions = []
    notes = []
    rhythms = []
    instruments = []
    
    # Basic simulation based on name characters
    for i, char in enumerate(name_input):
        ascii_val = ord(char)
        
        # Create mock instruction
        instruction = {
            'step': i,
            'pc': f'0x{(0x555555555000 + i * 4):x}',
            'instruction': f'mov ${ascii_val},%eax' if i % 2 == 0 else f'add ${ascii_val},%ebx',
            'registers': {
                'rax': f'0x{ascii_val:x}',
                'rbx': f'0x{(ascii_val * 2):x}',
                'rcx': f'0x{(ascii_val * 3):x}'
            }
        }
        instructions.append(instruction)
        
        # Convert to musical data
        note_map = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        notes.append(note_map[ascii_val % 7])
        rhythms.append(0.25 if ascii_val % 2 == 0 else 0.5)
        instruments.append(['piano', 'guitar', 'violin'][ascii_val % 3])
    
    return {
        'tempo': 120 + (len(name_input) * 10),
        'key': 'C',
        'notes': notes,
        'rhythms': rhythms,
        'instruments': instruments,
        'metadata': {
            'total_instructions': len(instructions),
            'name_processed': name_input
        },
        'raw_instructions': instructions
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 simple_tracer.py <name>")
        sys.exit(1)
    
    name = sys.argv[1]
    print(f"Processing name: {name}")
    
    # Try actual GDB tracing first
    success = trace_cpu_instructions('./name_processor', name)
    
    if not success:
        print("GDB tracing failed, creating simulated trace data...")
    
    # Create musical data (simulated for now)
    musical_data = create_mock_trace_data(name)
    
    # Save to JSON
    with open('musical_data.json', 'w') as f:
        json.dump(musical_data, f, indent=2)
    
    print(f"Musical data created for '{name}'")
    print(f"Tempo: {musical_data['tempo']} BPM")
    print(f"Notes: {len(musical_data['notes'])}")
    print("Saved to: musical_data.json")
    print("\nYou can now open audio_generator.html and load this file!")