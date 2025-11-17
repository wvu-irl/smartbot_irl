# Running Code

> Before running code we must [activate the robot](#activating-robot)!

There are a few demo programs included in `src/`. You should add your scripts here as well. Let's try and run the teleop example. If we open it in the editor we can click the small "Play" button at the top right. If our venv is created correctly and we have installed all the dependencies a PyGame window should appear. Arrow keys will move the robot. The `PGUP/PGDOWN` keys will open/close the gripper. The keys `b/n/m` will cycle the arm through the DOWN/STOW/HOLD positions.

You may also run the script from the shell with:
```bash
python3.12 src/demo_teleop.py
```
<details>
<summary>windows</summary>

```bash
.venv/Scripts/python.exe src/demo_teleop.py
```
</details>

<details open>
    <summary>See the following gif for details if you are confused.</summary>
<img src='./docs/gifs/start_teleop.gif' alt="TODO" style="max-width:700;  height:auto;">

To cycle through shell history the UP/DOWN arrow keys can be used.

## Running in sim/real

To change between a simulated and real robot modify the "mode" string to be "real"|"sim". To choose which real robot you are connecting to specify its IP address in the `SmartBot.init()` method.

```py
    # For SmartBot2.
    bot = SmartBot(mode="real", drawing=True, smartbot_num=2)
    bot.init(host="192.168.28.254", port=9090, yaml_path="default_conf.yml")

    # For a simulated SmartBot
    # bot = SmartBot(mode="sim", drawing=True, smartbot_num=3)
    # bot.init(drawing=True, smartbot_num=3)
```

<details>
    <summary>See the following gif for details if you are confused.</summary>
<img src='docs/gifs/smartbot_real_run.gif' alt="TODO" style="max-width:700;  height:auto;">
</details>

# Using `smartbot_irl`

The main classes in the `smartbot_irl` package are `SensorData`, `Command`, and
`SmartBot`. In the example scripts we create an instance `bot` from the
`SmartBot` class. This `SmartBot` instance `bot` has the _methods(A.K.A
functions)_ `SmartBot.read()`, `SmartBot.write()`, and `SmartBot.spin()`. For
the `bot` instance of `SmartBot` you will call these functions like so:

```py
def step()
bot=SmartBot()
# The following would go in the step() function.
my_sensor_data = bot.read()
# Your algorithm here
my_command = Command(
    linear_vel = 0.3, # Move forward at 0.3m/s
    angular_vel=0.4, # Rotate CCW
    gripper_closed=True, # Close the gripper.
)
bot.write(my_command)
```

## The step() Function
This is where all your code should go. The `step()` function is called repeatedly until shutdown by the `main()` function. The `step()` function has a number of parameters passed in when it is called.

## Example Program
You can have your code mirror the following structure:

```py
```

## Sending Commands
To send commands we use `SmartBot.write()`

**Note**: We *do not* actually call `write()` like `SmartBot.write()`. Instead what this is communicating is the full name of the `write()` function which is a method of the `SmartBot` class. What this means is that we can call `write()` on any object which is of the *type* `SmartBot`. To illustrate:
```py
# `bot` is an object of type `SmartBot`.
bot = SmartBot(mode="real", drawing=True, smartbot_num=8)
# `bot` inherits the functions(methods) of its type (i.e. SmartBot).
bot.init(host="192.168.33.8", port=9090, yaml_path="default_conf.yml")
bot.write()
```

It is conceivable that you could make multiple `SmartBot` type objects to control multiple robots simultaneously. If you try this you get a gold sticker.
```py
# `bot` is an object of type `SmartBot`.
bot2 = SmartBot(mode="real", drawing=True, smartbot_num=2)
bot3 = SmartBot(mode="real", drawing=True, smartbot_num=3)
# `bot` inherits the functions(methods) of its type (i.e. SmartBot).
bot2.init(host="192.168.33.2", port=9090, yaml_path="default_conf.yml")
bot3.init(host="192.168.33.3", port=9090, yaml_path="default_conf.yml")
```

## Reading Sensor Data
To read sensor data we use `SmartBot.read()`. This is called in a similar way to `SmartBot.cmd()` but it accepts no arguments. It returns an object of type `smartbot_irl.data.SensorData`

```py
    sensors = bot.read()

```

## Using Parameters
The example scripts provides a class called `Params` where you can define parameters and their values. This is useful for values that don't change (e.g. dimensions or PID terms). This simplifies accessing parameter values so that it may be done as follows:

```py
def step(bot: SmartBotType, params: Params, states: State) -> None:
    t = time()

    state_prev = states.last # Get previous steps state vector.
    t_prev = state_prev.t_epoch # The previous steps timestamp.

    # New row vector to append to our states matrix.
    state_now = {
        "t_epoch": t,  # Seconds since Jan 1 1970.
        "t_delta": t - t_prev,  # Seconds since last time step.
        "t_elapsed": t - params.t0,  # Seconds since program start.
    }
    if state_now.t_elapsed > params.time_per_side:
        # do something
        ...
```

## Using State Data
The `States` object acts like a giant matrix. Columns are for specific variables and rows are time indices (integer count).

```py
def step(bot: SmartBotType, params: Params, states: State) -> None:
    t = time()

    state_prev = states.last # Get previous steps state vector.
    t_prev = state_prev.t_epoch # The previous steps timestamp.

    # New row vector to append to our states matrix.
    state_now = {
        "t_epoch": t,  # Seconds since Jan 1 1970.
        "t_delta": t - t_prev,  # Seconds since last time step.
        "t_elapsed": t - params.t0,  # Seconds since program start.
    }

    sensors = bot.read()

    # Let's add the sum of the IMU acceleration data as a new column.
    imu_sum = sensors.imu.ax + sensors.imu.ay + sensors.imu.az
    state_now['my_column'] = imu_sum

    # And add to the end of our state matrix.
    states.append_row(state_now)

```

## Using SmartLogger to Print
A good alternative to using `print()` is the `SmartLogger` class (which wraps pythons logging package). This allows us to rate limit print messages and to set individual message severity levels.

The logging level can be changed (DEBUG|INFO|WARN|ERROR|CRITICAL) to control the verbosity of output. This can be used so that you do not have to comment out print statements. Rather, you can leave `logger.debug(<your_msg>)` in place and instead change the log level like `logger.setLevel(logging.WARN)` in `main()` to show only WARN and above log messages.

Some example logging commands:

```py
logger.info(sensors.odom, rate=3)
logger.info(sensors.odom.x, rate=3)
logger.info(sensors.odom.y, rate=3)
logger.info(msg=state_now["joints_positions"])
logger.debug(msg=f"Number of hexes: {my_var=}", rate=1)
```

## Saving Data

## Plotting

## Autoformat