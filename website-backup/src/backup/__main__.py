import sys
from backup.main import initiate_backup

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backup [options]")
        sys.exit(1)

    option = sys.argv[1]

    if option == "backup":
        initiate_backup()
    else:
        print(f"Unknown option: {option}")
        sys.exit(1)

if __name__ == "__main__":
    main()