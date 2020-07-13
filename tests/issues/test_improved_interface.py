from gata import Dataclass


def test_improved_interface() -> None:
    class Song(Dataclass, frozen=True):
        title: str
        artist: str

    raw_song = {"title": "test", "artist": "Test Artist"}

    song = Song(**raw_song)
    song_repr = repr(song)
    assert song.serialise() == raw_song
    assert "test_improved_interface.<locals>.Song" in song_repr

