# Download
I will provide instructions for running the software on linux. For windows users, the use of wsl is recommended.

First of all, it is necessary to download the script using the command `git clone https://github.com/LoZack19/ultimate_library_toolkit`. Once this is done, you will need to download the dependencies necessary to make the script work. To do this, enter the downloaded folder with `cd ultimante_library_toolkit` and simply type `pip install -r "requirements.txt"`. At this point the software is ready to run. To test whether the operation was successful, you can run the test script `script.py`. If everything has worked properly you should see a graph on your screen representing approximate CCL activity over time.

# Scripting
The advantage of this new software is to allow users to easily write their own scripts, using commands implemented as methods of the `Shell` class. To write your own script, you need to know the syntax by which these commands are to be used, and the main commands that are useful for doing most of the work.

## Basics
The fundamental object around which the program revolves is the `Shell`, which is a collection of libraries. Libraries are lists that contain a number of works. At startup the program knows only the special `general` library, which contains all the works contained in the initialization file. The initialization file can be modified from the `config.yaml` configuration file, but at first it will not be necessary to do so.

Commands are invoked with the syntax:

```python
sh.command(arg1 = val1, arg2 = val2, ..., argn = valn)
```

Note that the order in which the function arguments are listed is not important, since each is identified by its name.

These topics almost always include an input library (inlib) from which to read the works, and an output library (outlib) where to go to store the result of the operation performed on the input library. Let us imagine, for example, that we want to select all the works of Salvatore Giordano from the `general` library and store them in a new `giordano` library. We will do as follows:

```python
sh.select(inlib = "general", field = "author", arg = "Salvatore Giordano", outlib = "giordano")
```

Commands can also be invoked by exploiting the natural ordering of arguments, without explicitly specifying their names. In this case the order in which the arguments are specified is important, since they are not indentified by name.

```python
sh.select("general", "author", "Salvatore Giordano", "giordano")
```

## Commands

### Select and Discard
```
sh.select(inlib, field, arg, outlib, extra)
```

It selects all works in the `inlib` library that have `arg` as the value of the `field` field, and puts them in a library called `outlib`.

Possible field values are: `author`, `nation`, `place`, `title`, `date`, and even `link`, although the most useful are the first three.

The select command also includes the optional `extra` argument that allows selection based on more precise criteria, such as the domain of the link. If we wanted to select works based on the domain on which they are saved, we would have to add among the arguments `extra = 'domain'`. By default it holds `None` and it has no effect not to specify it.

```
sh.discard(inlib, field, arg, outlib, extra)
```

Identical to `sh.select`, but instead of selecting works from the `inlib` library, it selects the only works from `inlib` that will not go into outlib.

```
sh.time_range(inlib, time_range, outlib)
```

It selects the `inlib` jobs that are between `time_range[0]` and `time_range[1]`, and puts them in `outlib`.

`time_range` is a tuple of dates in `datetime` format. To use `time_range` correctly, one must know how to use tuples and the `datetime` object.

### Operations with libraries

It is possible to merge, intersect and complement libraries.

```
sh.and_(inlib1, inlib2, outlib)
sh.or_(inlib1, inlib2, outlib)
sh.not_(inlib, outlib, universe)
```

The and intersects the two `inlib` libraries and puts the result in `outlib`. The or joins the two `inlib` libraries and puts the result in `outlib`.

The not takes as input a library called `universe`, and a subset of it called `inlib`, and puts in `outlib` all the works that are in `universe` but not in `inlib`. So it performs the complement of `inlib` with respect to `universe`.

### Managing the libraries

```
sh.list_()
sh.del_(lib)
```

The list operation is used to list all the libraries currently in use, each accompanied by the number of works they contain. In contrast, the del operation permanently deletes a library from among those listed.

### Displaying info

```
sh.print_(inlib)
sh.stat(inlib, field, opt)
```

There are three operations for showing general information about a library. These operations are print, stat, and plot. The plotting operation is sufficiently complex to merit its own paragraph.

Print takes as input a library and prints all its works in BSL format. Stat, on the other hand, takes as input a library and a field (e.g., `author`) and lists how many occurrences of each value exist for that field (e.g., lists how many works each author wrote in the particular library specified). Values are listed in order with respect to the frequency with which they appear.

Stat shows numerical statistics on the specified library works related to the specified field. The `field` parameter can be accompanied by the optional `opt` specifier, which, as with `extra` in `select`, allows us to specify for a complex field what we specifically want to search for. For example if the field is `link` and we put `opt = 'domain'` the statistics provided will be about the domains used.

### Saving and loading

After hard selection work, it might be useful to save a library to a file so that it can be easily reloaded into the program for later use. This can be done with the save and load commands.

```
sh.save(filename, inlib)
sh.load(filename, outlib)
```

### Plot

One of the most useful and complex features of the program is the plot function. The latter allows one to temporally plot the distribution of works in a library over time, even in an approximate manner. This makes it easier to make judgments about the cultural activity of a particular place or historical period. With the approximate plot feature, it is also easy to identify the minima and maxima of the activity curve. Let us now see how to take advantage of the plot's main features.

It is recommended to use this function by making the names of the arguments explicit. It is not necessary to assign a value to each argument. In fact, should you not do so, default values will be assigned.

```
sh.plot(inlib,
        deg
        plabels
        pticks
        div
        show
        color)
```

Basically, the plot function graphs the distribution of works in the `inlib` library over time.

If the parameter `deg` is specified, it can be an integer greater than zero that expresses the accuracy with which the approximation will recalculate the original data. It is recommended not to go outside the range of numbers between one and ten. By default, the parameter has value `-1`, which indicates that no approximation is used.

The `plabels` argument indicates in what style the values on the x-axis should be represented. By default it is set to `pretty`, which means that the values are to be represented as dates. Any other value indicates that the representation will be by integer offsets from an initial date.

The `pticks` argument indicates with what spacing the labels should be inserted on the x-axis. Two possible values are `equispaced` and `minmax`. `equispaced` inserts the labels at regular spacing from each other. The distance is adjusted by the `div` parameter, which by default is set to 15. `minmax` places the labels at the critical points of the curve. It can be employed only if an approximation has been used.

The `show` parameter is an advanced parameter. Setting it to `False` allows you to accumulate multiple graphs in memory, which will all be shown at the same time on the first call of the plot command where `show` will be set to `True`.

`color` allows you to specify the color of the graph. To use it, you need to know the color syntax of the `pyplot` module.