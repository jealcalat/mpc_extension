import re
import argparse

def correct_semicolon_newline(source_code):
    corrected_code = []
    lines = source_code.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        
        # Ignore comments that start with backslash
        if stripped_line.startswith("\\"):
            corrected_code.append(line)
            continue
        
        # If line ends with semicolon, replace it with a newline
        if stripped_line.endswith(";"):
            corrected_code.append(stripped_line[:-1])  # Remove the semicolon
            corrected_code.append('')  # Add a newline
        else:
            corrected_code.append(line)
    
    return '\n'.join(corrected_code)
  
def indent_between_patterns(source_code, indent_size=4):
    # Define the patterns.
    state_set_pattern = re.compile(r'(?i)\bs\.s\.[1-9]\b|\bs\.s\.[1-9][0-9]\b')
    state_pattern = re.compile(r'(?i)\bs[1-9]\b|\bs[1-9][0-9]\b|\bs20\b')

    lines = source_code.split('\n')
    indent_level = 0  # Keep track of current indentation level

    indented_code = []

    for line in lines:
        stripped_line = line.strip()

        if state_set_pattern.match(stripped_line):  # If it's a state set
            indented_code.append(' ' * indent_level + stripped_line)
            indent_level += 4  # Increase the indentation for next lines
        elif state_pattern.match(stripped_line):  # If it's a state
            indented_code.append(' ' * indent_level + stripped_line)
            indent_level += 4  # Increase the indentation for next line only
        else:
            indented_code.append(' ' * indent_level + stripped_line)
            if indent_level > 0:  # If the line is indented because of a state, reset indent
                indent_level -= 4

    return '\n'.join(indented_code)

def align_at_symbol(source_code, indent_size=4):
  lines = source_code.split('\n')
  new_lines = []

  for idx, line in enumerate(lines):
      stripped_line = line.lstrip()

      # If the line starts with @ and there's a previous line
      if stripped_line.startswith('@') and idx > 0:
          # Calculate the whitespace (indent) of the previous line
          prev_line_indent = len(lines[idx - 1]) - len(lines[idx - 1].lstrip())
          # Add additional indent for clarity
          total_indent = prev_line_indent + indent_size
          
          # Append the modified line
          new_lines.append(' ' * total_indent + stripped_line)
      else:
          new_lines.append(line)

  return '\n'.join(new_lines)


def lint_and_correct(source_code):
    # Check for and correct semicolon violations
    corrected_code = correct_semicolon_newline(source_code)
    # ... Add other correction functions here as needed ...
    return corrected_code

def main():
    parser = argparse.ArgumentParser(description="Linter for my language")
    parser.add_argument("file", help="Source file to lint")

    args = parser.parse_args()

    with open(args.file, "r") as f:
        source_code = f.read()

    corrected_code = lint_and_correct(source_code)
    corrected_code = indent_between_patterns(corrected_code)
    corrected_code = align_at_symbol(corrected_code)
    # Optionally, write corrected code back to file
    with open('correct.MPC', 'w') as file:
        file.write(corrected_code)
if __name__ == "__main__":
    main()
