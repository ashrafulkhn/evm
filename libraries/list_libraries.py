
import pkg_resources

def list_installed_libraries(file_name="libraries.txt"):
    try:
        # Get a list of all installed packages
        installed_packages = pkg_resources.working_set

        # Open the file in write mode
        with open(file_name, "w") as file:
            # Write the libraries and their versions to the file
            for package in sorted(installed_packages, key=lambda x: x.project_name.lower()):
                file.write(f"{package.project_name}=={package.version}\n")
        
        print(f"Library list saved to '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_installed_libraries()
