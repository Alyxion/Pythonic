# Creating namespace packages with Poetry

Imagine you have a large mono-repo named toolbox with submodules named `toolbox.images`,
`toolbox.database` and want to split this up into multiple, smaller projects in
different Git repositories while keeping their original import path such as
`from toolbox.images import Image`.

This demo shall give a brief overview of how to share the namespace between multiple
Python packages, either for your local projects or extendable Python packages you
want to publish on platforms such as PyPi.

## Running the demo

1. Install Python 3.8 or above
2. Open your terminal and go to the directory `goodbye`. Execute
    * `disable` in case you already are (e.g. through PyCharm) in a virtual env
    * `poetry env use python3.8` to select your Python version
    * `poetry build` to build the package
3. Do the same for the package `hello`
4. On success you should now find the corresponding wheels in `goodbye/dist` and
   `hello/dist` which you could (in theory) even publish individually as packages to
   PyPi. (please don't).
5. Go to `test_app`
    * `poetry lock` to update the hashes for your wheels
    * `poetry env use python3.8` to select your Python version
    * `poetry install` to install all dependencies (in this case the two wheels
      you just build)
    * Execute `poetry run python main.py` to test them

## What do I have to consider in difference to classical packages?

* In case of a simple package you want to bundle and/or publish on PyPi you would
  usually create a sub-folder named the same way as the package itself. See
  https://github.com/SciStag/SciStag/blob/v0.8.2/pyproject.toml where the package is
  named `name = "scistag"` and so is the name of the sub folder.
* Within the `scistag` folder or in case of your own package the folder named the
  same way as the package itself you would then create an `__init__.py` so that Poetry
  and Python also handle this folder like a module.

In case of **namespace packages** you have to declare the (effective) import path such
as follows:

```
packages = [
    { include = "myns/hello", from = "." }
]
```

and

```
packages = [
    { include = "myns/goodbye", from = "." }
]
```

## Naming the sub-package

A quite popuplar naming convention for the sub modules would be
`mainpackage-subpackage` such as `azure-core` or in our case `myns-goodbye` which
we declare in the Poetry file via

```
[tool.poetry]
name = "myns-goodbye"
```

## Files in the module's root directory

One major difference is that in difference to classical packages **you do not need**
an `__init__.py` in the main namespace's folder, so `myns` in our case though you
need one in the subpackage folders such as `goodbye` and `hello` in our case.<br>

Actually the `__init__.py` in `myns` were even ignored by the package config shown
above because both packages point directly into the `myns/hello` and `myns/goodbye`
folder so everything directly in `myns` is ignored.

If you need or want an `__init__.py` inside the main folder or e.g. a main entry point
for command line usage of your module such as `__main__.py` you though may import
such a file in addition:

```
packages = [
    { include = "myns/goodbye", from = "." },
    { include = "myns/__init__.py", from = "." }
]
```

And then you could also for example store the version in the `__init__.py` and do
something like `import myns; print(myns.__version__)`, but...

**The problem**: You could now do precisely the same in the package **hello** and also
add there an `__init__.py` file.<br>You could then build both packages without issues
and also install them both at the same time without any issues even though they contain
the same file `myns/__init__.py` actually competing for the same name in the
installation path.

So if you ask yourself: **Which __init__.py will be used then, the one from the
goodbye or the one from the sub_package?**

Well as it turns out pip and poetry just **merge the contents** of both packages into
one shared disk path such as

`/home/michael/.cache/pypoetry/virtualenvs/packagenamespaces-kiplBBmp-py3.8/lib/python3.8/site-packages/myns/goodbye`
and
`/home/michael/.cache/pypoetry/virtualenvs/packagenamespaces-kiplBBmp-py3.8/lib/python3.8/site-packages/myns/hello`

in the case of my demo.

And which of the both `__init__.py` versions will win now?

Short answer: **It's random**!
<br>They just overwrite each other in the same disk location in the order they are
installed.<br>So if you install **hello** first and then **goodbye** you would get the
version of **goodbye** and if you would install **hello** later you would get the
version of **hello**.<br>And in case you ever do something like `poetry update` you
can likely as well as throw the dice ;-).

Or with other words: **You should avoid storing and importing any files from within
the shared area of the namespace**.<br>And if you can not avoid it e.g. for some fancy
import magic or a main entry point for command line tools into your package please
be very careful.

## Questions? Suggestions?

Feel free to reach out to me at LinkedIn:
[Michael Ikemann](https://www.linkedin.com/in/michael-ikemann/)

## Try SciStag

The reason for my research about namespace packages was for a cleaner structuring of
my computer vision & data visualization tools package named
[SciStag](https://github.com/SciStag/SciStag).

Feel free to *star* it on GitHub, try it yourself and give me feedback:

* **PyPi**: https://pypi.org/project/scistag/
* **Demos**: https://github.com/SciStag/SciStag/tree/main/scistag/examples

# Thanks

Thanks to **Wei-Hung Pan** for his
original [article on Medium](https://n124080.medium.com/create-python-package-toolbox-using-poetry-namespace-bd7e6cbd4bf0)
on which I based my tests.