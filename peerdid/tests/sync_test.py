import os
import pytest

from ..sync import get_state
from .. import get_predefined_did_value
from ..delta import Delta
from ..file import File


def test_get_state_for_unknown_did(scratch_repo):
    with pytest.raises(AttributeError):
        get_state(scratch_repo, "did:peer:foo")


def test_get_state_for_reserved_did(scratch_repo):
    with pytest.raises(AttributeError):
        get_state(scratch_repo, get_predefined_did_value('1'))


def test_get_state_for_1_normal_did(sample_delta, scratch_file, scratch_repo):
    scratch_file.append(sample_delta)
    scratch_repo.new_doc(scratch_file.genesis)
    snapshot = get_state(scratch_repo, scratch_file.did)
    assert len(snapshot) == 1
    assert snapshot[0]["did:peer:1zQmeiupQudTUZfotKWHhVVrtnA5Vu721Su68XZB35Kh3hTV"] == "WDuyVDIB7R1C6GhHX9lxhowEMCQkSw_QwBRtBvEFzVg="


def test_get_state_for_2_normal_dids(scratch_space, scratch_file, scratch_repo):
    scratch_file.append(Delta('{"publicKeys": {"key-1": "foo"}}', []))
    scratch_repo.new_doc(scratch_file.genesis)
    f2 = File(os.path.join(scratch_space.name, 'peerdid-file2'))
    f2.append(Delta('{"publicKeys": {"key-2": "foo"}}', []))
    scratch_repo.new_doc(f2.genesis)
    snapshot = get_state(scratch_repo, scratch_file.did, f2.did)
    assert len(snapshot) == 2
    did_a = 'did:peer:1zQmb6WrwDimrMTNJFZcBe86A96gF9D5APikmeeyhg4jwQuT'
    did_b = 'did:peer:1zQmXT4fGHZMnLfWyXnzMZR9qjpdNkq1w3EbvV95Z5aUsrme'
    a = snapshot[0] if did_a in snapshot[0] else snapshot[1]
    b = snapshot[1] if a == snapshot[0] else snapshot[0]
    assert did_a in a
    assert did_b in b
    assert a[did_a] == '4GKyAZVLGaSvb81v6RA3acWRzhV5vhzhHNzBCyri2Ek='
    assert b[did_b] == 'qWlggN0vuqzOtWEo_37lb5yHVHku5H7lFcYODMaR5-k='
