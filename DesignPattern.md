# Design Pattern

* Reuseable: don't need to re-write code with same functionality
* Readable
* Extendable, Maintainable: easy to add new features
* Reliable: new features has not effect on old features
* Loose Coupling and higher cohesive:

## 7 Design Principles
Three important characteristics of a bad design:
* Rigidity: hard to change, since every change affects too many other parts
* Fragility: when make a change, unexpected parts of system break.
* Immobility: hard to reuse in another app, since it cannot be disentangled.

### Single Responsibility Principle
A class should have only one reason to change. When we need to make a change in a class having more responsibilities the change might affect the other functionality of the classes. 

If there logic is pretty simple, and only has few methods, we can maintain the principle at method level.

### Open Close Principle
Open for extension(for provider), but closed for modification(for user).

### Liskov's Substitution Principle
Inheritance couples classes(invasive): when modified a class, we need to consider all of its subclass, since it may affect the behavior of subclass. 

New derived class should just extend without replacing the functionality of old classes. Otherwise it can produce undesired effects when they are used in existing program. 

Liskov's Substitution Principle states that if a program module is using a Base Class, then the reference to the Base class can be replaced with a Derived class without affecting the functionality of the program module.

E.g. square and rectangle. Fix: derive the rectangle and square from a common "Polygon" or "Shape", which does not enforce any rules regarding width ad height.

To fix violation of LSP, create a new common Base class for the super and sub classes, and use depend, aggregate, composite relationships to link them.

### Interface Segregation Principle
Client should not be forced to depend upon interfaces that they don't use. Only add methods that should be there when write interfaces.

### Dependency Inversion Principle
High-level modules should not depend on low-level modules. Both should depend on abstractions.
Abstractions should not depend on details. **Details should depend on abstractions**.

Dependency can be passed by interface, constructor and setter.

### Law of Demeter
* Each unit should have only limited knowledge about other units: only units "closely" related to the current unit.
* Each unit should only talk to its friends; don't talk to strangers.
* Only talk to your immediate friends.

### Composite Reuse Principle
Composite(passed by constructor, i.e. required) and Aggregation(pass by setter, i.e. optional) over inheritance.

## Overview of Design Pattern

There are three categories: creational patterns, behavior patterns, structural patterns.

### Creational Patterns
* Singleton
* Factory
* Abstract Factory
* Bulder
* Prototype

### Structural Patterns
* Adapter
* Bridge
* Composite
* Decorator
* Flyweight
* Proxy

### Behavior patterns
* Chain of Responsibility
* Command
* Interpreter
* Iterator
* Mediator
* Memento
* Observer
* Strategy
* Template Method
* Visitor
* Null Object

## Singleton

Ensure that only one instance of a class is created, and provide a global point of access to the object. Usually singleton are used for centralized management of internal or external resource. Sometimes, it is costy to create such a instance, like SessionFactory in Hibernate.
Recommend using static nested class and enum.

### In JDK
java.lang.Runtime is a singleton instance. It is in hungry mode.

### Use Cases
* Frequently created and destroyed object
* Initialization of object cost a lot of resources (data source, session factory)
* Utils objects

## Factory Method
* Createobjects without exposing the instantiation logic to the client.
* Refer to the newly created object through a common interface.

The Advantage is that when there is any new type added, there is no need to modify client code.

### Simple Factory / Static Factory
```java
public class ProductFactory{
	public Product createProduct(String ProductID){
		if (id==ID1)
			return new OneProduct();
		if (id==ID2) return
			return new AnotherProduct();
		... // so on for the other Ids
		
        return null; //if the id doesn't have any of the expected values
    }
    ...
}
```
If we add a new concrete product, we should modify the Factory class, still violate OCP
### Factory Method
Define an interface to create a object, but leaves the choice of its type to the subclasses.

### Abstract Factory

## Prototype
It allows an object to create customized objects without knowing their class or any details of how to create them.
### Deep Copy
* Override clone()
* Serialization (recommended)

## Builder
Decoupling the product and the initialization of the product.

## Adapter

## Bridge
Seperate the Abstraction with the Implementaion, and assign separate inheritence tree for it.

## Decorator

java.io


