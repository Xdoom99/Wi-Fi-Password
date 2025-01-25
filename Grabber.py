import subprocess
import re
import csv
from tabulate import tabulate

def get_wifi_profiles():
    try:
        command = ["netsh", "wlan", "show", "profiles"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", result.stdout)
        return profiles
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve WiFi profiles:", e)
        return []

def get_wifi_password(profile):
    try:
        command = ["netsh", "wlan", "show", "profile", profile, "key=clear"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        password_match = re.search(r"Key Content\s*:\s*(.*)", result.stdout)
        return password_match.group(1) if password_match else "No password stored"
    except subprocess.CalledProcessError:
        return "Error retrieving password"

def display_profiles_and_passwords(profiles):
    table = []
    for profile in profiles:
        password = get_wifi_password(profile)
        table.append({"Profile": profile, "Password": password})
    print(tabulate(table, headers="keys", tablefmt="grid"))

def export_to_csv(profiles):
    filename = "wifi_profiles.csv"
    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Profile", "Password"])
            writer.writeheader()
            for profile in profiles:
                password = get_wifi_password(profile)
                writer.writerow({"Profile": profile, "Password": password})
        print(f"Exported profiles to {filename}")
    except Exception as e:
        print("Failed to export profiles to CSV:", e)

def main():
    print("Fetching WiFi profiles and passwords...\n")
    profiles = get_wifi_profiles()
    if not profiles:
        print("No WiFi profiles found.")
        return

    while True:
        print("\nOptions:")
        print("1. Display profiles and passwords")
        print("2. Export profiles and passwords to CSV")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_profiles_and_passwords(profiles)
        elif choice == "2":
            export_to_csv(profiles)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
