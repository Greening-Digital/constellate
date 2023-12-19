import pytest
from vobject.vcard import Name

from .. import vcard_util


class TestVcardUtil:
    def test_full_name_to_name(self):
        """
        Check that we can convert free-form full name strings to structured
        vCard names.
        """
        all_in_given_name = [
            "",
            "Biscuit",
            "Dr.",
            "Dr. Gravy Biscuit",
            "Sweet Gravy Biscuit",
            "Ms. Dr. Cheese Gravy Biscuit Jr. M.D.",
            "Biscuit Jr.",
            "宮本 茂",
            "أبو بکر محمد بن زکریاء الرازي",
        ]
        for full_name in all_in_given_name:
            actual = vcard_util.full_name_to_name(full_name)
            expected = Name(given=full_name)
            assert actual == expected

        split = [
            ("Gravy", "Biscuit"),
            ("Großer", "Keks"),
        ]
        for given, family in split:
            full_name = f"{given} {family}"
            actual = vcard_util.full_name_to_name(full_name)
            expected = Name(given=given, family=family)
            assert actual == expected

    def test_content_disposition_filename(self):
        """
        Check that we can turn profile names into .vcf filenames.
        """
        use_fallback = [
            "",
            "  ",
            "a" * 256,
            "A\nB",
            "ÀBC",
            "A%B",
            "A\\B",
            "A\tB",
            "A$B",
            "AB123",
        ]
        for full_name in use_fallback:
            actual = vcard_util.content_disposition_filename(full_name)
            expected = "contact.vcf"
            assert actual == expected

        ok_to_serialize = [
            "Biscuit",
            "Gravy Biscuit",
            "Big Gravy Biscuit",
            "Gravy-Biscuit",
        ]
        for full_name in ok_to_serialize:
            actual = vcard_util.content_disposition_filename(full_name)
            expected = f"{full_name}.vcf"
            assert actual == expected

        filtered_actual = vcard_util.content_disposition_filename(
            "Dr. Gravy Biscuit, Jr."
        )
        filtered_expected = "Dr Gravy Biscuit Jr"
        assert actual == expected
