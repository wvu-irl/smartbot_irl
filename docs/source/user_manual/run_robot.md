# Running the Robot
Once we have our workspace setup and dependencies installed we are ready to make the robot do something!

```{contents} Table of Contents
:depth: 3
```

:::{warning}
Starting and stopping the robots using VSC tasks is currently broken for windows. Try running the linux `bash` commands in gitbash for windows.
:::

## Start hardware interface on the robot

Before the robot will respond to commands the hardware interface code _on the robot_ must be running. Fortunately this has been greatly simplified. We can start the hardware interface with two methods: A VSCode task or the shell.

### Start hardware interface with VSCode task


If the "Fast Tasks" extension was installed then several buttons will be available in the "Explorer" pane which will automate the process of starting the robot.

<img src='../_static/images/start_robot_vsc.png' style="max-width:300;  height:auto;">

TODO Video
<!-- <div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div> -->


### Start hardware interface with shell

Rather than using the VSCode task we can manually invoke the shell/powershell scripts that connect to the robot.

For linux:

```bash
bash .scripts/start_robot.bash 192.168.33.<your_robot_num> prod
```

For windows:

```bash
.scripts/start_robot_windows 192.168.33.<your_robot_num> prod
```

TODO Video
<!-- <div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div> -->



## Stop hardware interface on the robot

Before the robot will respond to commands the hardware interface code _on the robot_ must be running. Fortunately this has been greatly simplified. We can start the hardware interface with two methods: A VSCode task or the shell.

### Stop hardware interface with VSCode task

Same as starting but now it's stopping.

<img src='../_static/images/stop_robot_vsc.png' style="max-width:300;  height:auto;">

TODO Video
<!-- <div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div> -->


### Stop hardware interface with shell

For linux:

```bash
bash .scripts/stop_robot.bash 192.168.33.<your_robot_num> prod
```

For windows:

```bash
.scripts/stop_robot_windows 192.168.33.<your_robot_num> prod
```

TODO Video
<!-- <div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div> -->
