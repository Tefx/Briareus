# 使用

在程序的第一行：

    from Briareus import patch; patch()
    
## 接口

全部使用注释，包括

    # remote
    
    # async
    
    # parallelize
    
### `#remote`

使用 `#remote` 修饰的函数会分发到云平台上计算

### `#async`

使用 `#async` 修饰的函数会被异步执行，其后的语句不等待该函数完成即开始执行，但保证需要使用函数返回值式函数已执行完成。

### `#parallelize`

使用`#parallelize` 修饰的`for`循环、`map`调用和列表解析将会被并行执行（使用该注释修饰的循环假设没有数据依赖）。
    
如果循环中有部分同时使用了`# remote`分发到云平台上计算，可以使用更复杂的形式：

    # parallelize with consts A, B and C
    
    # parallelize with cached R
    
这种情况下，`A`、`B`、`C`、`D`会被在云平台上缓存。（`A`、`B`、`C`和`D`需要是常量）

# 配置

## 配置文件位置

按顺序从以下位置读取配置文件，后一个位置配置文件中的项覆盖之前的配置

1. /etc/briareus.conf
2. ~/.briareus.conf
3. ./briareus.conf
    
 
## 配置文件格式
    {
        "host": "192.168.70.150",    #云平台地址
        "port": 6379,                #可选，云平台端口
        "queue_name": "Runtime",     #可选，云平台队列名称
    }
    
# 示例

    # remote
    def foo(…):
        …
        
    foo()
    
`foo()`将分发到远程进行

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
    
    #parallelize
    for … in …:
        …
    
`for`循环将并行进行。

    #remote
    def func(A):
        …
        
    #parallelize with cached a
    for … in …:
        …
        func(a)
        …
        
`for`循环将并行执行，其中`func(a)`将被（并行）分发到云平台执行，a会在云平台被缓存。


    