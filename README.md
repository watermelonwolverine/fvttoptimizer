WARNING: DEPRECATED, DO NOT USE WITH FOUNDRYVTT VERSION >10
=========================================================
Because FoundryVTT changed its underlying database with version 11 this tool no longer works and should be considered deprecated.
I will update it once I find the time.
Until then, don't use it.

About
=====

Optimizes images by (re-)saving them as webp. For every file it replaced it automatically updates all references.
Works on single files as well as on folders.

Installation: Windows
=====================

Step 1: Get the exe
-------------------

### Option 1: Download

Download one of the pre-built `fvttoptimizer.exe` files from `Releases`

Go to Step 2: Install program

### Option 2: Build it yourself

Install python3 (version >= 3.8) and add it to your PATH system environment variable.

You can check the version via CMD or powershell with:

`python --version`

Download or clone the repo.

Open a CMD instance inside the project root folder and create a virtual environment.

`python -m venv .\venv`

Activate the venv:

`.\venv\Scripts\activate`

Install the Pillow package:

`pip install pillow==9.1.0`

Install pyInstaller package:

`pip install pyInstaller==4.10`

Download the fvttmv python package (whl file) from
here: `https://github.com/watermelonwolverine/fvttmv/releases/tag/0.2.4` move it into the folder and install it:

`pip install fvttmv-0.2.4-py3-none-any.whl`

Run build file:

`.\scripts\build_for_windows.cmd`

You should now have a fvttoptimizer.exe file under dist. After the build succeeded you can delete the venv you
previously created.

Go to Step 2: Install program

Step 2: Install program
-----------------------

Create an empty folder where you want to install the program for example C:\fvttoptimizer

Copy fvttoptimizer.exe into that folder.

Create a fvttoptimizer.conf text file in that folder.

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into fvttoptimizer.conf

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

IMPORTANT: Escape all `\` with `\\` in that path.

It should look something like this:

`{"absolute_path_to_foundry_data":"C:\\Users\\user\\foundrydata\\Data"}`

Add the installation path to your PATH system environment variable.

Uninstallation: Windows
=======================

Delete fvttoptimizer.exe and fvttoptimizer.conf files from the installation directory.

Remove the path to the installation directory from the PATH system environment variable.

Installation: Ubuntu 16.04 -20.04
=================================

Optional: Install Python
------------------------

An up-to-date Ubuntu 20.04 should have python >= 3.8. Check it with:

`python3 --version`

From here on `pythonX` will be used as placeholder for the python you should use. Depending on your system you need to
replace `X` with `3`, `3.8`, `3.9` or `3.10` .

Install python version>=3.8 if not yet installed.

`sudo apt install pythonX`

Step 1: Get the executable
--------------------------

### Option 1: Download

Download one of the pre-built `fvttoptimizer` files from `Releases`

Go to Step 2: Install the files

### Option 2: Build it yourself

Install python if haven't already.

Install Pillow dependencies (read more here `https://pillow.readthedocs.io/en/stable/installation.html`):

`sudo apt install pythonX-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev`

Download or clone repo.

Create venv inside the repo:

`sudo apt install pythonX-venv`

`pythonX -m venv ./venv`

Activate venv:

`source venv/bin/activate`

Install Pillow (should succeed if you installed all the dependencies):

`pythonX -m pip install Pillow==9.1.0`

Install pyInstaller:

`pythonX -m pip install pyInstaller==4.10`

Download the fvttmv python package (whl file) from
here: `https://github.com/watermelonwolverine/fvttmv/releases/tag/0.2.4` move it into the folder and install it:

`pythonX -m pip install fvttmv-0.2.4-py3-none-any.whl`

Now run the build script:

`./scrips/build_for_ubuntu.sh`

Step 2: Install the files
-------------------------

### Option 1: Automatic installation

Install python if you haven't already.

Clone the repo if you haven't already.

Go into the project folder.

Build the project if you haven't already. If you downloaded a pre-built executable. Create a folder named `dist` and move the file there. 

Inside the project folder run:

`sudo pythonX scripts/install_on_ubuntu.sh`

### Option 2: Manual installation

Copy the `fvttoptimizer` file either from `dist` from where you downloaded it to `usr/bin/fvttoptimizer`

Make the file executable:

`sudo chmod ugo=rx usr/bin/fvttoptimizer`

Create a `fvttoptimizer.conf` file at `/etc/`

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into `fvttoptimizer.conf`

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

It should look something like this:

`{"absolute_path_to_foundry_data":"/home/user/foundrydata/Data"}`

Uninstallation: Ubuntu
======================

Delete the files /etc/fvttoptimizer.conf and /usr/bin/fvttoptimizer

Usage
=====

IMPORTANT:
---------
Shut down Foundry VTT before optimizing any files.

Use this program at your own risk. It has been tested extensively but there are no guarantees. Always keep backup of
your Foundry VTT data for cases where something goes wrong.

Syntax
------

`fvttoptimizer [--verbose-info, --verbose-debug, --version, --help, --quality value, --override-percent value, --skip-webp, --skip-existing, --recursive] target`

`target`: Path to file or directory which should be optimized

Options
-------

`--verbose-info`: Enables verbose output to console

`--verbose-debug`: Enables very verbose output to console

`--version`: Prints version and exits

`--help`: Display help and exit 

`--skip-existing`: Ignores files of which a webp already exists. For example image.png will not be converted if a
image.webp is already in the same folder 

`--skip-webp`: Don't touch webp files at all 

`--quality`: The quality setting for the webp compression. Default is 75 

`--override-percent`: How much smaller the new file needs to be to replace the old one. For example if this value is 25
the file size after optimizing needs to be 25% smaller than the original. Default is 25 

`--recursive`: If the optimization should be done recursively to all sub folders of the target folder.

Examples
--------

Optimizing a file:

Ubuntu:
`fvttoptimizer path/to/file.png`

Windows:
`fvttoptimizer path\to\file.png`

Optimizing a folder and all it's sub folders:

Ubuntu:
`fvttoptimizer --recursive pathto/folder`

Windows:
`fvttoptimizer.exe --recursive path\to\folder`

Use single quotes when moving a file with a space:

Ubuntu:
`fvttoptimizer 'some folder/some file.jpg'`

Windows:
`fvttoptimizer.exe 'some folder\some file.jpg'`

Change parameters:

Ubuntu:
`fvttoptimizer --quality 50 --override-percent 50 file.jpg`

Windows:
`fvttoptimizer --quality 50 --override-percent 50 file.jpg`

Known Issues and Quirks
=======================

Windows
-------

The program only works in powershell not in cmd.

When one of the paths has `\'` at the end, the arguments will get mixed up. This is a problem with how python handles
arguments and probably can't be fixed. For example on Windows `fvttoptimizer.exe '\folder name with spaces\'`
will fail but `fvttoptimizer.exe '\folder name with spaces'` will succeed.
