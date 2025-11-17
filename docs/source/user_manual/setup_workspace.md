# Setting Up Your Workspace
This document will help you setup your personal computer to control the SmartBots

```{contents} Table of Contents
:depth: 3
```

## Clone the repo using git

Clone this repo with the following command (note the --recursive flag!):

```bash
git clone --recursive https://github.com/wvu-irl/smartbot3_project_template
```

This repo includes _another repo_ `smartbot_irl` which is a python package used to control the IRL SmartBot.
See the following gif for details if you are confused.
<div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/win_clone_repo.webm" type="video/webm">
  </video>
</div>

## Open the `smartbot3_project_template` folder in VSCode

Now, let's open VSCode to the directory for the reop we have just cloned. **When prompted to install recommended extensions, click yes**. See the following gif for details if you are confused.
<div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/win_vsc_extensions_open.webm" type="video/webm">
  </video>
</div>

## Install workspace recommended extensions

If the prompt to install recommended extensions did not appear or if you want to check for newly added recommended extensions you can search for `@recommended` in the "Extensions" menu. To download all recommended extensions click the small download button under the search bar.
<img src='../_static/images/vsc_ext_download.png' style="max-width:800;  height:auto;">

## Open a VSCode terminal (shell)

This can be done by going to the menu `View->Terminal`. Alternatively the keymap `` Ctrl-`  `` will toggle the terminal pane open/closed.

We can have VSC open a variety of shells. On windows we can select from gitbash, CMD, and powershell. You may do this by clicking on the small down arrow at the top of the terminal pane.
<img src='./_static/images/vsc_new_shell.png' style="max-width:800;  height:auto;">

We can make additional terminal windows here if desired. Alternatively, the keymap `` Ctrl-Shift-`  `` will also do this.

<img src='./_static/images/vsc_new_shell2.png' style="max-width:800;  height:auto;">

## Create a python virtual environment (venv)

> **Note**: Windows makes using python and venvs more cumbersome. Instructions
> found online will be primarily aimed at Linux and may not work for windows.

Before we can can use the `smartbot_irl` package to send and receive data from
the SmartBot we must make it importable for our python code.

We will use a python [virtual environment](https://peps.python.org/pep-0405/) in
our project so that we can more easily manage python dependencies. There are two
options for creating and manage venvs: Shell commands and VSCodes built in
tools. Both are shown here.

### Linux Venv

<details linux>

</details linux>

### Windows Venv

<details open>

### Option 1: Setting up a venv using the shell

> Make sure to run the following commands from inside the top level of the `smartbot3_project_template` you cloned!

To create a python3.12 venv in a directory named `.venv` use the command:

```bash
python3.12 -m venv .venv
```

<details >
    <summary>See the following gif for details if you are confused.</summary>
<img src='./docs/gifs/win_venv_install.gif' style="max-width:700;  height:auto;">
</details>
<br>

Then install python dependencies using `pip.exe` inside of the `.venv` directory:

```bash
.venv/Scripts/pip.exe install -r requirements.txt
```

<details>
    <summary>See the following gif for details if you are confused.</summary>
<img src='./docs/gifs/win_venv_req_install.gif' style="max-width:700;  height:auto;">
</details>
<br>

Then install the `smartbot_irl` package using:

```bash
.venv/Scripts/pip.exe install -e smartbot_irl
```

<details>
    <summary>See the following gif for details if you are confused.</summary>
<img src='./docs/gifs/win_venv_smartbot_install.gif' style="max-width:700;  height:auto;">
</details>

### Option 2: Setting up a venv using VSCode

<details vscopt>
</details vscopt>

</details win>