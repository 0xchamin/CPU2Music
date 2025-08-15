#!/usr/bin/env python3
"""
GDB CPU Instruction Tracer for Name Processing
This script captures actual CPU instructions during name processing
"""

import gdb
import json
import time
import re

class NameInstructionTracer(gdb.Command):
    """Custom GDB command to trace CPU instructions during name processing"""
    
    def __init__(self):
        super().__init__("trace-name", gdb.COMMAND_USER)
        self.instructions = []
        self.registers = []
        self.memory_accesses = []
        
    def invoke(self, arg, from_tty):
        """Main tracing function"""
        print(f"Starting instruction trace for name processing...")
        
        # Set up logging
        gdb.execute("set logging overwrite on")
        gdb.execute("set logging file instruction_trace.log")
        gdb.execute("set logging on")
        
        # Find the name processing function
        try:
            # Set breakpoint at main or name processing function
            gdb.execute("break process_name")
            print("Breakpoint set at process_name function")
        except:
            print("Setting breakpoint at main")
            gdb.execute("break main")
        
        # Run the program
        gdb.execute("run")
        
        # Start instruction-by-instruction tracing
        self.trace_instructions()
        
        # Save results to JSON
        self.save_trace_data()
        
        print(f"Trace complete! Captured {len(self.instructions)} instructions")
    
    def trace_instructions(self):
        """Step through instructions and collect data"""
        instruction_count = 0
        max_instructions = 1000  # Limit to prevent infinite loops
        
        try:
            while instruction_count < max_instructions:
                # Get current instruction
                try:
                    frame = gdb.selected_frame()
                    pc = int(frame.pc())
                    
                    # Get disassembly of current instruction
                    disasm_output = gdb.execute(f"x/i 0x{pc:x}", to_string=True)
                    instruction = self.parse_instruction(disasm_output, pc)
                    
                    # Get register states
                    registers = self.get_register_state()
                    
                    # Get memory access info if available
                    memory_info = self.get_memory_info(instruction)
                    
                    # Store the data
                    trace_entry = {
                        'step': instruction_count,
                        'pc': f"0x{pc:x}",
                        'instruction': instruction,
                        'registers': registers,
                        'memory': memory_info,
                        'timestamp': time.time()
                    }
                    
                    self.instructions.append(trace_entry)
                    
                    print(f"Step {instruction_count}: 0x{pc:x} - {instruction}")
                    
                    # Execute single instruction
                    gdb.execute("stepi")
                    instruction_count += 1
                    
                except gdb.error as e:
                    print(f"GDB Error: {e}")
                    break
                except Exception as e:
                    print(f"Error during tracing: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\nTracing interrupted by user")
    
    def parse_instruction(self, disasm_output, pc):
        """Parse GDB disassembly output"""
        # Example: "0x555555555149 <main+4>:\tmov    %rdi,-0x18(%rbp)"
        try:
            lines = disasm_output.strip().split('\n')
            for line in lines:
                if f"0x{pc:x}" in line:
                    # Extract instruction part after the tab
                    parts = line.split('\t')
                    if len(parts) > 1:
                        return parts[1].strip()
        except:
            pass
        return "unknown"
    
    def get_register_state(self):
        """Capture current CPU register values"""
        registers = {}
        reg_names = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp', 'rip']
        
        for reg in reg_names:
            try:
                output = gdb.execute(f"info registers {reg}", to_string=True)
                # Parse register value
                match = re.search(rf'{reg}\s+0x([0-9a-f]+)', output)
                if match:
                    registers[reg] = f"0x{match.group(1)}"
            except:
                registers[reg] = "unknown"
        
        return registers
    
    def get_memory_info(self, instruction):
        """Extract memory access information from instruction"""
        memory_info = {
            'read': None,
            'write': None,
            'address': None
        }
        
        # Look for memory operands like (%rax), 0x8(%rbp), etc.
        memory_pattern = r'[+-]?0x[0-9a-f]+\([^)]+\)|\([^)]+\)'
        matches = re.findall(memory_pattern, instruction)
        
        if matches:
            memory_info['address'] = matches[0]
            
            # Determine if it's a read or write
            if instruction.startswith('mov') and ',' in instruction:
                parts = instruction.split(',')
                if any(match in parts[1] for match in matches):
                    memory_info['write'] = True
                else:
                    memory_info['read'] = True
        
        return memory_info
    
    def save_trace_data(self):
        """Save collected trace data to JSON file"""
        trace_data = {
            'metadata': {
                'total_instructions': len(self.instructions),
                'timestamp': time.time(),
                'tracer_version': '1.0'
            },
            'instructions': self.instructions
        }
        
        with open('cpu_trace.json', 'w') as f:
            json.dump(trace_data, f, indent=2)
        
        print("Trace data saved to cpu_trace.json")

# Register the custom command
NameInstructionTracer()

print("GDB Name Instruction Tracer loaded!")
print("Usage: trace-name")
print("Make sure your program has a 'process_name' function or it will trace from main")