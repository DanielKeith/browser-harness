"""Agent-editable browser helpers.

Add task-specific browser primitives here. Core helpers from browser_harness.helpers
load this file when BH_AGENT_WORKSPACE points at this directory, or when this
repo's default agent-workspace exists.
"""


def lexical_type(text):
    """Type multi-paragraph TEXT into a Lexical / rich contenteditable composer
    (Reddit comment box, Product Hunt comment box) so paragraph breaks SURVIVE.

    Why this exists: type_text() is a single Input.insertText carrying the
    literal "\\n\\n". Lexical (and most rich contenteditable editors) strips
    those newlines, because it only creates paragraph blocks in response to real
    Enter key events, not from "\\n" chars inside an inserted string. So a bulk
    type_text(body) posts a wall of text with every paragraph break gone. This
    shipped broken on two consecutive Reddit batches (2026-05-21, 2026-05-22)
    before it was caught.

    This splits the body on blank lines and presses Enter once between
    paragraphs. Verified 2026-05-22 against Reddit's composer DOM: one Enter ==
    one paragraph block (<p>..</p><p><br></p><p>..</p>); two Enters over-space.

    Do NOT use this for plain <textarea> composers (Hacker News, Indie Hackers):
    a textarea keeps "\\n" literally, so a single type_text(body) is correct and
    simpler there.
    """
    from browser_harness.helpers import type_text, press_key
    paras = [p for p in text.split("\n\n") if p.strip()]
    for i, p in enumerate(paras):
        type_text(p)
        if i < len(paras) - 1:
            press_key("Enter")  # one Enter == one paragraph break in Lexical
    return len(paras)
