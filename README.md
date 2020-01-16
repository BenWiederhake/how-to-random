# how-to-random

> Shows you a "random" image from WikiHow.

This program downloads a random image from wikiHow, for your viewing pleasure.

Note that this tool gives you no more access or abilities than just browsing to the page https://www.wikihow.com/Special:Randomizer
Therefore, the resulting images may be copyrighted.

The following examples are all CC BY-NC-SA 3.0 with Wikivisual or Wikiphoto:

![Collage of 9 random WikiHow images](collage.jpg)

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Licensing](#licensing)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Install

The requirements can be found in `requirements.txt`, and can be installed like this:

```
$ pip3 install -r requirements.txt 
Requirement already satisfied: beautifulsoup4==4.8.2 in /usr/lib/python3/dist-packages (from -r requirements.txt (line 1)) (4.8.2)
Requirement already satisfied: requests==2.22.0 in /usr/lib/python3/dist-packages (from -r requirements.txt (line 2)) (2.22.0)
Requirement already satisfied: lxml==4.4.2 in /usr/lib/python3/dist-packages (from -r requirements.txt (line 3)) (4.4.2)
```

## Usage

Just call it!  It's written in python3, which basically everyone has, and has few dependencies.

Here's an example run:

```
$ ./how_to_random.py
Fetching base URL …
	Chose https://www.wikihow.com/Name-Chemical-Compounds
	Chose #3: /Image:Name-Chemical-Compounds-Step-4.jpg?ajax=true&aid=1286499
	Fetching image metadata …
	Fetching image itself …
Written to aid1286499-v4-900px-Name-Chemical-Compounds-Step-4.CC-BY-NC-SA-3.0.Wikiphoto.jpg
Copyright license seems to be CC BY-NC-SA 3.0 with Wikiphoto:
	https://creativecommons.org/licenses/by-nc-sa/3.0/
	https://www.wikihow.com/User:Wikiphoto
Have a great day!
```

There's also a way to use it in a pipeline:

```
$ ./how_to_random.py --output=json
{"choice":{"base":"https://www.wikihow.com/Become-a-New-Zealand-Citizen","base_index":16,"image_metadata":"https://www.wikihow.com/Image:Become-a-New-Zealand-Citizen-Step-17.jpg?ajax=true&aid=8005302"},"image":{"data_base64":"/9j/4AAQSkZJRgABAQEASABIAAD//gBURmlsZSBzb3VyY2U6IGh0dHA6…","url":"https://www.wikihow.com/images/thumb/1/1c/Become-a-New-Zealand-Citizen-Step-17.jpg/aid8005302-v4-900px-Become-a-New-Zealand-Citizen-Step-17.jpg"},"license":{"name":"CC BY-NC-SA 3.0","url":"https://creativecommons.org/licenses/by-nc-sa/3.0/"},"uploader":{"name":"Wikivisual","url":"https://www.wikihow.com/User:Wikivisual"}}
```

Or from a python program, if you copy it into your project:

```
import how_to_random

how_ro_random.gather(verbose=True)
```

## TODOs

* Do something meaningful with it?

## NOTDOs

Here are some things this project will definitely not support:
* "Fast" or "complete" crawling.
* Any kind of "guarantee" that the copyright parsing always succeeds (but it should be quite robust).
* Nicer output methods

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/how-to-random/issues/new) or submit PRs.
