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

The heap area is the run-time data area from which memory for almost all the class instances and arrays is allocated. Object in the heap will not be removed right after the return of methods, GC will collect the space then.

* Young Generation Space
  * Eden Space
  * Survivor
* Tenure Generation Space
* Permanent Space(Meta Space after JDK 8) Implemented in Method Area


(-X is runtime parameter for the jvm)

* -XX:+PrintGCDetails to print gc info
* -Xms: set the initial memory of the heap area, same as -XX:InitialHeapSize
* -Xmx: set the maximum memory of the heap area, same as -XX:MaxHeapSize. If there this limit is exceeded, there will be a OutOfMemoryError.

The configuration for heap only affect Young Generation and Tenure Generation Space, not the Permanent Space. 


Usually, we will set initial and the maximum the same, so that the gc does not need reassign the heap after clear the heap, which improve the performance. By default, the inital mem is set to physical mem / 64, while the maximum is set to physical mem / 4. The actual memory of Runtime will be less than the declared because only one survivor region can be used(either s0 or s1). Apart from that, There are some preoccupied space in the memory, so the actual size might be less than declared physical mem. 

### Young Generation and Old Generation
Object in java can be divided into two types:
1. Short life cycle, the creation and destroy of this object is pretty fast.
2. Long life cycle, sometimes can be as long as jvm's.

`-XX:NewRatio` to configure the ratio of OG and YG, which is 2 by default. e.g. -XX:NewRatio=2 YG takes 1/3 and OG takes 2/3. If there are more type 2 objects, we can use increase the size of OG.

`-XX:SurvivorRatio` to configure the ratio of Eden Space to the survivor spaces, which is 8 by default, i.e. 8:1:1. If not, we can assign explicitly.
`-XX:-UseAdaptiveSizePolicy`(minus to close the adaptive memory allocation policy).
`-Xmn`: set the size of Young Generation Space. It will override -XX:NewRatio parameter.

* Most object will be initialized at Eden Space, but if its size exceed the limit of Eden Space, it will be put at other area, like OG. 
* Most object will be destroyed at the Eden Space.

### Memory Assignment
1. The newly created object is put at Eden Space
2. When Eden space is full, and there is new object to be create, the jvm will collect the garbage in the Eden Space(YGC/Minor GC), destroy the object referred by nothing。
3. Move the survivor to the survivor 0 area, and tag it with age = 1, and create the new object.
4. If another GC is triggered, survivors from last time will be put at survivor 1 if they are not collected. And their age will be incremented.
5. When the a survior's age is equal to 15, the next time it will be promoted into old generation area(promotion). Can set this parameter: `-XX:MaxTenuringThreshold=<N>` to configure.

GC happens in the YG frequently, in OG seldomly and barely at Permanent Space/Meta Space.

#### Special Case

If the object is too large to be put in the YG, it will be put into OG directly. If is does not fit into the OG, majorGC/FGC will be triggered, and the object will be put after GC. If still cannot fit into OG, OutOfMemoryError will be thrown.

If the object in Eden Space is larger than the size of suvivor space, it will be put into the OG directly.

If the total size of objects with the same age in the survivor space exceeds half the size of survivor, all objects at that age or elder than that will be put into OG, ignoring MaxTenuringThreshold.

#### Minor GC, Major GC and Full GC
When jvm collects the garbage, it will not always collect on all three space. Mostly, the GC happens at the Young Generation Space. For hotspot VM, there are two kinds of GC:

* Partial GC
  * Minor GC/ Young GC: collect only on Eden, S0 S1. It will lead to STW. Minor GC runs frequently and fast.
  * Major GC/ Old GC: collect only on OG. When Major GC happens, it is often companioned by a Minor GC. Major GS is ususally 10x slow than Minor GC, which means longer STW. If memory is still insufficent after Major GC, the program will throw OOM.
  * Mixed GC: Collect on both YG and OG, only G1 GC do that.
* Full GC: collect on the whole java heap and method area. Avoid full gc in the optimization to have a better performance, since it is costy.

### Why separate the heap into different region

Separating the heap can improve the performance of Garbage Collection. Most objects in Java has short life cycle, if we don't separate the heap, GC will scan the whole heap every time, which is costy. By putting those transient objects into the Eden Space improve the efficiency significantly.

### Thread Local Allocation Buffer(TLAB)
The reason why we want buffer is reducing the need of synchronization between threads.
Heap is shared by threads, every thread can access the data in the heap. Objects are created frequently in jvm, and its not thread safe to assign a block of memory during the concurrent programming. To avoid conflict, we need to lock the memory when allocate, which will slow down the program. 

Hence, we have TLAB for each thread in the Eden Space. JVM will first try to create an object in the TLAB. TLAB will just occupied very small piece of memory(1% of Eden). If the object cannot be created in the TLAB, jvm will create it at Eden directly with synchroniztion.

`-XX:UseTLAB` the default value is true.
`-XX:TLABWasteTargetPercent` set the percentage

`jps: look up the pid`
`jinfo - flag SurvivorRatio <jpid>` look up some parameter.


### Escape Analysis

`-XX: +DoEscapeAnalysis` open the analysis
`-XX: +PrintEscapeAnalysis` to show the escape analysis

`-XX: +EliminateAllocations` to enable converting aggregate to the scalar

## Method Area

```java
Person person = new Person();
```

When initialize a variable, there is a reference in the stack(LV) pointing to an instance in the heap. The instance in the heap contains a pointer to the class data in the method area.