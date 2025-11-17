# Activating Your Robot

Before controlling the robot we must perform several steps.

- Powering On the Robot
- Start hardware interface on the robot

## Powering On the Robot

Find the big red button and rotate it CCW until it pops out ~1/4 inch and clicks. This will provide power to the motors and lidar. Power to the computer (Jetson) is provided seperately by the rocker switch. Turn this on by pushing down on the side marked with a `|`.

[Add picture](!foo)

To check if the jetson is powered, open the vanity plate (the lid) and look for a green light on the computer.

[Add picture](!foo)

## Start hardware interface on the robot

Before the robot will respond to commands the hardware interface code _on the robot_ must be running. Fortunately this has been greatly simplified. We can star the hardware interface with two methods: A VSCode task or the shell.

### Start hardware interface with VSCode task

<details open>

If the "Fast Tasks" extension was installed then several buttons will be available in the "Explorer" pane which will automate the process of starting the robot.

<img src='./docs/images/start_robot_vsc.png' style="max-width:300;  height:auto;">


<div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div>


### Start hardware interface with shell

<details vscopt>
Rather than using the VSCode task we can manually invoke the shell/powershell scripts that connect to the robot.

For linux:

```bash
bash .scripts/start_robot.bash 192.168.33.<your_robot_num> prod
```

For windows:

```bash
.scripts/start_robot_windows 192.168.33.<your_robot_num> prod
```


<div style="max-width: 100%; overflow-x: auto;">
  <video controls style="width: 100%; height: auto;" poster="../_static/gifs/demo_preview.gif">
    <source src="../_static/videos/todo.webm" type="video/webm">
  </video>
</div>

