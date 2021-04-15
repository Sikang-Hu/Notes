# Java Multithreading

* Implements Runnable: good for sharing data, not restricted by single inheritance.
* Extends Thread

## Status

* NEW
* RUNNABLE
* BLOCKED
* WAITING
* TIMED_WAITING
* TERMINATED 


```java
// Thread-safe lazy load
class Test {
    private static Test instance = null;

    private Test() {}

    public static getInstance() {
        if (instance == null) {
            synchronized (Test.class) {
                if (instance == null)
                    instance = new Test();
            }
        }
        return instance;
    }
}
```

* Avoid definetion of shared data
* Avoid embeded sychronization

## Lock
```java
class Test implements Runnable {
    private int ticket = 100;
    private ReentrantLock lock = new ReentrantLock();

    @Override
    public void run() {
        while (true) {
            try {
                lock.lock()

                if (ticket > 0) {
                    // sleep to catch data racing case.
                    System.out.println(Thread.currentThread().getName() + ": " + ticket);
                    ticket--;
                } else break;
            }
        }
    }

    public static void main() {
        Test t = new Test();

        Thread t1 = new Thread(t);
        Thread t2 = new Thread(t);
        Thread t3 = new Thread(t);

        t1.start();
        t2.start();
        t3.start();
    }
}
```

Difference between synchronized & Lock:
* synchronized release the monitor automatically, while the lock needs to be released manually.
* While using lock, jvm spend less time to schedule threads, giving a better performance. And it provides better extendability(can be extended).

Lock > synchronized block > synchronized method

## Communication between Threads
Can only be used in synchronized block or method.
* wait()
* notify()
* notifyAll()

sleep() vs. wait() :
* Thread.sleep() vs. obj.wait() (declared as an instance method in Object class)
* sleep() can be called anywhere while wait() can only be called in synchronized block
* sleep() does not release monitors.

## Callable since jdk 5.0

## Thread pools
Advantages: 
* Responsive, reduce the time to create new Thread
* Reuse resources
* Easy to manage Threads, there are a bunch of parameter can be configured:
  * corePoolSize
  * maximumPoolSize
  * keepAliveTime
```java
ExecutorService service = Executors.newFixedThreadPool(10);

service.execute(Runnable);
service.submit(Callable);
```

## IO stream
abstract class:
byte stream(8 bit): InputStream, OutputStream used for non-text file
char stream(16 bit, depends on how the data encoded): Reader, Writer used for text file(.txt, .java, .c, cpp)

Buffered Stream: for better performance

## Reflection

### Get the super class in the runtime

This is useful in framework, such as get the generic of the DAO

```java
public void getSuperClass() {
    Class clazz = Person.class;

    Type genericSuperclass = clazz.getGenericSuperclass();

    ParameterizedType paramType = (ParameterizedType) genericSuperclass;
    // Get all the generic types, which is actually Class object
    Type[] actualTypeArguments = paramType.getActualTypeArguments();
}
```

### Get the interface, pacakge and Annotation

```java
public void getInterface() {
    Class clazz = Person.class;

    Class[] interfaces = clazz.getInterfaces();
    for (Class c : interfaces) {
        System.out.println(c);
    }

    Package pack = clazz.getPackage();
    System.out.println(pack);

    Annotation[] annotations = clazz.getAnnotations();
    for (Annotation annos : annotations) {
        System.out.println(annos);
    }
}
```

### Invoke static method at runtime

```java
public void getMethod() throws Exception{
    Class clazz = Person.class;
    // 1. method's name; 2. list of arguments
    Method show = clazz.getDeclaredMethod("show", String.class);
    show.setAccessible(true);
    Object returnValue = show.invoke(null, "CHN"); // can also give the Class object, i.e. Person.class
    // If the method has now return value, returnValue will be null
}
```

### Dynamic Proxy





