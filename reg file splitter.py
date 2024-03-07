import os

def extract_hive(line):
    if line.startswith('[HKEY_CURRENT_USER'):
        return 'HKCU'
    elif line.startswith('[HKEY_LOCAL_MACHINE'):
        return 'HKLM'
    elif line.startswith('[HKEY_CLASSES_ROOT'):
        return 'HKCR'
    elif line.startswith('[HKEY_CURRENT_CONFIG'):
        return 'HKCC'
    return None

def handle_continuation_lines(lines):
    # Combine continuation lines into a single line
    combined_lines = []
    continuation = False
    for line in lines:
        if continuation:
            combined_lines[-1] += line.strip()
            continuation = line.endswith('\\')
        else:
            combined_lines.append(line.strip())
            continuation = line.endswith('\\')
    return combined_lines

original_file_path = input("Enter the path of the original .reg file: ")

if not os.path.isfile(original_file_path):
    print("Error: Invalid file path.")
    exit()

script_directory = os.path.dirname(os.path.abspath(__file__)) if __file__ != '' else os.getcwd()

hives = {'HKCR': [], 'HKCU': [], 'HKLM': [], 'HKCC': []}

with open(original_file_path, 'r') as f:
    current_hive = None
    lines = []
    for line in f:
        line = line.strip()
        if line:
            if line.startswith(';'):
                continue  # Skip comments
            hive = extract_hive(line)
            if hive:
                current_hive = hive
            if current_hive:
                lines.append(line)
    combined_lines = handle_continuation_lines(lines)
    for line in combined_lines:
        hive = extract_hive(line)
        if hive:
            current_hive = hive
        if current_hive:
            hives[current_hive].append(line)

for hive, content in hives.items():
    output_file_path = os.path.join(script_directory, f'{hive}.reg')
    with open(output_file_path, 'w') as f:
        f.write("Windows Registry Editor Version 5.00\n\n")
        for line in content:
            f.write(line + '\n')

print("Splitting complete.")
