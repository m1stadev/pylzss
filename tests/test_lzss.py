import hashlib
import random

import lzss
import pytest

# Known-good outputs produced by pylzss 0.3.4 (the last release PyIMG4 pinned).
KNOWN_ANSWERS = [
    (b'', b''),
    (b'A', bytes.fromhex('0141')),
    (b'ABC', bytes.fromhex('07414243')),
    (b' ' * 40, bytes.fromhex('00dcffffff1101')),
    (b'\0' * 40, bytes.fromhex('0100eeff000f0400')),
    (b'abcabcabcabcabcabc', bytes.fromhex('07616263eefc')),
]

CORPUS = (
    b''.join(bytes([i % 251]) * (i % 7 + 1) for i in range(20000))
    + b'The quick brown fox jumps over the lazy dog. ' * 300
)
CORPUS_COMPRESSED_SHA256 = (
    '3c49d8a0f218e6cee0ea8e3816a40ae4fff21ccf5af35c55ad766f04a0348a49'
)


@pytest.mark.parametrize('data, compressed', KNOWN_ANSWERS)
def test_known_answers(data, compressed):
    assert lzss.compress(data) == compressed
    assert lzss.decompress(compressed) == data


def test_corpus_matches_0_3_4():
    compressed = lzss.compress(CORPUS)
    assert hashlib.sha256(compressed).hexdigest() == CORPUS_COMPRESSED_SHA256
    assert lzss.decompress(compressed) == CORPUS


@pytest.mark.parametrize(
    'size', list(range(0, 70)) + [255, 256, 4077, 4078, 4095, 4096, 4097, 65537]
)
def test_roundtrip_sizes(size):
    rnd = random.Random(size)
    for data in (
        bytes(rnd.randrange(256) for _ in range(size)),
        b'\0' * size,
        b' ' * size,
        (b'ab' * size)[:size],
    ):
        assert lzss.decompress(lzss.compress(data)) == data


def test_initial_buffer_values():
    data = b'AAAA' * 8
    compressed = lzss.compress(data, initial_buffer_values=0x41414141)
    # The pre-filled window already holds the input, so it compresses to back-references only.
    assert len(compressed) < len(lzss.compress(data))
    assert lzss.decompress(compressed, initial_buffer_values=0x41414141) == data
    # Reference into the pre-filled window.
    assert lzss.decompress(bytes.fromhex('000f')) == b''
    assert lzss.decompress(bytes.fromhex('00000f')) == b' ' * 18
    assert (
        lzss.decompress(bytes.fromhex('00000f'), initial_buffer_values=0x41414141)
        == b'A' * 18
    )
