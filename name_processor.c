#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Function that processes the name - this will be traced
unsigned int process_name(const char* name) {
    printf("Processing name: %s\n", name);
    
    // Calculate a hash of the name (generates CPU instructions)
    unsigned int hash = 5381;
    int c;
    const char* str = name;
    
    // This loop will generate interesting CPU instructions
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    
    // Some additional operations to generate more instructions
    int length = strlen(name);
    unsigned int result = hash;
    
    // Character frequency analysis
    int char_counts[256] = {0};
    for (int i = 0; i < length; i++) {
        char_counts[(unsigned char)name[i]]++;
    }
    
    // Combine with character analysis
    for (int i = 0; i < 256; i++) {
        if (char_counts[i] > 0) {
            result = result ^ (char_counts[i] * i);
        }
    }
    
    printf("Name: %s, Length: %d, Hash: %u, Result: %u\n", 
           name, length, hash, result);
    
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <name>\n", argv[0]);
        printf("Example: %s \"John\"\n", argv[0]);
        return 1;
    }
    
    const char* name = argv[1];
    
    printf("=== CPU Instruction Tracing for Name Processing ===\n");
    printf("Name to process: %s\n", name);
    printf("Starting processing...\n");
    
    unsigned int result = process_name(name);
    
    printf("Processing complete. Result: %u\n", result);
    
    return 0;
}