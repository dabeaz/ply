As a starting point, you should consult some [[books]] on programming language design and implementation.
We are not going to rewrite the whole [[Dragon Book|http://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools]] here, but :warning: this tutorial can be [[Susanin|https://en.wikipedia.org/wiki/Ivan_Susanin]] will astray you into compilers design, be warned :smile_cat: 

## Typical compiler structure

Modern compilers use modular structure to be portable and easy retargetable for new languages to be compiled and new platforms it should support:
1. (optional) preprocessor
1. **frontend** for the specific programming language
1. intermediate representation (IR) optimizer stages
1. **backend** targets to machine architecture on which program must run
1. target code generator and machine level optimization
1. object code tools: linker, library manager,..

![](https://compilerdesign.files.wordpress.com/2012/03/topic4notesimage3.jpg)

Compiler splitting into frontend and backend let us share parts of compiler between different programming languages, optimizers, and target platforms. For example, you can write a frontend for the language you designed yourself, and leave the whole hell of compiler implementation to production ready systems like Java or .NET runtimes.