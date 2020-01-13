# how-to-random

> Shows you a "random" image from wikiHow.

This program downloads a random image from wikiHow, for your viewing pleasure.

Note that this tool gives you no more access or abilities than just browsing to the page https://www.wikihow.com/Special:Randomizer
Therefore, the resulting images may be copyrighted.

## Table of Contents

- [Usage](#usage)
- [Licensing](#licensing)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Usage

Just use it!  It's written in python3, which basically everyone has, and has no additional dependencies.

Here's an example run:

```
$ ./how_to_random.py
Fetching page ... chose Become-a-Reflexologist
Fetching image ... chose Step 3
Written to aid1353564-v4-900px-Become-a-Reflexologist-Step-3-Version-2_by-nc-sa-3.0_Wikivisual.jpg
Copyright seems to be CC-BY-NC-3.0 with Wikivisual
  https://creativecommons.org/licenses/by-nc-sa/3.0/
  https://www.wikihow.com/User:Wikivisual
Have a great day!
```

There's also a way to use it in a pipeline:

```
$ ./how_to_random.py --pipe-out
{"title": "Become-a-Reflexologist", "image": {"filename": "aid1353564-v4-900px-Become-a-Reflexologist-Step-3-Version-2_by-nc-sa-3.0_Wikivisual.jpg", "copyright": "Wikivisual", "data_base64": "/9j/4AAQSkZJRgABAQEASABIAAD//gBXRmlsZSBzb3VyY2U6IGh0dHA6Ly93d3cud2lraWhvdy5j…"}}
```

Or from a python program, if you copy it into your project:

```
import how_to_random

how_ro_random.fetch_stuff()  # TODO
```

## TODOs

* Implement it

## NOTDOs

Here are some things this project will definitely not support:
* "Fast" or "complete" crawling.
* Any kind of "guarantee" that the copyright parsing always succeeds (but it should be quite robust).
* Nicer output methods

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/how-to-random/issues/new) or submit PRs.
