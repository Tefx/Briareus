
**This is only a prototype project and it is not suitable for production environments!**

**This document is to show you what Briareus can do, but not how to use it. If you are going to use Briareus, please contact me (zhaomeng.zhu@gmail.com) for more details. Thank you!**

# About

Briareus aims to speed up python applications using distributed platforms like Cloud. It can automatically parallelize loops (including the `for` loops, list comprehensions and the `map` function), making functions asynchronous, or migrate functions to be evaluated in remote servers. To achieve these goals, only minimal modifications of the source code is needed.

This repo only contains the code related to the interfaces and code transformations. The distributed framework used and the task queue are in [Corellia](https://github.com/Tefx/Corellia), and the serialization part is in [Husky](https://github.com/Tefx/Husky).

# Installation and deployment

Please contact me via zhaomeng.zhu@gmail.com

# Features

To use Briareus, a patch in the first line of the source file (the `__main__` file) is required:

    from Briareus import patch; patch()

This monkey patch will release the power of Briareus!

There are three operations provided by Briareus, and all of them are enabled by comments:

    # remote
    # async
    # parallelize

*Why we use comments?*

*Because by this way, the behavior of the program will not be changed if `patch()` is not applied, or if the target platforms is not available.*


The `# remote` makes a following function's evaluations be migrated to remote servers. For example,

    from Briareus import patch; patch()

    # remote
    def foo(a, b):
      return a+b

    print "1+2=%d" % foo(1,2)

Here, the evaluation of `1+2` will be calculated in a pre-configured remote server. However, the other part of the program still run locally.

The `# async` makes a following function asynchronous. For example,

    from Briareus import patch; patch()

    # async
    def foo1(...):
        ...
        ...

    a = foo1(...)
    b = foo1(...)

    bar(a, b)


Here, the evaluation of `b` starts without waiting for the finish of the evaluation of `a`. However, `bar(a,b)` will not start until both the evaluations of `a` and `b` has finished.

Of course, this comment can be used together with `# remote`:

    from Briareus import patch; patch()

    # async
    # remote
    def foo1(...):
        ...

    # async
    # remote
    def foo2(...):
        ...

    a = foo1(...)
    b = foo2(...)

    bar(a, b)

Now, `a` and `b` is evaluated simultaneously in the configured distributed environment!

Finally, `# parallelize` parallelizes a following `for` loop, `map` invocation and *list comprehension*:

    from Briareus import patch; patch()

    # paralleliz
    for a in l:
        do_something(a)

    # paralleliz
    for a,b,c in l:
        do_something(a)
        do_other_thing(b,c)

    # paralleliz
    for a in l0:
        for b in l1:
            for c in l2:
                do_something(a,b,c)

    # parallelize
    after = map(foo, l)

    # parallelize
    new_list = [x*2 for x in l if x > 0]

    # parallelize
    new_list2 = [x*y+z for x in l0 if x>0 \
                       for y in l1 if y>0 \
                       for z in l3]

All of the above loops are parallelized!


Now, combine the use of `# remote` and `# parallelize` in a real-world example implementing the OMP algorithm:

    from Briareus import patch; patch()
    import numpy as np
    from scipy
    import sparse

    # remote
    def OMP(s, T, N):
        body_of_OMP

    def recovery_image(a, b, Y, R, ww):
        X = np.zeros((a, b))

        # parallelize with const R
        for i in xrange(b):
            X[:,i] = OMP(Y[:,i].reshape((-1,1)), R, a)
            X1 = ww.H * sparse.csr_matrix(X) * ww

        return X1.toarray()

    if __name__ == "__main__":
        a, b, Y, R, ww, original =
        perpare_image()
        recovered = recovery_image(a, b, Y, R, ww, original)
        errorx = (np.absolute(recovered - original) ** 2).sum()
        psnr = 10 * np.log10(255 * 255 / (errorx / a / b))

        return psnr

Great! The algorithm has been parallelized in a distributed environment!

You may notice that here we use a slightly different comment `# paralleliz with const R`. This comment distributes and caches the large variable `R` in distributed workers. Of course, there can be more than one cached variables:

    # parallelize with const a

    # parallelize with const a, b, c

    # parallelize with const a, b and c

or, if you like,

    # parallelize with cached a

    # parallelize with cached a, b, c

    # parallelize with cached a, b and c
