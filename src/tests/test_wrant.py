from wrant import create_wrant


def test_wrant_boots_up():
    wrant = create_wrant()
    assert wrant is not None
    assert wrant.nlp is not None

    # components
    assert wrant.concorder is not None
    assert wrant.concorder.tokens is not None
    assert wrant.concorder.offsets is not None

    assert wrant.suggester is not None
    assert wrant.suggester.tokens is not None
    assert wrant.suggester.offsets is not None

    assert wrant.verbs_prep is not None
    assert wrant.verbs_prep.verbs is not None
