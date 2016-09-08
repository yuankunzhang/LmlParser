# LML Parser

AWS's API gateway does some black magic to perfectly mess up our JSON data.
That's why we need this parse_valuer to save the world.

It parse_values a source string to a Python dictionary. Format of the source
string is defined below.

* The source string begins with a '{', leading white spaces are allowed.
* Each '{' has an enclosing '}', otherwise the source string is malformed.
* Two data types are allowed:
    * Strings are specified by a sequence of raw characters.
    * Objects are specified by a pair of '{' and '}'.
* Elements of an object is specified by this format: `key=value`.
* Elements of an object is split by ',', a trailing ',' after the last element is allowed: `{key1=value1, key2=value2,}`.

For example, this is a valid source string:

```
{product1={id=gold1, price=13}, product2={id=gold2, price=26}}
```