import argparse

from dotenv import load_dotenv

from src.pipeline import run


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Math textbook → competency hierarchy Excel")
    parser.add_argument("--input", required=True, help="Path to PDF or text file")
    parser.add_argument("--topic", required=True, help="Topic name (e.g. 'Slope of Lines')")
    parser.add_argument("--out", required=True, help="Output .xlsx path")
    args = parser.parse_args()

    run(args.input, args.topic, args.out)


if __name__ == "__main__":
    main()
