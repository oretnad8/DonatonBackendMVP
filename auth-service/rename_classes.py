import os
import re
import glob

def get_new_name(old_name):
    # Split by camel case
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', old_name).split()
    # Reverse order of words, reverse each word, and capitalize
    reversed_words = [w[::-1].capitalize() for w in reversed(words)]
    return "".join(reversed_words)

class_names = [
    "AuthApplication", "SecurityConfig", "AuthController", "AuthResponse",
    "LoginRequest", "TokenValidationResponse", "ValidateTokenRequest",
    "Rol", "Usuario", "GlobalExceptionHandler", "UsuarioRepository",
    "JwtUtil", "AuthService"
]

mapping = {name: get_new_name(name) for name in class_names}
# Sort by length descending to replace longer words first
sorted_mapping = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)

base_dir = r"c:\Users\Dante\Desktop\5to\evsoftware\ev3\MVP\donaton\auth-service"
java_files = glob.glob(os.path.join(base_dir, "**", "*.java"), recursive=True)

print("Mapping de clases:")
for old, new in sorted_mapping:
    print(f"{old} -> {new}")

for file_path in java_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old_name, new_name in sorted_mapping:
        new_content = re.sub(r'\b' + old_name + r'\b', new_name, new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Update pom.xml just in case the main class is referenced
pom_path = os.path.join(base_dir, "pom.xml")
if os.path.exists(pom_path):
    with open(pom_path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content
    for old_name, new_name in sorted_mapping:
        new_content = re.sub(r'\b' + old_name + r'\b', new_name, new_content)
    if new_content != content:
        with open(pom_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Now rename the files
for file_path in java_files:
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    old_class = file_name.replace(".java", "")
    if old_class in mapping:
        new_class = mapping[old_class]
        new_file_path = os.path.join(dir_name, new_class + ".java")
        os.rename(file_path, new_file_path)
        print(f"Renamed {file_name} to {new_class}.java")

print("Done.")
