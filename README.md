About
=====

Optimizes images by (re-)saving them as webp. Works on single files as well as on folders.

IMPORTANT: Shut down Foundry VTT optimizing any files.

Installation: Windows
=====================

Step 1: Get the exe
-------------------

### Option 1: Download

Download one of the pre-built fvttoptimizer.exe files from `Releases`

Goto Step 2: Install program

### Option 2: Build it yourself

Install python3 (version >= 3.9) and add it to your PATH system environment variable.

You can check the version via CMD or powershell with:

`python --version`

Download or clone the repo.

Open a CMD instance inside the project root folder and create a virtual environment.

`python -m venv .\venv`

Activate the venv:

`.\venv\Scripts\activate`

Install pyInstaller package:

`pip install pyInstaller`

Run build file:

`.\scripts\build_for_windows.cmd`

You should now have a fvttoptimizer.exe file under dist. After the build succeeded you can delete the venv you
previously created.

Goto Step 2: Install program

Step 2: Install program
-----------------------

Create an empty folder where you want to install the program for example C:\fvttoptimizer

Copy fvttoptimizer.exe into that folder.

Create a fvttoptimizer.conf text file in that folder.

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into fvttoptimizer.conf

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

IMPORTANT: Escape all \\ with \\\\ in that path.

It should look something like this:

`{"absolute_path_to_foundry_data":"C:Users\\user\\foundrydata\\Data"}`

Add the installation path to your PATH system environment variable.

Uninstallation: Windows
=======================

Delete fvttoptimizer.exe and fvttoptimizer.conf files from the installation directory.

Remove the path to the installation directory from the PATH system environment variable.

Installation: Ubuntu
====================

Install python3 if not yet installed

`sudo apt install python3`

Download or clone repo.

Run the install.py script inside the project folder with

`sudo python3 ./scripts/install_on_ubuntu.py`

and follow the installation instructions.

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

`src`: Source path which should be moved or checked\
`*srcs`: Optional additional source paths\
`dst`: Path to destination folder or file, needed when not using the --check option

Options
-------

`--verbose-info`: Enables verbose output to console\
`--verbose-debug`: Enables very verbose output to console\
`--version`: Prints version and exits\
`--help`: Display help and exit \
`--skip-existing`: Ignores files of which a webp already exists. For example image.png will not be converted if a
image.webp is already in the same folder \
`--skip-webp`: Don't touch webp files at all \
`--quality`: The quality setting for the webp compression. Default is 75 \
`--override-percent`: How much smaller the new file needs to be to replace the old one. For example if this value is 25%
the file size after optimizing needs to be 25% smaller than the original. Default is 25 \
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

