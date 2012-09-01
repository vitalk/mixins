#!/usr/bin/python
# -*- coding: utf-8 -*-
from attest import Tests, assert_hook, raises

from mixins import *


mixin = Tests()


@mixin.test
def user_mixin():
    class User(UserMixin):
        pass

    user = User(name='vital')
    assert user.name == 'vital'
    # while password not set raise assertion error on access
    with raises(AssertionError):
        assert user.password
        assert user.verify_password('oops')

    user.password = 'so secret'
    assert user.verify_password('so secret')
    assert not user.verify_password('wrong')


@mixin.test
def activation_mixin():
    class User(ActivationMixin):
        pass

    user = User()
    assert user.is_active
    assert user.activation_key is None

    user.is_active = False
    assert user.is_active == False
    assert user.activation_key is not None


if __name__ == '__main__':
    mixin.main()
