# Aspect Oriented Programming

AOP is a complement of Object-Oriented-Programming. In OOP, the key unit of modularity is class, whereas in AOP the unit of mdularity is the aspect. **Aspects enable the modularization of concerns that cut cross multiple types and objects.**

AOP is used in the Spring Framework to:

* Provide declarative enterprise services
* Let users implement custom aspects

## AOP Concepts

### Aspect

A modularization of a concern that cuts cross multiple classes. In Spring AOP, aspects are implemented by using regular classes or regular classes annotated with @Aspect annoation.

### Join point

A point during the execution of a program, such as execution of a method or handling of an exception.

### Advice

Action taken by an aspect at a particular join point. Different types include *around*, *before*, after *advices*. Action is usually modeled as interceptor and the framework maintains a chain of interceptor around the join point.

### Pointcut

A predicate the matches the join points. Advice is associated with a pointcut expression and run at matched join points. The concept of join points as matched by pointcut expression is central to AOP.

### Introduction

Declaring additional methods or fields on behalf of a type. Spring AOP lets you introduce new interfaces to any advised object.

### Target Object

An object being advised by one or more aspects. A.K.A advised object. Since Spring AOP is implemented by using runtime proxies, this object is always a proxies object.

### AOP Proxies

An object created by AOP framework to implement aspect contracts. In Spring, an AOP proxy is usually a JDK proxy or a CGLIB proxy.

### Weaving

Linking aspects with other application types or object to created an advised object. This can be done at complie, loading or runtime, while Spring does it at runtime.

Spring AOP includes following types of advice:
* Before advice: Advice that runs before a join point but has no ability to prevent the execution proceeding to the join point

* After returning advice: Advice to be executed after a join point completed normally

* After throwing advice: Advice to be executed if a method exits by throwing an exception.

* After (finally) advice: Advice to be executed regardless of the means by which a join point exits

* Around advice: advice surrounds a join point such as a method invocation. It can perform custom behavior before and after the method invocation. It is also responsible for choosing whether to proceed to the join point or return/throw exception.

## AOP Annotaion

* @Before: run before target method
* @After: run after target method
* @AfterReturning: run after normal return of target method
* @AfterThrowing: run after exception has been thrown by target method
* @Around: dynamic proxy(jointPoint.proceed())

### @EnableAspectJAutoProxy
`@Import(AspectJAutoProxyRegistrar.class)` to register an `AnnotationAwareAspectJAutoProxyCreator`, which is a PostProcessor 
1. Create bussiness beans and aspect beans
2. AnnotationAwareAspectJAutoProxyCreator intercepts the creation of beans
3. Wrap aspects advices and create proxy for beans

When executing the target method:
1. proxy method executes target method
2. CglibAopProxy.intercept()
   1. generate a interception chain, MethodInterceptor
   2. Traverse the chain and execute advice following chains rule.



