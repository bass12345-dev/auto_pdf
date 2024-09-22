
import re
def capitalize_first_and_after_spaces(text):
    # Capitalize the first letter of the string
    text = text.capitalize()
    
    # Split the string into words
    words = text.split(' ')
    
    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]
    
    # Join the words back into a single string with spaces
    result = ' '.join(capitalized_words)
    
    return result


