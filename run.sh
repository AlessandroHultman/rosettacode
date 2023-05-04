#!/bin/bash

# Check if the task name argument is given
if [ -z "$1" ]; then
  # Print a message indicating the task name argument is missing
  echo "Please provide a task name as an argument"
  exit 1
fi

echo "Fetching source code..."
# Run the Python program that scrapes the source code from the website
python3 rccli.py --task "$1"

# Array of languages that can be generated as LLVM IR
llvm_langs=(C C++ Objective-C Swift D Rust Fortran Ada Haskell Kotlin Julia)

# Checks if a language can be generated as LLVM IR
can_generate_llvm() {
  # Get the language name from the file name
  lang=${1%.txt}
  # Loop through the array of languages
  for llvm_lang in "${llvm_langs[@]}"; do
    # Check if the language name matches the current element of the array
    if [[ "$lang" = "$llvm_lang" ]]; then
      # Return true if it matches
      return 0
    fi
  done
  # Return false otherwise
  return 1
}

# Function that returns the file extension for a language
get_file_extension() {
  # Get the language name as an argument
  lang=$1
  # Match the language name with the file extension
  case "$lang" in
    C)
      echo ".c"
      ;;
    C++)
      echo ".cpp"
      ;;
    Objective-C)
      echo ".m"
      ;;
    Swift)
      echo ".swift"
      ;;
    D)
      echo ".d"
      ;;
    Rust)
      echo ".rs"
      ;;
    Fortran)
      echo ".f90"
      ;;
    Ada)
      echo ".adb"
      ;;
    Haskell)
      echo ".hs"
      ;;
    Kotlin)
      echo ".kt"
      ;;
    Julia)
      echo ".jl"
      ;;
    *)
      # Return .txt for unknown languages
      echo ".txt"
      ;;
  esac
}

# Loop through all the files in the code directory
for file in "$1"/*.txt; do
  # Check if the file is a language that can generate LLVM IR
  if can_generate_llvm "$(basename "$file")"; then
    # Get the language name from the file name without the task_name/ prefix
    lang=${file#"$1"/}
    lang=${lang%.txt}
    # Get the file extension for the language
    ext=$(get_file_extension "$lang")
    # Create a new file with the correct extension in the same directory with the task_name/ prefix
    new_file=""$1"/$lang$ext"
    cp "$file" "$new_file"
    # Remove the old file with .txt extension
    rm "$file"
  else
    rm "$file"
  fi
done

echo "Files successfully written to $PWD/$1"