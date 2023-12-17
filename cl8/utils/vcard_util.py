import itertools
import unicodedata
import vobject


def _is_all_latin_characters(string: str) -> bool:
    """
    Returns True if every character in the string meets the following criteria:

    - It's in the [Basic Latin][1] or [Latin-1 Supplement][2] Unicode block
      (U+0000 to U+00FF).
    - It's a hyphen or [categorized][3] as a Unicode Letter.

    Returns False otherwise.

    [1]: https://www.unicode.org/charts/PDF/U0000.pdf
    [2]: https://www.unicode.org/charts/PDF/U0080.pdf
    [3]: https://www.unicode.org/reports/tr44/#General_Category_Values
    """
    for character in string:
        if character == "-":
            continue

        # Characters < 0x41 are in the Basic Latin block,
        # but 0x41 is the first letter.
        is_in_latin_block = 0x41 <= ord(character) <= 0xFF
        if not is_in_latin_block:
            return False

        is_in_valid_category = unicodedata.category(character).startswith("L")
        if not is_in_valid_category:
            return False

    return True


def full_name_to_name(full_name: str) -> vobject.vcard.Name:
    """
    Convert free-form full name strings (like "Alice McBiscuit") to structured
    vCard names.

    vCard has two relevant name fields:

    1. [FN], which is effectively a string
    2. [N], which breaks names into pieces: given name, surname, etc.

    We should always provide FN. Unfortunately, we also need to provide N
    because (1) some vCard parsers require it (2) our vCard library produces
    vCard version 3 files where [N is required][0].

    Because we don't store these structured fields, we use a simple heuristic
    to build structure from free-form name strings.

    If this function receives a two-word name made up of Latin characters, it
    will break it into given + family name. Otherwise, it will "give up" and
    put everything into the given name. See the tests for examples, as well as
    some edge cases not documented here.

    This heuristic could be made more sophisticated but should work well enough
    given that many contact apps prefer FN and use N as a fallback.

    [FN]: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.1
    [N]: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2
    [0]: https://www.rfc-editor.org/rfc/rfc2426#section-3.1.2
    """

    give_up_result = vobject.vcard.Name(given=full_name)

    if len(full_name) >= 1024:
        return give_up_result

    words = full_name.split()

    if len(words) != 2:
        return give_up_result

    if not all(_is_all_latin_characters(word) for word in words):
        return give_up_result

    return vobject.vcard.Name(given=words[0], family=words[1])


def content_disposition_filename(full_name: str) -> str:
    """
    Generate the .vcf filename given a full name, suitable for use in the
    `Content-Disposition` header. Should be quoted.
    """

    fallback = "contact.vcf"

    if len(full_name) >= 256:
        return fallback

    if not full_name.isascii():
        return fallback

    full_name = full_name.replace(".", "").replace(",", "").strip()

    if len(full_name) == 0:
        return fallback

    for character in full_name:
        is_valid = character == "-" or character == " " or character.isalpha()
        if not is_valid:
            return fallback

    return f"{full_name}.vcf"
