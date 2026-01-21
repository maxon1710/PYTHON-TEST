def test_use_fixture(my_data):
    print("fixture value:", my_data)
    assert my_data == 5
