#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <text_file> <word_list_file>"
    exit 1
fi

# Input files
text_file="$1"
word_list_file="$2"

# Output file
output_file="word_frequencies.csv"

# Process word list file and create an associative array
declare -A word_map_cl_word
declare -A word_map_spel_var
while IFS=, read -r cl_word spel_var category; do
    word_map_cl_word["$cl_word"]=0
    word_map_spel_var["$spel_var"]=0
done < <(tail -n +2 "$word_list_file")  # Skip the header line

# Process text file and update word frequencies
while IFS= read -r line; do
    for word in $line; do
        word=${word,,}  # Convert to lowercase for case-insensitive comparison
        if [ -n "${word_map_cl_word[$word]}" ]; then
            ((word_map_cl_word["$word"]++))
        fi
        if [ -n "${word_map_spel_var[$word]}" ]; then
            ((word_map_spel_var["$word"]++))
        fi
    done
done < "$text_file"

# Output word frequencies to the same file
echo "cl_word,spel_var,Category,frequency_cl_word,frequency_spel_var" > "$output_file"
while IFS=, read -r cl_word spel_var category; do
    echo "$cl_word,$spel_var,$category,${word_map_cl_word[$cl_word]},${word_map_spel_var[$spel_var]}" >> "$output_file"
done < <(tail -n +2 "$word_list_file")  # Skip the header line

echo "Word frequencies have been saved to $output_file"
