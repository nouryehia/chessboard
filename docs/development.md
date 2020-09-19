---
layout: default
title: Chessboard
---
# Getting Started with Development

## PyCharm Debugger Setup
Follow the steps below to setup `chessboard` with a configuration to use Pycharm's Debug tool for Python, which allows you to set breakpoints, watch variables, etc.

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
5. Click on the folder icon add the end of the `Path Mappings` field to edit path mappings.
   ![](photos/pycharm_interpreter_path_mapping.png)
6. Click the `+` icon to add a new path mapping with the settings below and click `OK`. 
    1. NOTE: Replace `Local Path` with your path to `chessboard`.
   ![](photos/pycharm_interpreter_edit_path_mapping.png)
7. Your screen should look like step 3. If so, click `Apply` and `OK`.

#### Run/Debug Configuration Setup

Then we need to setup a Run/Debug Configuration for `chessboard` which "specifies details such as app installation, launch, and test options".

1. Click on the dropdown indicated below and select `Edit Configurations`.
    ![](photos/pycharm_edit_configurations.png)
2. Click the `+` icon and select `Python` to add a Python Run/Debug Configuration.
    ![](photos/pycharm_add_new_configuration.png)
3. Fill out the form with the settings below.
    1.  NOTE: Replace `Script Path` with your local path to `runner.py`.
    2.  NOTE: Replace `Working Directory` with your local path to `chessboard`.
	![](photos/pycharm_configuration.png)
4.  Click on the folder icon add the end of the `Path Mappings` field to edit path mappings.
5. Click the `+` icon to add a new path mapping with the settings below and click `OK`. 
    1. NOTE: Replace `Local Path` with your path to `chessboard`. 
	![](photos/pycharm_configuration_path_mapping.png)
6. Your screen should look like step 3. If so, click `Apply` and `OK`.

## Using the Debugger
Check out [this link](https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html#breakpoints) to learn how to use Pycharm's Debug tool.

1. Set breakpoints by clicking in the margin on the left side of a line number. You should see a red dot next to the line.
2. Start a debug session by clicking the debug icon. Your docker image should build.
    ![](photos/pycharm_debug.png)
3. Stop a debug session by typing in `docker-compose down --volumes` in your terminal or clicking the stop icon.
    ![](photos/pycharm_stop.png)
4. Here's an example of a running debug session!
    ![](photos/pycharm_set_breakpoint.png) 

Happy debugging!! :)
   
---
[Go back](/chessboard)
