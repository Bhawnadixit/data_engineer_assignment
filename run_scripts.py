import subprocess

# Define the list of scripts you want to run
scripts = [
    "data_API.py",
    "map_schema.py",
    "extract_diseases.py"
]

# Run each script
for script in scripts:
    try:
        print(f"Running {script}...")
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        print(f"Output of {script}: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e.stderr}")
    print("="*40)
