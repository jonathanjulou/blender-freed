# blender-freed

A blender plugin to read a live freed feed. \
It provides 4 freed receiver slots, which can be bound to objects to change their position and orientation in real-time. \
Lens data not supported yet. Genlock and Timecode not supported.

Animation data can be recorded by pressing the play button in the timeline. \
/!\ make sure not to loop over previously recorded data. stop the receivers before playing recorded data. /!\

This code belongs to the company oARo and is provided as is to help people interested in experimenting with virtual production / previz in Blender.
https://oaro.studio/ \
This code was tested using and is mainly meant for oARo product EZtrack, a camera and talent tracking hub which can output freed over the network.
https://eztrack.studio 


## install the add-on

in Blender, go to edit->preferences->add-on\
click the "install" button\
select the zip file and proceed\
check the box to activate the add-on.

In the Scene menu, a "Freed" panel should have appeared.

## compile add-on

run compile_addon.py from the root of the git repository\
this will generate a zip file whih can be installed in Blender.

