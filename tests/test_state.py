from trainer_host.state import TrainerState


def test_flag_toggle():
    s = TrainerState()
    assert s.godmode is False
    s.set_flag("godmode", True)
    assert s.godmode is True


def test_shutdown():
    s = TrainerState()
    s.shutdown()
    assert s.alive is False
</br>