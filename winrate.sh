
#!/bin/bash

# Check if a file is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <result_file>"
    exit 1
fi

# Assign the input file to a variable
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

# Extract bot names and optional strengths using pattern matching
filename=$(basename "$input_file")
if [[ "$filename" =~ ^([a-zA-Z]+)([0-9]*)_vs_([a-zA-Z]+)([0-9]*)\.txt$ ]]; then
    black_bot="${BASH_REMATCH[1]}"
    black_strength="${BASH_REMATCH[2]}"
    white_bot="${BASH_REMATCH[3]}"
    white_strength="${BASH_REMATCH[4]}"
else
    echo "Error: Filename format is incorrect. Expected format: (black_bot)(optional_strength)_vs_(white_bot)(optional_strength).txt"
    exit 1
fi

# Set default values if strengths are missing
black_strength=${black_strength:-"N/A"}
white_strength=${white_strength:-"N/A"}

# Count wins for black and white
black_wins=$(grep -c "black win" "$input_file")
white_wins=$(grep -c "white win" "$input_file")
ties=$(grep -c "tie" "$input_file")
total_games=$((black_wins + white_wins + ties))

# Check if there are any games to avoid division by zero
if [ $total_games -eq 0 ]; then
    echo "No games found in the file."
    exit 1
fi

# Calculate win rates
black_winrate=$(echo "scale=2; $black_wins / $total_games * 100" | bc)
white_winrate=$(echo "scale=2; $white_wins / $total_games * 100" | bc)

# Display results with bot names and strengths
echo "Results for black:$black_bot (Strength: ${black_strength}) vs white:$white_bot (Strength: ${white_strength}) in a pool of $total_games games:"
echo "Black Win Rate: $black_winrate%"
echo "White Win Rate: $white_winrate%"

