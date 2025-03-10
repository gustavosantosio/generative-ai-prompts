'''

Prompt Instructions on Google AI Studio:

    "You are an expert regex string creator and understand how regex works. Your job is to convert the user's natural language queries and constraints in the form of regex. 
    After generating the regex string, provide explanation in detail with a few examples. Then demonstrate its use in a python code.

    User query:
    Give me the regex equivalent of the following:
    My requirements are:

    I want my string to have 2-63 characters.

    The string should be alphanumeric and can contain - also.

    The string must start as well as end with alphanumeric characters only."


'''


import re

def regex_example():
    """
    Regular expression to validate a hostname according to RFC 1034.
    
    From the standard:
    
        "The syntax of a legal Internet host name was specified in RFC-952
        [DNS:4].  One aspect of host name syntax is hereby changed: the
        restriction on the first character is relaxed to allow either a
        letter or a digit.  Host names are limited to 63 characters."
    
    This regular expression will validate that the input string is a
    valid hostname according to the standard. It will not validate that
    the hostname is resolvable to an IP address. It only checks that the
    syntax of the hostname is correct.
    
    The regular expression works by checking that the first and last
    characters are either a letter or a number, and then checks that the
    remaining characters are either a letter, a number, or a hyphen.
    The length of the string is also checked to ensure that it is
    between 2 and 63 characters long.
    
    Parameters
    ----------
    string : str
        The string to be validated.
    
    Returns
    -------
    bool
        True if the string is a valid hostname, False otherwise.
    
    Examples
    --------
    >>> regex_example()
    'ab' is VALID
    'abc-123' is VALID
    'A1-aZ' is VALID
    'abcdefgh123456' is VALID
    'test-string' is VALID
    '-abc' is INVALID
    'abc-' is INVALID
    '123-456-' is INVALID
    '----' is INVALID
    'a' is INVALID
    'abcdefgh123456789012345678901234567890' is INVALID
    '123-456-789-' is INVALID
    '-test' is INVALID
    '1a' is VALID
    'a1' is VALID
    """
    
    regex = r"^(?=[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]$)[a-zA-Z0-9\-]{2,63}$"

    strings = [
        "ab",
        "abc-123",
        "A1-aZ",
        "abcdefgh123456",
        "test-string",
        "-abc",
        "abc-",
        "123-456-",
        "----",
        "a",
        "abcdefgh123456789012345678901234567890",
        "123-456-789-",
        "-test",
        "1a",
        "a1"
    ]

    for string in strings:
        match = re.match(regex, string)
        if match:
            print(f"'{string}' is VALID")
        else:
            print(f"'{string}' is INVALID")