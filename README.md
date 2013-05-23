# 使用/Usage

在程序的第一行：   
In the first line of your source:

    from Briareus import patch; patch()
    
## 接口/Interfaces

全部使用注释，包括   
All interfaces are special comment, including

    # remote
    
    # async
    
    # parallelize
    
### `#remote`

使用 `#remote` 修饰的函数会分发到云平台上计算   
The functions marked by `#remote` will be migrating to cloud:

### `#async`

使用 `#async` 修饰的函数会被异步执行，其后的语句不等待该函数完成即开始执行，但保证需要使用函数返回值式函数已执行完成。   
A function marked by `#async` will be called in an asynchronous way. Following functions will be start do not need to wait for this function's finish.

### `#parallelize`

使用`#parallelize` 修饰的`for`循环、`map`调用和列表解析将会被并行执行（使用该注释修饰的循环假设没有数据依赖）。      
Any `for` loop, `map` loop and list comprehension marked by comment `#paralleliz` will be evaluated in parallel. BUT IT IS PROGRAMMERS' DUTIES TO MAKE SURE THE LOOPS CAN BE PARALLELIZED.
    
如果循环中有部分同时使用了`# remote`分发到云平台上计算，可以使用更复杂的形式：     
If there is any function that had been marked by comment `# remote`, there are more complex forms for `# parallelize` like,

    # parallelize with consts A, B and C
    
    # parallelize with cached R
    
这种情况下，`A`、`B`、`C`、`D`会被在云平台上缓存。（`A`、`B`、`C`和`D`需要是常量）      
In these examples, variants `A`, `B`, `C` and `D` will be cached un the cloud platform (assuming these variants are constant).

# 配置/Configuration

## 配置文件位置/Location of configuration files.

按顺序从以下位置读取配置文件，后一个位置配置文件中的项覆盖之前的配置      
Brareus read the configurations form below locations sequentially.

1. /etc/briareus.conf
2. ~/.briareus.conf
3. ./briareus.conf
    
 
## 配置文件格式/Format of configuration files

    {
        "host": "192.168.70.150",    #Address of cloud platform
        "port": 6379,                #Optional, port of Briareus
    }
    
# 示例/Examples

    # remote
    def foo(…):
        …
        
    foo()
    
`foo()`将分发到远程进行      
`foo()` will be migrated to remote cloud platform

    # async
    def foo1(…):
        …
        
    # async
    def foo2(…):
        …
        
    a = foo1(…)
    b = foo2(…)
    c = foo2(…)
    
    bar(a, b, c)
    
`a=foo1(…)`，`b=foo2(…)`和`c = foo2(…)`将并行（异步）进行，`bar(a,b,c)`则等待`a`、`b`、`c`的求值都完成之后再进行。      
`a=foo1(…)`，`b=foo2(…)` and `c = foo2(…)` will be evaluated at the same time, and the evaluation of `bar(a,b,c)` will be started after all of `a`, `b` and `c` being calculated.
    
    #parallelize
    for … in …:
        …
    
`for`循环将并行进行。      
The `for` loop will be evaluated in parallel.

    #remote
    def func(A):
        …
        
    #parallelize with cached a
    for … in …:
        …
        func(a)
        …
        
`for`循环将并行执行，其中`func(a)`将被（并行）分发到云平台执行，a会在云平台被缓存。      
The `for` loop will be evaluated in parallel, the evaluation of `func(q)` will be migrated to cloud, and const `a` will be cached in cloud.


    