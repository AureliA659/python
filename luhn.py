import random

def luhn_generate():
    """
    Generate a valid card number using the Luhn algorithm.
    :return: str, a valid card number
    """
    # Start with a random 15-digit base (excluding the check digit)
    base_number = [random.randint(0, 9) for _ in range(15)]

    # Reverse the base number for Luhn processing
    reversed_digits = base_number[::-1]

    # Apply Luhn algorithm to calculate the check digit
    for i in range(0, len(reversed_digits), 2):
        doubled = reversed_digits[i] * 2
        reversed_digits[i] = doubled - 9 if doubled > 9 else doubled

    # Sum all the digits and calculate the check digit
    total_sum = sum(reversed_digits)
    check_digit = (10 - (total_sum % 10)) % 10

    # Append the check digit to the base number
    base_number.append(check_digit)

    # Return the generated card number as a string
    return ''.join(map(str, base_number))

def luhn_check(card_number):
    """
    Validate a card number using the Luhn algorithm.
    :param card_number: str, the card number as a string of digits
    :return: bool, True if valid, False otherwise
    """
    # Remove any non-digit characters (e.g., spaces or dashes)
    card_number = ''.join(filter(str.isdigit, card_number))

    # Reverse the card number and process it
    reversed_digits = [int(digit) for digit in card_number[::-1]]
    
    # Double every second digit from the right and adjust if greater than 9
    for i in range(1, len(reversed_digits), 2):
        doubled = reversed_digits[i] * 2
        reversed_digits[i] = doubled - 9 if doubled > 9 else doubled

    # Sum all the digits
    total_sum = sum(reversed_digits)

    # The card number is valid if the total sum is a multiple of 10
    return total_sum % 10 == 0

# Example usage
if __name__ == "__main__":
    print("Luhn Algorithm Example")
    generated_number = 0
    answer = ''
    while answer.lower() != 'y' or answer.lower() != 'n' or answer.lower() != 'q':
        answer = input("Do you want to verify your number? (y/n), (q) to quit: ")
        if answer.lower() == 'y':
            numb_to_check = input("Enter the number to verify: ")
            if luhn_check(numb_to_check):
                print(f"The card number {numb_to_check} is VALID.")
            else:
                print(f"The card number {numb_to_check} is INVALID.")
        elif answer.lower() == 'n':
            numb_to_check = generated_number
            # Generate a valid card number
            generated_number = luhn_generate()
            print(f"Generated card number: {generated_number}")
            # Validate the generated number
            if luhn_check(generated_number):
                print(f"The card number {generated_number} is VALID.")
            else:
                print(f"The card number {generated_number} is INVALID.")
        elif answer.lower() == 'q':
            break
    
    

    