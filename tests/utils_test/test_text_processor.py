import pytest

from pyagentai.utils.text_processor import sanitize_text


@pytest.mark.parametrize(
    ("input_text", "expected_output"),
    [
        ("valid_filename", "valid_filename"),
        ("file name with spaces", "file name with spaces"),
        ("file-name-with-dashes", "file-name-with-dashes"),
        ("file_name_with_underscores", "file_name_with_underscores"),
        ("filename.with.dots", "filename.with.dots"),
        ("  leading and trailing spaces  ", "leading and trailing spaces"),
        ("invalid$cha@racters!", "invalid_cha_racters_"),
        ("", ""),
        ("a!b@c#d$e%f^g&h*i(j)k_l-m.n o", "a_b_c_d_e_f_g_h_i_j_k_l-m.n o"),
        (
            "  MiXeD cAsE with $pecial Chars!  ",
            "MiXeD cAsE with _pecial Chars_",
        ),
        # Unicode characters - should be treated as alphanumeric
        ("你好世界", "你好世界"),
        ("emoji_test_😂", "emoji_test__"),
        ("français_éàç", "français_éàç"),
    ],
)
def test_sanitize_text(input_text: str, expected_output: str) -> None:
    """Test that sanitize_text correctly sanitizes various inputs."""
    assert sanitize_text(input_text) == expected_output
