Blair Lego Robotics 2015
========================

General Design
--------------
* Use the [python-ev3 API](https://github.com/topikachu/python-ev3)

Work Delegation
---------------
Here are the tasks each programmer should focus on, along with the approximate date it should be completed by:
* Antares - Goal setting - localization
* George - Goal setting - localization
* Ramu - 
* Aaron - General managment and goal setting - path finding
* Alan - Maintence code - drive code
* Harrison - Maintence code - drive code
* Karina - Presentation/Notebook and goal setting - path finding

Note that to run the code on the robot only through the ev3 interface, you must have an executable shell script.

The shell script must initialize the virtual environment to allow for the ev3-python packages.

The commands are:
<initialize shell>
source /etc/bash_completion.d/virtualenvwrapper
workon ev3_py34