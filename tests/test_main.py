from golden_ratio_dual_gate import main


def test_main(capsys):
    main()
    assert capsys.readouterr().out
