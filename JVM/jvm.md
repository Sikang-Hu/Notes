# Java Virtual Machine

## Class Loading process

### Loading

### Linking

#### Verify

#### Prepare

#### Resolve

### Initializing

## JVM stack
set a fixed size for the stack -Xss`<size>`

### Data Structure in the Stack
Every thread has its own stack, data stored in *Stack Frame*. **Every methods executed by this thread has its corresponding stack frame, they are 1 to 1 mapped.** At one time, there is only one active stack frame in a active thread, which is called *Current Frame*, and its corresponding method is called *Current Method*, the class defining this class is *Current Class*. The byte code executed by the execute engine only applies on current frame. If this method calls other method, there will be a new stack frame to be put at the top of the stack.

Stack frames of different thread cannot refer each other.

Method can be terminated by normal return or throwing a exception.

### Structure of Stack Frame

`javap -v <.class file>` to view the bytecode file, or use jclasslib plugin in the IntelliJ.

* Local Variables
* Operand Stack
* Dynamic Linking
* Return Address
* Additional information: Optional, depends on implementation of JVM. 

#### Local Variables
An array of int to store parameters and local variables, can store primitive, reference and returnAddress. The size of the local variables is determined when compiled. Slot is the smallest unit in local variables table. Data type within 32bits takes one slot, while 64bits(long, double) data type takes two slot.

If current frame is created by constructor or instance method, the reference to this object will be put at index 0, and the rest will be arrange by their declaration sequence. The slot can be reused if a local variable's field ends(e.g. for loop or if block ends).

When the method ends, the local variables table will also be destroyed.

The local variable is the most related part in jvm optimization in the stack frame.

#### Operand Stack
A stack implemented by **array**, also called Expression Stack. It is used to stored the intermediate result during the execution. The stack will be created when the when the method begin to be executed. Every stack has a `max_stack` for the depth of the stack, which is defined at the compiling. 32bits data type takes one slot, while 64bits data type takes one slot. The return value will be push into the stack lastly.

#### Top-of-Stack Cashing
Stack-based virtual machine has more compact structure, but it needs more instruction to complete an operation, i.e. more instruction dispatch and memory read/write. To optimize this, HotSpot JVM designed the ToS, caching all top-of-stack element in the register of the physical CPU to reduce the read/write to the memory to improve the performance.

#### Dynamic Linking
Every stack frame contains a reference to the method it belong in the runtime constant pool. The purpose of storing it is to support dynamic linking(invokedynamic).

When java source code is compiled to bytecode, all the variables and method references stored as **Symbolic Reference** in the constant pool. Dynamic linking is used to convert the symbolic reference to direct reference.

#### Method Invocation
1. Static linking: when the method to be invoked is known at compiling, and won't change during the execution, converting the symbolic reference to direct reference is static linking.
2. Dynamic Linking: the method to be invoked cannot be determined during the compilation, the conversion is dynamic linking. 


Binding is to convert the symbolic reference to direct reference.
* Early binding: target method can be determined at the compilation
* Late binding: determined at the runtime, e.g. call the methods of interfaces.

* Virtual Method: *invokevirtual(while calling final method through this instruction, final method is non-virtual), invokeinterface*
* Non-Virtual Method: can be determined at the compilation, static method, private method, constructor, super.xxx(). *invokestatic, invokespecial*

invokedynamic is for dynamic linking. Used in anonymous object:
```java
Comparator<String> cmp = (a, c) -> {
    if (a.equals(c))
        return 0;
    else
        return a.compareTo(c);
};
```

* To improve the performance of invoking virtual method, there is a virtual method table in the jvm's method area. Every class has a virtual method table, which contains the actual entrance of the methods. The virtual method table will be create at the linking. After prepare for the inital value of class members, its table will also be initialized(at Resolve phase).

#### Return Address
Store the value in the PC register of the method's caller, i.e. the address of the next instruction of its caller. 

* There is no GC in the stack.
* Local variable is not always thread safe, if the local reference pointed to a object can be accessed by other methods, e.g.
```java
public static void method1() {
    // thread safe, there is no other method can access s1
    StringBuilder s = new StringBuilder();
    s.append("a");

}

public static void method2(StringBuilder s) {
    // not thread safe, the reference is passed from the outside, other methods can access the object
    s = new StringBuilder();
    s.append("a");
}

public static void method3() {
    // not thread safe, the object is returned, which means the methods from outside can modified it.
    StringBuilder s = new StringBuilder();
    s.append("a");
    return s;
}
```

### Native Method Stack
Stack for native method. When a thread invoke a native method, it enters a new state out of JVM's contraint, and it has the same access as JVM.
* Native method can access jvm's runtime data areas through native method interface
* Can use register of physical cpu
* Can acquire memory from local heap.

## Native Method
Java invokes non-java code. E.g. getClass(). no method body for native method.

## Heap
Heap and Method Area are unique for each process(i.e. a jvm instance). Heap is created when jvm bootstrapped, and its size is also determined at that time. It is the largest area managed by jvm. Heap can lie on incontinuous chunk in the physical memory, but continuous in logical memory. All the threads share the heap, and there are private buffer for each thread(Thread Local Allocation Buffer, TLAB).


