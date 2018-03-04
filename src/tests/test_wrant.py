from wrant import create_wrant

def test_wrant_bootup():
    wrant = create_wrant()
    assert wrant != None
    assert wrant.nlp != None

    # components
    assert wrant.concorder != None
    assert wrant.concorder.tokens != None
    assert wrant.concorder.offsets != None

    assert wrant.suggester != None
    assert wrant.suggester.tokens != None
    assert wrant.suggester.offsets != None
