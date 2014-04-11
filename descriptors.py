"""
class Celsius(object):
    def __get__(self, instance, owner):
        return 9 * (instance.fahrenheit + 32) / 5.0

    def __set__(self, instance, value):
        instance.fahrenheit = 32 + 5 * value / 9.0


class Temperature(object):
    def __init__(self, initial_f):
        self.fahrenheit = initial_f

    celsius = Celsius()

t = Temperature(212)
print(t.celsius)
t.celsius = 0
print(t.fahrenheit)
"""


class Decorator(object):
    def __init__(self, arg):
        print arg
        self.arg = arg

    def __call__(self, cls):
        class Wrapped(cls):

            classattr = self.arg
            BBB = self.arg



            def new_method(self, value):
                return value * 2

        return Wrapped


@Decorator("decorated class")
class TestClass(object):
    def new_method(self, value):
        return value * 3


# dec = Decorator("without notation")
# b = dec(TestClass)
#
# # c = b()
#
# print b.new_method("A")
# print b.BBB
# print b.classattr


b = TestClass()
print b.new_method("A")



