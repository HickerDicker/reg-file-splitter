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

original_file_path = input("Enter the path of the original .reg file: ")

if not os.path.isfile(original_file_path):
    print("Error: Invalid file path.")
    exit()

script_directory = os.path.dirname(os.path.abspath(__file__)) if __file__ != '' else os.getcwd()

hives = {'HKCR': [], 'HKCU': [], 'HKLM': [], 'HKCC': []}

with open(original_file_path, 'r') as f:
    current_hive = None
    for line in f:
        line = line.strip()
        if line:
            hive = extract_hive(line)
            if hive:
                current_hive = hive
            if current_hive:
                if line.startswith(';'):
                    hives[current_hive][-1] += "\n" + line
                else:
                    if line.startswith('['):
                        hives[current_hive].append('\n' + line)
                    else:
                        if not line.startswith("Windows Registry Editor Version 5.00") and not hives[current_hive][-1].endswith(';'):
                            line = "\n" + line
                        hives[current_hive][-1] += line
                        
for hive, content in hives.items():
    output_file_path = os.path.join(script_directory, f'{hive}.reg')
    with open(output_file_path, 'w') as f:
        f.write("Windows Registry Editor Version 5.00\n")
        for line in content:
            f.write(line + '\n')

print("Splitting complete.")
