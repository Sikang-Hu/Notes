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
* Additional information

#### Local Variables
An array of int to store parameters and local variables, can store primitive, reference and returnAddress. The size of the local variables is determined when compiled. Slot is the smallest unit in local variables table. Data type within 32bits takes one slot, while 64bits(long, double) data type takes two slot.

If current frame is created by constructor or instance method, the reference to this object will be put at index 0, and the rest will be arrange by their declaration sequence. The slot can be reused if a local variable's field ends(e.g. for loop or if block ends).

When the method ends, the local variables table will also be destroyed.

The local variable is the most related part in jvm optimization in the stack frame.