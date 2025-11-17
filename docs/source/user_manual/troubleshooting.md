# Troubleshooting

```{contents} Table of Contents
:depth: 3
```

## The dir `smartbot_irl` is empty!

Try running the following inside of your project repo

```bash
git submodule update --init --recursive
```

## Updating smartbot_irl

The directory named smartbot*irl inside of your project directory is itself a
git repo and is called a \_git submodule*. To update/reset the contents of the
smartbot_irl package you can run the following command insode of your repo:

```
git -C smartbot_irl reset --hard main
git submodule update --checkout --recursive -f
```

## I Can't Get Lidar or Move the Robot!

Check the E-Stop button is off (meaning the lidar+motors have power)! When the
E-stop is activated power is cut to the robot motors and lidar but the computer
will still receive power (if the toggle switch is on).

Another common problem is low voltage causing the lidar to stop spinning. Check if you can hear the lidar and if the battery is low.

## Updating The Template Repo

If you want to pull changes made to the template repo (not the smartbot_irl repo). Run the following in the project template directory.

```bash
git pull
```
