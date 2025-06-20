import pytest
from aqt.addcards import AddCards
from anki.notes import Note
from aqt import mw

# Helper para criar nota com tags e stickiness simulada
def make_note_with_tags_and_sticky(tags, sticky):
    note = mw.col.newNote()
    note.tags = tags
    # Simula um modelo com campo sticky ou não
    flds = note.note_type()["flds"]
    for fld in flds:
        fld["sticky"] = sticky
    return note

@pytest.fixture
def widget(qtbot):
    add_cards = AddCards(mw)
    qtbot.addWidget(add_cards)
    return add_cards

# CT1 - C1: sticky_fields_from is None (CD1 = False)
def test_load_new_note_none(widget):
    # Executa método com sticky_fields_from = None
    widget._load_new_note(None)

    # Verifica se a nota foi criada e não herdou campos nem tags
    note = widget.note
    assert note is not None
    assert all(f == "" for f in note.fields)
    assert note.tags == []

# CT2 - C2: sticky_fields_from exists, but fields are not sticky (CD1 = True, CD2 = False)
def test_load_new_note_tags_only(widget):
    old_note = make_note_with_tags_and_sticky(["tag1"], sticky=False)
    old_note.fields = ["campo1", "campo2"]

    widget._load_new_note(old_note)

    # Só as tags são copiadas
    note = widget.note
    assert note.tags == ["tag1"]
    assert note.fields != ["campo1", "campo2"]
    assert all(f == "" for f in note.fields)

# CT3 - C3: sticky_fields_from exists, and fields are sticky (CD1 = True, CD2 = True)
def test_load_new_note_tags_and_fields(widget):
    old_note = make_note_with_tags_and_sticky(["tag1"], sticky=True)
    old_note.fields = ["campo1", "campo2"]

    widget._load_new_note(old_note)

    # Tags e campos sticky devem ser copiados
    note = widget.note
    assert note.tags == ["tag1"]
    assert note.fields == ["campo1", "campo2"]
