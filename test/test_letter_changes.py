from challenge import LetterChanges


def test_letter_changes_default():
    assert LetterChanges('fun times!') == 'gvO Ujnft!'

def test_letter_changes_default_001():
    assert LetterChanges('hello*3') == 'Ifmmp*3'
