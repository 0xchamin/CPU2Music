#!/usr/bin/env python3
"""
CPU Trace to Music Converter
Converts actual CPU instruction traces into musical data
"""

import json
import re
from collections import defaultdict

class CPUTraceToMusic:
    def __init__(self, trace_file='cpu_trace.json'):
        self.trace_file = trace_file
        self.trace_data = None
        self.musical_data = {
            'notes': [],
            'rhythms': [],
            'instruments': [],
            'tempo': 120,
            'key': 'C',
            'metadata': {}
        }
        
        # Musical mappings
        self.instruction_to_note = {
            'mov': 'C4',
            'add': 'D4', 
            'sub': 'E4',
            'mul': 'F4',
            'div': 'G4',
            'cmp': 'A4',
            'jmp': 'B4',
            'call': 'C5',
            'ret': 'D5',
            'push': 'E5',
            'pop': 'F5',
            'lea': 'G5',
            'xor': 'A5',
            'and': 'B5',
            'or': 'C6'
        }
        
        self.register_to_instrument = {
            'rax': 'piano',
            'rbx': 'guitar', 
            'rcx': 'violin',
            'rdx': 'flute',
            'rsi': 'trumpet',
            'rdi': 'drums',
            'rbp': 'bass',
            'rsp': 'synth'
        }
    
    def load_trace(self):
        """Load CPU trace data from JSON file"""
        try:
            with open(self.trace_file, 'r') as f:
                self.trace_data = json.load(f)
            print(f"Loaded trace with {len(self.trace_data['instructions'])} instructions")
            return True
        except FileNotFoundError:
            print(f"Error: {self.trace_file} not found")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.trace_file}")
            return False
    
    def analyze_instructions(self):
        """Analyze CPU instructions and convert to musical elements"""
        if not self.trace_data:
            return
        
        instructions = self.trace_data['instructions']
        notes = []
        rhythms = []
        instruments = []
        
        for i, entry in enumerate(instructions):
            instruction = entry['instruction']
            registers = entry['registers']
            
            # Extract instruction opcode
            opcode = self.extract_opcode(instruction)
            
            # Map instruction to musical note
            note = self.instruction_to_note.get(opcode, 'C4')
            notes.append(note)
            
            # Calculate rhythm from instruction complexity
            rhythm = self.calculate_rhythm(instruction, registers)
            rhythms.append(rhythm)
            
            # Determine instrument from active registers
            instrument = self.determine_instrument(registers)
            instruments.append(instrument)
        
        self.musical_data['notes'] = notes
        self.musical_data['rhythms'] = rhythms  
        self.musical_data['instruments'] = instruments
        
        # Calculate tempo from instruction frequency
        self.musical_data['tempo'] = self.calculate_tempo()
        
        # Determine key from register patterns
        self.musical_data['key'] = self.determine_key()
    
    def extract_opcode(self, instruction):
        """Extract opcode from assembly instruction"""
        if not instruction or instruction == 'unknown':
            return 'mov'
        
        # Split instruction and get first part (opcode)
        parts = instruction.split()
        if parts:
            opcode = parts[0].lower()
            # Remove suffixes like 'movq' -> 'mov'
            base_opcodes = ['mov', 'add', 'sub', 'mul', 'div', 'cmp', 'jmp', 
                           'call', 'ret', 'push', 'pop', 'lea', 'xor', 'and', 'or']
            for base in base_opcodes:
                if opcode.startswith(base):
                    return base
            return opcode
        return 'mov'
    
    def calculate_rhythm(self, instruction, registers):
        """Calculate rhythm duration based on instruction complexity"""
        base_duration = 0.25  # Quarter note
        
        # Simple instructions = shorter notes
        simple_ops = ['mov', 'push', 'pop']
        complex_ops = ['mul', 'div', 'call']
        
        opcode = self.extract_opcode(instruction)
        
        if opcode in simple_ops:
            return base_duration
        elif opcode in complex_ops:
            return base_duration * 2
        else:
            return base_duration * 1.5
    
    def determine_instrument(self, registers):
        """Determine instrument based on which registers are active"""
        # Find register with most significant value
        max_reg = 'rax'  # default
        max_val = 0
        
        for reg, val_str in registers.items():
            if val_str != 'unknown':
                try:
                    # Convert hex string to int
                    val = int(val_str, 16) if val_str.startswith('0x') else 0
                    if val > max_val:
                        max_val = val
                        max_reg = reg
                except:
                    pass
        
        return self.register_to_instrument.get(max_reg, 'piano')
    
    def calculate_tempo(self):
        """Calculate tempo based on instruction density"""
        if not self.trace_data or len(self.trace_data['instructions']) == 0:
            return 120
        
        # More instructions = faster tempo
        instruction_count = len(self.trace_data['instructions'])
        
        if instruction_count < 100:
            return 90   # Slow
        elif instruction_count < 500:
            return 120  # Medium
        else:
            return 150  # Fast
    
    def determine_key(self):
        """Determine musical key from register value patterns"""
        if not self.trace_data:
            return 'C'
        
        # Analyze register value patterns
        register_sums = defaultdict(int)
        
        for entry in self.trace_data['instructions']:
            registers = entry['registers']
            for reg, val_str in registers.items():
                if val_str != 'unknown':
                    try:
                        val = int(val_str, 16) if val_str.startswith('0x') else 0
                        register_sums[reg] += val
                    except:
                        pass
        
        # Map dominant register to key
        if register_sums:
            dominant_reg = max(register_sums, key=register_sums.get)
            key_map = {
                'rax': 'C', 'rbx': 'D', 'rcx': 'E', 'rdx': 'F',
                'rsi': 'G', 'rdi': 'A', 'rbp': 'B', 'rsp': 'C'
            }
            return key_map.get(dominant_reg, 'C')
        
        return 'C'
    
    def generate_music_notation(self):
        """Generate human-readable music notation"""
        notation = []
        
        for i in range(min(len(self.musical_data['notes']), 20)):  # First 20 notes
            note = self.musical_data['notes'][i]
            rhythm = self.musical_data['rhythms'][i]
            instrument = self.musical_data['instruments'][i]
            
            duration_name = {
                0.125: '8th',
                0.25: 'quarter', 
                0.375: 'dotted quarter',
                0.5: 'half'
            }.get(rhythm, 'quarter')
            
            notation.append(f"{note} ({duration_name}) - {instrument}")
        
        return notation
    
    def save_musical_data(self, output_file='musical_data.json'):
        """Save converted musical data to JSON file"""
        # Add metadata
        self.musical_data['metadata'] = {
            'source_trace': self.trace_file,
            'total_instructions': len(self.trace_data['instructions']) if self.trace_data else 0,
            'conversion_version': '1.0'
        }
        
        with open(output_file, 'w') as f:
            json.dump(self.musical_data, f, indent=2)
        
        print(f"Musical data saved to {output_file}")
    
    def print_summary(self):
        """Print summary of the musical conversion"""
        print("\n=== CPU Trace to Music Conversion Summary ===")
        print(f"Tempo: {self.musical_data['tempo']} BPM")
        print(f"Key: {self.musical_data['key']} major")
        print(f"Total notes: {len(self.musical_data['notes'])}")
        
        # Instrument usage
        instrument_count = defaultdict(int)
        for inst in self.musical_data['instruments']:
            instrument_count[inst] += 1
        
        print("\nInstrument usage:")
        for instrument, count in sorted(instrument_count.items()):
            percentage = (count / len(self.musical_data['instruments'])) * 100
            print(f"  {instrument}: {count} notes ({percentage:.1f}%)")
        
        print("\nFirst 10 notes:")
        notation = self.generate_music_notation()
        for i, note_desc in enumerate(notation[:10]):
            print(f"  {i+1:2d}. {note_desc}")

def main():
    print("=== CPU Trace to Music Converter ===")
    
    converter = CPUTraceToMusic()
    
    # Load trace data
    if not converter.load_trace():
        return
    
    # Convert to musical data
    print("Converting CPU instructions to musical data...")
    converter.analyze_instructions()
    
    # Save results
    converter.save_musical_data()
    
    # Show summary
    converter.print_summary()
    
    print("\n=== Conversion Complete ===")
    print("Files created:")
    print("- musical_data.json (JSON musical data)")
    print("\nYou can now use this musical data to generate actual audio!")

if __name__ == "__main__":
    main()