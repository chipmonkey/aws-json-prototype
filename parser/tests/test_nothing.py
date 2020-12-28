""" Run an empty test to avoid failing if no other tests are run
This is helpful when we filter the active test set to zero due to previos successes
THIS test should never be filtered out
"""
def test_placeholder():
    pass
