from gata import Validator

assert Validator.assert_email("email@test.com")
assert Validator.assert_integer(12)
assert Validator.assert_duration("PT2H")
