import random
import hashlib

def get_random_words(filename, num_words):
    """Get a list of random words from a file

    Args:
        filename (str): The name of the file to read the words from
        num_words (int): The number of words to get from the file

    Returns:
        list: A list of random words from the file
    """
    with open(filename) as f:
        words = f.read().splitlines()
    return random.sample(words, num_words)

def hash_password(password):
    """Hash a password using SHA-256

    Args:
        password (str): The password to hash

    Returns:
        str: The hexadecimal representation of the password hash
    """
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    """Generate and hash random passwords

    The main function generates 4 random passwords by concatenating 4 random words from a file, 
    each word's first 4 characters and a random number between 0 and 9. It also randomly capitalizes 
    a letter in each password. The password and its hash are then printed.
    """
    filename = "password.txt"
    num_words = 4
    num_results = 4
    for i in range(num_results):
        words = get_random_words(filename, num_words)
        password = "".join([word[:4] + str(random.randint(0,9)) for word in words])
        password_list = list(password)
        password_list[random.randint(0, len(password_list) - 1)] = password_list[random.randint(0, len(password_list) - 1)].upper()
        password = "".join(password_list)
        hashed_password = hash_password(password)
        result = {"created_word": password, "password_hash": hashed_password}
        print(result)

if __name__ == "__main__":
    main()
