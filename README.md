# SetupFire
### A tool to setup your Akai Fire to a specific pattern of colored pads on demand.

When the computer initially starts up, the Akai Fire device will display an alternating red/white pattern on it's pads. This pattern remains until FL Studio is started. 

This tool was developed to allow users to change their Akai Fire color from the default red/white to whatever they choose so that they can set the Fire to a preferred color scheme when not using FL Studio.

## Pre-compiled version
A pre-compiled version for Windows can be used without the need to download and compile the source. Download from [**SetupFireEXE.zip**](https://github.com/nfxbeats/SetupFire/releases/download/precompiled/SetupFireEXE.zip)

## .INI File documentation
The code relies upon an .INI file to direct it how to setup the Fire pads. The .INI file should exists in the same folder from where SetupFire is running and be named ```SetupFire.INI```

A sample .INI file looks like this:

```
[Fire]
UsePattern=True

[Pattern]
colors = [0x000000, 0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0x101010, 0x000010]
row1 = [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
row2 = [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
row3 = [0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]
row4 = [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]

```
### [Fire] section
If ```UsePattern``` is ```False``` then the Fire will simply turn off all the button and pad lights, otherwise if ```True``` it will use the information contained in the ```[Pattern]``` section to determine how to color the pads.

### [Pattern Section]
There are four important lines required. One for the color definitions, and four more that represent each 16 pad row on the Fire.

```colors``` should be a comma delimited list of RGB colors using the python style hex format (0xRRGGBB) enclosed by square braces. 
For example:
```
colors = [0x000000, 0xFFFFFF, 0xFF0000]
```
Each color in the list has an index value where the starting index is 0. So using the above example the Color Index values are as follows:

| Color Value | Color Index |    
|-------------|-------------|
| 0x000000    |     0       |    
| 0xFFFFFF    |     1       |
| 0xFF0000    |     2       |

Using the Color Index number allows you to define the rows of 16 pads. you can define row1...row4. Each rowX should be a list of comma delimited Color Indexes anclosed in square brackets.

Here is an example for row1:
```
row1 = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2]
```

From the example above, the first four pads in row 1 will be colored 0x000000. The next four pads will be of color 0xFFFFFF followed by four more of color 0x000000 and finally the last four pads will be colored 0xF00000.

Any Color Index value that does not exist will default to 0x000000.

# Source Requirements
This project uses the following python libraries:

1. **mido** - this allows the program to communicate with MIDI devices.
2. **pyinstaller** (optional)- this allows the user to create a stand-alone executable.

You can use pip to install the libraries:

```
pip install mido
pip install pyinstaller
```

