class Person:
    def __init__(self, name, age, occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

    def greet(self):
        print("Hello, my name is", self.name, "and I am", self.age, "years old.")

    def change_occupation(self, new_occupation):
        self.occupation = new_occupation

person1 = Person("Alice", 30, "Software Engineer")
person1.greet()
print("Person 1's occupation:", person1.occupation)

person1.change_occupation("Data Scientist")
print("Person 1's occupation after change:", person1.occupation)
