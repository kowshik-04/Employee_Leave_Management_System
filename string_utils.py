"""
String utility functions for text manipulation
"""

def reverse_string(text):
    """Reverse a string"""
    return text[::-1]

def is_palindrome(text):
    """Check if a string is a palindrome"""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def count_vowels(text):
    """Count the number of vowels in a string"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)

def capitalize_words(text):
    """Capitalize the first letter of each word"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_whitespace(text):
    """Remove all whitespace from a string"""
    return ''.join(text.split())

def count_words(text):
    """Count the number of words in a string"""
    return len(text.split())

def is_anagram(str1, str2):
    """Check if two strings are anagrams"""
    return sorted(str1.lower().replace(" ", "")) == sorted(str2.lower().replace(" ", ""))

def truncate(text, length, suffix="..."):
    """Truncate a string to specified length"""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix

def repeat_string(text, count):
    """Repeat a string n times"""
    return text * count

def starts_with_vowel(text):
    """Check if string starts with a vowel"""
    if not text:
        return False
    return text[0].lower() in "aeiou"

def extract_numbers(text):
    """Extract all numbers from a string"""
    return ''.join(char for char in text if char.isdigit())

if __name__ == "__main__":
    print("String Utilities Test")
    print(f"Reverse 'hello': {reverse_string('hello')}")
    print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
    print(f"Vowels in 'hello world': {count_vowels('hello world')}")
    print(f"Capitalize 'hello world': {capitalize_words('hello world')}")
    print(f"Remove whitespace 'hello world': {remove_whitespace('hello world')}")
    print(f"Word count 'hello world': {count_words('hello world')}")
    print(f"'listen' and 'silent' are anagrams: {is_anagram('listen', 'silent')}")
    print(f"Truncate 'hello world' to 5: {truncate('hello world', 5)}")
    print(f"Repeat 'abc' 3 times: {repeat_string('abc', 3)}")
    print(f"'apple' starts with vowel: {starts_with_vowel('apple')}")
    print(f"Extract numbers from 'abc123xyz456': {extract_numbers('abc123xyz456')}")
