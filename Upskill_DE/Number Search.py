def number_search(text: str) -> int:
    digit_sum = 0
    letter_sum = 0

    for char in text:
        if char.isdigit():
            digit_sum += int(char)
        elif char.isalpha():
            letter_sum += 1
    result = digit_sum / letter_sum
    return round(result)

text = input()
print(number_search(text))
