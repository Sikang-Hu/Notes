# Effective Python

## PEP 8
* In a file , functions and classes should be separated by two blank lines.
* In a class, method should be separated by one blank line
* **Functions**, **variables** and **attributes** should be in `lowercase_underscore`
* Protected instance attribute should be in `_leading_underscore`
* private instance attributes should be in `__double_leading_underscore`
* Classes (including exceptions) should be in `CapitalizedWord`
* Instance methods in classs should use `self` refer to the as the first parameter
* Class methods should use `cls`, which refers to the class, as the name of the first parameter.

* Use inline negation `if a is not b`
* Use `if not somelist` to check for empty, and assume that empty values will implicitly evaluate to `False`, don't use `if len(somelist) == 0`
* if cannot fit an expression on one line, surround it with parenteses and add line breaks

* import should be in sections in the folowing order: standard library modules, third-party modules, your own modules, and in **alphabetical** order.

## `bytes` and `str`

Instances of `bytes` contain raw, unsigned 8-bit values(displayed in the ASCII encoding). Instances of `str` contain Unicode code points that represent textual chracters from human languages.

To convert `str` to `bytes`, we need encoe mathod of `str`, and `decode` for backward. Do the encoding and decoding at the furthest boundary of your interfaces.

You can use the `+` operator to add two `bytes` or `str`, but you cannot add `str` to a `bytes`

## Item 10 Prevent Repetition with Assignment Expressions

`:=` a walrus b, this enable you to assign variabels in places where assignment statements are disallowed, such as in the conditional expression of an `if` statement. 

```python
if (count := fresh_fruit.get('lemon', 0)) > 4: # When a assignment expression is a subexpression of a larger expression, it must be surrounded with parentheses.
    make_lemonade(count)
else:
    out_of_stock()
```

```python
bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
```

## Item 11: Slice sequences

Slicing allows you to access a subset of a sequence's items with minimal effort. Slicing can be extended to any Python class that implements the `__getitem__` and `__setitem__`, basic:
```python
somelist[start:end] # end exclusive
a[:]
a[:-1] # negative value for doing offsets relative to the end of a list

first_twenty_item = a[:30] # slicing deals properly with start and end indexes that are beyond the boundaries
last_twenty_item = a[-30:]
```

The result of slicing is a whole new `list`. References to the objects from the original `list` are maintained. Modify the result won't change the original list. But when used in assignments, slices replace the specified range in the original `list`, the lengths of the slice assignments don't need to be the same.
```python
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After ', a)
```

When assigned to a slice with no start or end indexes, you replace the entire contents of the `list` with a copy of what's referenced, not allocating a new list.

## Item 12: Avoid Striding and Slicing in a Single Expression

`somelist[start:end:stride]`

Aovid using stride with start or end indexes, since it is confusing. Prefer makign it a positive value and omit start and end indexes.

## Item 13: Prefer Catch-All Unpacking Over Slicing

* catch-all unpacking throuhg a starred expression. 
* The starred expression can appear in any position. 
* But you have to have at lease one required part.
* You cannot use multiple catch-all expressions in a single-level unpacking pattern
* But you can use multiple starred expressions in an unpacking assignment statement, as long as they're catching for different parts.
* Can also use this expresssion to unpack an iterator but you are risking using up your memmory, since it is turned into a list.
```python
oldest, second_oldest, *other = car_ages_descending
oldest, *other, youngest = car_ages_descending
*other, second_youndest, youngest = car_ages_descending
```

## Item 14: Sort by Complex Criteria Using the `key` Parameter
```python
list.sort(key=lambda x: x.name)
```

If you have multiple criteria, you can use `tuple` type, which is comparable by default and have a natural ordering. One downside is that the direction of sorting for all criteria must be the same. In this case, you can call sort multiple times as the sort in python is stable.

## Item 15: Be cautious when relying on `dict` insertion order

After python 3.6, the insertion order is preserved.


## Item 39: Use @classmethod Polymorphism to Construct Objects Generically

* python only support a single constructor per class
* we can use `@classmethod` to define alternative constructor for the class, like a factory method.
* Use the class method polymorphism to provide generic ways to build and connect many concrete subclass.
  * You can put the abstract operatoring in the higher level and use the `cls` passed in to create the instance of the concrete subclass.

## Item 40: Initialize Parent Class with `super`

The old simple way to initialize a parent class from child class is simply call the parent class's `__init__`
```python
class MyBase:
    def __init__(self, value):
        self.value = value
    
class MyChild(MyBase):
    def __init__(self):
        MyBase.__init__(self, 5)
```
However, this may result to confusion in multiple inheritance:
* when the order of initialization is inconsistent with the order in class definition.
```python
class MyChild(MyBase1, MyBase2):
    def __init__(self):
        MyBase2.__init__()
        MyBase1.__init__()
```
* When there is diamond inheritance, there will be unexpected behavior
```python
class MyBase1(MyBase):
    def __init__(self):
        MyBase.__init__(self, 1)
        self.value += 1

class MyBase2(MyBase):
    def __init__(self):
        MyBase.__init__(self, 1)
        self.value += 2

a = MyChild()
print(a.value) # 2, is not 4 because MyBase1.__init__() calls MyBase's __init__ and reset the value again.
```
* By using `super().__init__()`, we rely on the python's built-in funciton and standard methond resolution order(MRO). `super` ensures common ancesters only run once. The MRO defines the order in which superclasses are initialized, following an algorithm called `C3 linearization`
* `super()` can also be called with two extra parameters, but usually called with only no parameters, python compiler automatically provides the correct parameters (`__class__` and `self`)

# Item 41: