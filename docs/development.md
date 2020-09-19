---
layout: default
title: Chessboard
---
# Getting Started with Development

## PyCharm Debugger Setup

Follow the steps below to setup `chessboard` with a configuration to use Pycharm's Debug tool for Python, which allows you to set breakpoints, watch variables, etc.

Check out [this link](https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html#breakpoints) to learn how to use Pycharm's Debug tool.


#### Installing Pycharm

1. Make sure you have the [JetBrains Product Pack for Students](https://www.jetbrains.com/community/education/#students).
2. Download the Professional version of [PyCharm 2020.2.2](https://www.jetbrains.com/pycharm/download/#section=mac). (Older versions may not work!)
3. Follow the installation steps for PyCharm.
4. Open the `chessboard` directory in PyCharm.

#### Interpreter Setup

First, we need to setup the Python Interpreter to use the Docker Image set up on starting the project.

1. Select `Pycharm` &rarr; `Preferences`.
   ![](photos/pycharm_preferences.png) 
2. Select `Project:chessboard` &rarr; `Python Interpreter`.
3. Click the gear icon and select `Add`.
   ![](photos/pycharm_interpreter.png)
4. Fill out the form with the settings below for the interpreter and click `OK`.
   ![](photos/pycharm_interpreter_add.png)
5. Click on the folder icon to edit path mappings.
   ![](photos/pycharm_interpreter_path_mapping.png)
6. Click the `+` icon to add a new path mapping with the settings below and click OK. 
   1. NOTE: Replace the left path with your path to `chessboard`.
   ![](photos/pycharm_interpreter_edit_path_mapping.png)
7. Click `Apply` and `OK`.

#### Run/Debug Configuration Setup
   
---
[Go back](/chessboard)
