"""This module defines a key generator."""

import random


def key(
        seq,
        tooth=lambda seq: str(random.SystemRandom().choice(seq)).strip(),
        nteeth=6,
        delimiter=' ',
):
    """Concatenate strings generated by the tooth function."""
    return delimiter.join(tooth(seq) for _ in range(nteeth))