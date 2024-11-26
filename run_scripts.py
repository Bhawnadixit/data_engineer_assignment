# Import the functions from the 'assignment' package
from extract_disease import main1, main2, main3

def main():
    print("Starting sequence of main functions...")
    main1()  # Call module1's main to download data via API
    main2()  # Call module2's main to map data to target schema
    main3()  # Call module3's main to extract diseases from inclusion criteria
    print("All main functions executed.")

if __name__ == "__main__":
    main()