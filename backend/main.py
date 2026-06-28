from src.input_processor import process_input
from src.inference import run_inference
from src.output_formatter import format_output

def main():
    user_input = input("Enter input: ")

    processed = process_input(user_input)
    result = run_inference(processed)
    output = format_output(result)

    print(output)

if __name__ == "__main__":
    main()