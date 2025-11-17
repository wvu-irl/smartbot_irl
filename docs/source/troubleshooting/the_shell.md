# I am Confused and Angry About Typing Commands

`¯\_(ツ)_/¯`

## The Text Shell

A shell is any program you use to interface with a computer. A **text shell**
is, as the name implies, a text-only computer interface. Other common names are
"command prompt", "terminal", "tty". A common shell in linux is `Bash`, windows
has powershell and CMD. A **graphical shell** is how computers are most commonly
used today (buttons, windows, mouse cursor, etc).

Graphical shells are easy to learn and can be very effective. However, for the
shallow learning curve and high abstractness of a graphical shell we pay a
price. In a graphical shell if is no button or menu for what we want to do, _we
simply cannot do it_. A text shell will give you the freedom to do as you please
on your own terms provided you are willing to struggle.

Text shells are hard to learn in the same way language is hard to learn. There
is some upfront memorization necessary before you can do/say anything
non-trivial. Very quickly learning transitions away from memorization and
becomes exploration, play.

Eventually, rather than invoking the base set of commands as monosyllabic sentences
([holophrastics](https://en.wikipedia.org/wiki/Holophrasis)) you compose them.
This is not just a matter of efficiency but of being able to say entirely new
things. For example,

> "How many lines of text are there in all the python files in the current
> directory?"

becomes,

```sh
wc -l *.py
```

This is where the real power of a text interface arises. The translation of
human desire to a sequence of characters is less arcane when viewed through the
lens of sentence formation.

But just like "go", "to", and "hi" never stop being useful in human language the
base commands `cd`, `ls`, `du`, etc never stop being useful in the shell.
Fortunately the actions we need to learn how to do in the shell are relatively
few and we can quickly memorize the commands we will be repeating most often.

## The Prompt

Shells have many different forms of "prompts". A prompt is a metaphorical object where you provide your input and where additional details may be presented. Commonly the prompt will show your username along with the **current working directory** (i.e. where you are in the filesystem). This is important as the behaviour of many commands depends on _where they are run_.

```bash
username@hostname:directory$
```

Often we give **file paths** to a command and this will be affected by where the command and file path are ran.

## Copying Command Examples

Angle brackets `<>` will be used to denote an argument that is mandatory. The string inside the brackets is semantically desriptive. Do not type the brackets when actually writing the command.

```bash
cd <path/to/dir>
```

will become something like,

```bash
cd src/
```

<br>

Square brackets `[ ]` are often used to indicate optional arguments and should be interpreted the same as angle brackets otherwise.

## Further Reading:

- https://linuxjourney.com/lesson/the-shell
- [In the Beginning... Was the Command Line](https://web.stanford.edu/class/cs81n/command.txt)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
- https://cheat.sh/
- https://devhints.io/bash
- https://en.wikipedia.org/wiki/Everything_is_a_fil