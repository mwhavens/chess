class MyClass:
    __var2 = 'var2'
    var3 = 'var3'

    def __init__(self):
        self.__var1 = 'var1'

    def normal_method(self):
        print(self.__var1)

    @classmethod
    def class_method(cls):
       print(cls.__var2)

    def my_method(self):
        print(self.__var1)
        print(self.__var2)
        print(self.__class__.__var2)

if __name__ == '__main__':
    print(MyClass.__dict__['var3'])

    clzz = MyClass()
    clzz.my_method()
