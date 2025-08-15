#!/bin/bash

# Automated CPU Instruction Tracing Script for Name Processing

echo "=== CPU Instruction Tracer for Name Processing ==="
echo

# Check if name argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <name>"
    echo "Example: $0 \"John\""
    exit 1
fi

NAME="$1"
echo "Name to trace: $NAME"

# Compile the name processor with debug symbols
echo "Compiling name processor..."
gcc -g -O0 -o name_processor name_processor.c
if [ $? -ne 0 ]; then
    echo "Error: Failed to compile name_processor.c"
    exit 1
fi

echo "Compilation successful!"

# Create GDB batch script
cat > gdb_script.txt << EOF
# Load the Python tracer
source gdb_tracer.py

# Set the program arguments
set args "$NAME"

# Start tracing
trace-name

# Quit GDB
quit
EOF

echo "Starting GDB tracing session..."
echo "This will capture actual CPU instructions during name processing..."

# Run GDB with the tracer
gdb -batch -x gdb_script.txt ./name_processor

# Check if trace file was created
if [ -f "cpu_trace.json" ]; then
    echo
    echo "=== Trace Complete ==="
    echo "CPU instruction trace saved to: cpu_trace.json"
    echo "Instruction log saved to: instruction_trace.log"
    
    # Show summary
    echo
    echo "=== Trace Summary ==="
    INSTRUCTION_COUNT=$(grep -c '"step":' cpu_trace.json)
    echo "Total instructions captured: $INSTRUCTION_COUNT"
    
    echo
    echo "=== Sample Instructions ==="
    head -20 instruction_trace.log
    
    echo
    echo "=== First Few Traced Instructions (JSON) ==="
    head -50 cpu_trace.json
    
else
    echo "Error: Trace file not created. Check for errors above."
    exit 1
fi

echo
echo "=== Files Created ==="
echo "- name_processor (executable)"
echo "- cpu_trace.json (JSON trace data)"
echo "- instruction_trace.log (raw instruction log)"
echo "- gdb_script.txt (GDB commands used)"

echo
echo "You can now use cpu_trace.json to generate music from the actual CPU instructions!"