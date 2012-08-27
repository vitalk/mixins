# mixins

A python module that contains a useful mixins. Sadly now it contains only user
authentication mixin.

## UserMixin

This class provides simple way to add authentication to base model. All
password encryption and salting handles automatically via the 'password'
property.

It's possible to keep password empty, this is useful if you don't manage
password auth internally(maybe thought openid?). But if you try to access
the password then assertion raises.

## Copyright

Copyright © 2012 Vital Kudzelka <vital.kudzelka@gmail.com>.

This code shall be used for Good, not Evil.
