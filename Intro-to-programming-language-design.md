As a starting point, you should consult some [[books]] on programming language design and implementation.
We are not going to rewrite the whole [[Dragon Book|http://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools]] here, but :warning: this tutorial can be [[Susanin|https://en.wikipedia.org/wiki/Ivan_Susanin]] will astray you into compilers design, be warned :smile_cat: 

### Typical compiler structure

Modern compilers use modular structure to be portable and easy retargetable for new languages to be compiled and new platforms it should support:
1. **frontend** for the specific programming language
* (optional) preprocessor
* syntax parser
* semantic analysis, type inference, programming rules checker (LINT)
* intermediate representation (IR) machine independent optimizer stages
2. **backend** targets to machine architecture on which program must run
* target code generator and machine level optimization
* object code tools: linker, library manager,..

![](https://compilerdesign.files.wordpress.com/2012/03/topic4notesimage3.jpg)

Compiler splitting into frontend and backend let us share parts of compiler between different programming languages, optimizers, and target platforms. For example, you can write a frontend for the language you designed yourself, and leave the whole hell of compiler implementation to production ready systems like Java and .NET runtimes, LLVM compiler framework, or some virtual machine (VM) able to execute code in IR form. In this tutorial, we will use Python2.7 as runtime system.

### Compiler vs Interpreter

Factically *compiler* and *interpreter* are **orthogonal** terms. Both are software modules that 

* *compiler* takes program in some representation and **transforms** it into other (more low-level) representation
* *interpreter* **executes** program in some representation *programmatically* (interprets it)

*Modern **interpreters** mostly **include** special sort of **compiler***: JIT, which **transforms** IR program representation into machine code directly into RAM to speed up program execution and link it with external platform libraries.

And **all interpreters** during its entire history **contains** another sort of **compiler** that compiles source code into some much or less *low level but platform-independent form*. Typically this IR is [[bytecode]], Lisp systems use lists, Forth use [[threaded code]], and so on. [[AST]]-like trees used very rarely and **source code can't be ever interpreted** as you can read it in a lot of books.

And finally, *interpreters have a key feature* in which we are very interested: **only interpreter able to implement dynamic languages**. In turn, [[dynamic language]] let us build very flexible software systems, as we can 
* change any part of a program *in runtime*,  
* debug and optimize it via tracking on real data, and
* get the power of [[transformational programming|http://en.wikipedia.org/wiki/Program_transformation]] techniques.
