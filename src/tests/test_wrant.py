from wrant import create_wrant

def test_wrant_bootup():
    wrant = create_wrant()
    assert wrant != None
    assert wrant.nlp != None

    # components
    assert wrant.concorder != None
    assert wrant.concorder.text != None
