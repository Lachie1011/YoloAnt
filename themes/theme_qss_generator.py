import os
import yaml

# Base directories
UI_DIR = '../ui'
THEMES_DIR = 'definitions'
OUTPUT_QSS_DIR = 'generated'

def generate_theme_qss(theme_filename: str, theme_data: dict):
    # Extract theme name and colour mapping
    theme_name = theme_data.get('name', os.path.splitext(theme_filename)[0])
    colour_map = theme_data.get('colours', {})

    final_qss = ""

    # Walk through all subdirectories and find .qss files
    for root, _, files in os.walk(UI_DIR):
        for file in files:
            if file.endswith(".qss"):
                qss_path = os.path.join(root, file)

                print(f"Found QSS: {qss_path}")
                with open(qss_path, 'r') as f:
                    qss_data = f.read()

                    # Replace theme placeholders like @app_background, @font_header, etc.
                    for key, value in colour_map.items():
                        qss_data = qss_data.replace(f'@{key}', str(value))

                    module_name = os.path.basename(root).capitalize()
                    final_qss += f"/* === {module_name} ({file}) === */\n{qss_data}\n\n"

    if not final_qss:
        print("No QSS files were found or matched.")
        return

    os.makedirs(OUTPUT_QSS_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_QSS_DIR, f'{theme_name.lower().replace(" ", "_")}.qss')
    with open(output_path, 'w') as f:
        f.write(final_qss)

    print(f"Generated theme: {theme_name}.qss → {output_path}")


def main():
    for theme_file in os.listdir(THEMES_DIR):
        if theme_file.endswith('.yaml'):
            theme_path = os.path.join(THEMES_DIR, theme_file)
            with open(theme_path, 'r') as f:
                theme_data = yaml.safe_load(f)
                print(f"\nGenerating theme for '{theme_file}'...")
                generate_theme_qss(theme_file, theme_data)

if __name__ == "__main__":
    main()
