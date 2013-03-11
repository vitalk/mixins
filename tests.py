#!/usr/bin/python
# -*- coding: utf-8 -*-
from attest import Tests, assert_hook, raises

from mixins import *


mixin = Tests()


@mixin.test
def user_mixin():
    class User(UserMixin):
        pass

    user = User(email='vital@laptop')
    assert user.email == 'vital@laptop'
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

    user.is_active = True
    assert user.is_active
    assert user.activation_key is None


@mixin.test
def gravatar_mixin():
    class User(GravatarMixin):
        GRAVATAR_FALLBACK = 'monsterid'
        GRAVATAR_DEFAULT_SIZE = 128

    user = User('email@example.com')
    GRAVATAR_URL = 'http://www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e?s=128&d=monsterid'
    assert user.avatar_url == GRAVATAR_URL
    assert user.get_gravatar_url() == GRAVATAR_URL


if __name__ == '__main__':
    mixin.main()
