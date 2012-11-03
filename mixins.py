#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from urllib import urlencode
from hashlib import sha1, md5


__version__ = '0.2'
__all__ = ['randstr', 'UserMixin', 'ActivationMixin', 'GravatarMixin']


def randstr(len, reallyrandom=False):
    """Generate random string alphanumeric string of length 'len'.  If really
    random, add uppercase and punctuation and suitable for use as
    salt.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    if reallyrandom:
        alphabet += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=~\|,.<>?/;:{}[]'
    return u''.join(random.choice(alphabet) for i in range(len))


class UserMixin(object):
    """This class provides simple way to add authentication to base model. All
    password encryption and salting handles automatically via the 'password'
    property.

    It's possible to keep password empty, this is useful if you don't manage
    password auth internally(maybe through openid?). But if you try to access
    the password then assertion raises.

    >>> user = User(name='vital')
    >>> user.password
    Traceback (most recent call last):
    ...
    AssertionError: Some dumbass forgot to set a password?
    >>> user.verify_password('oops')
    Traceback (most recent call last):
    ...
    AssertionError: Some dumbass forgot to set a password?

    After we explicitly set a new password all be fine.

    >>> user.password = 'secret'
    >>> user.verify_password('secret')
    True

    """
    # default password salt size(32)
    SALT_SIZE = 1<<5

    def __init__(self, name, password=None):
        """Base init."""
        self.name = name
        self.pswdhash = None
        if password:
            self.password = password

    @property
    def password(self):
        """Password getter."""
        assert self.pswdhash, 'Some dumbass forgot to set a password?'
        return self.pswdhash

    @password.setter
    def password(self, raw):
        """Password setter. Provides password hashing and salting for raw
        password value.
        """
        self.pswdhash = self.passhash(raw)

    def verify_password(self, raw):
        """Verify for a password match with the given raw password."""
        return self.password == self.passhash(raw, self.password[:self.SALT_SIZE])

    @classmethod
    def passhash(cls, password, salt=True):
        """Generate salted hash for password."""
        if salt is True:
            salt = randstr(cls.SALT_SIZE)
        to_hash = u'%s:%s' % (password, salt)
        to_hash = to_hash.encode('utf-8')
        return salt + sha1(to_hash).hexdigest()


class ActivationMixin(object):
    """This class provide simple activation properties to base model.

    >>> class User(ActivationMixin):
    ...     pass
    ...
    >>> user = User()
    >>> user.is_active
    True

    If user is not active, then the user property `activation_key` contains
    random token.

    >>> user.is_active = False
    >>> user.activation_key is not None
    True

    """
    # default activation token length(32)
    ACTIVATION_TOKEN_LENGTH = 32

    def __init__(self):
        self.activation_key = None

    @property
    def is_active(self):
        return self.activation_key is None

    @is_active.setter
    def is_active(self, value):
        if value:
            self.activation_key = None
        else:
            self.activation_key = randstr(self.ACTIVATION_TOKEN_LENGTH)


class GravatarMixin(object):
    """This class provide methods to get gravatar image.

    >>> class User(GravatarMixin):
    ...     pass
    >>> user = User(email='email@example.com')
    >>> user.avatar_url
    'http://www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e?s=48&d=mm'
    """
    GRAVATAR_URL = 'http://www.gravatar.com/avatar'
    GRAVATAR_FALLBACK = 'mm'
    GRAVATAR_DEFAULT_SIZE = 48

    def __init__(self, email):
        self.email = email

    def get_gravatar_url(self, size=None):
        """Returns the gravatar URL."""
        gravatar_url = '%(url)s/%(hash)s?' % {
            'url': self.GRAVATAR_URL,
            'hash': md5(self.email.encode('utf8').lower()).hexdigest()
        }
        return gravatar_url + urlencode({
            'd': self.GRAVATAR_FALLBACK,
            's': size or self.GRAVATAR_DEFAULT_SIZE
        })

    @property
    def avatar_url(self):
        return self.get_gravatar_url()
