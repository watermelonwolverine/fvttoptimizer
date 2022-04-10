from cli_wrapper import __version_checker
from cli_wrapper.__constants import app_name

about = "\
About\n\
=====\n\
\n\
Optimizes images by (re-)saving them as webp. For every file it replaced it automatically updates all references.\n\
Works on single files as well as on folders."

usage = "\
Usage\n\
=====\n\
\n\
IMPORTANT:\n\
---------\n\
Shut down Foundry VTT before optimizing any files.\n\
\n\
Use this program at your own risk. It has been tested extensively but there are no guarantees. Always keep backup of\n\
your Foundry VTT data for cases where something goes wrong.\n\
\n\
Syntax\n\
------\n\
\n\
`{0} [--verbose-info, --verbose-debug, --version, --help, --quality value, --override-percent value, --skip-webp, --skip-existing, --recursive] target`\n\
\n\
`src`: Source path which should be moved or checked\n\
\n\
`*srcs`: Optional additional source paths\n\
\n\
`dst`: Path to destination folder or file, needed when not using the --check option\n\
\n\
Options\n\
-------\n\
\n\
`--verbose-info`: Enables verbose output to console\n\
\n\
`--verbose-debug`: Enables very verbose output to console\n\
\n\
`--version`: Prints version and exits\n\
\n\
`--help`: Display help and exit \n\
\n\
`--skip-existing`: Ignores files of which a webp already exists. For example image.png will not be converted if a\n\
image.webp is already in the same folder \n\
\n\
`--skip-webp`: Don't touch webp files at all \n\
\n\
`--quality`: The quality setting for the webp compression. Default is 75 \n\
\n\
`--override-percent`: How much smaller the new file needs to be to replace the old one. For example if this value is 25\n\
the file size after optimizing needs to be 25% smaller than the original. Default is 25 \n\
\n\
`--recursive`: If the optimization should be done recursively to all sub folders of the target folder.\n\
\n\
Examples\n\
--------\n\
\n\
Optimizing a file:\n\
\n\
Ubuntu:\n\
`{0} path/to/file.png`\n\
\n\
Windows:\n\
`{0} path\\to\\file.png`\n\
\n\
Optimizing a folder and all it's sub folders:\n\
\n\
Ubuntu:\n\
`{0} --recursive pathto/folder`\n\
\n\
Windows:\n\
`{0}.exe --recursive path\\to\\folder`\n\
\n\
Use single quotes when moving a file with a space:\n\
\n\
Ubuntu:\n\
`{0} 'some folder/some file.jpg'`\n\
\n\
Windows:\n\
`{0}.exe 'some folder\\some file.jpg'`\n\
\n\
Change parameters:\n\
\n\
Ubuntu:\n\
`{0} --quality 50 --override-percent 50 file.jpg`\n\
\n\
Windows:\n\
`{0} --quality 50 --override-percent 50 file.jpg`".format(app_name)

issues = "\
Known Issues and Quirks\n\
=======================\n\
\n\
Windows\n\
-------\n\
\n\
The program only works in powershell not in cmd.\n\
\n\
When one of the paths has `\\'` at the end, the arguments will get mixed up. This is a problem with how python handles\n\
arguments and probably can't be fixed. For example on Windows `{0}.exe '\\folder name with spaces\\'`\n\
will fail but `{0}.exe '\\folder name with spaces'` will succeed.".format(app_name)

installation = "\
Installation: Windows\n\
=====================\n\
\n\
Step 1: Get the exe\n\
-------------------\n\
\n\
### Option 1: Download\n\
\n\
Download one of the pre-built `{0}.exe` files from `Releases`\n\
\n\
Go to Step 2: Install program\n\
\n\
### Option 2: Build it yourself\n\
\n\
Install python3 (version >= 3.8) and add it to your PATH system environment variable.\n\
\n\
You can check the version via CMD or powershell with:\n\
\n\
`python --version`\n\
\n\
Download or clone the repo.\n\
\n\
Open a CMD instance inside the project root folder and create a virtual environment.\n\
\n\
`python -m venv .\\venv`\n\
\n\
Activate the venv:\n\
\n\
`.\\venv\\Scripts\\activate`\n\
\n\
Install the Pillow package:\n\
\n\
`pip install pillow=={1}`\n\
\n\
Install pyInstaller package:\n\
\n\
`pip install pyInstaller=={2}`\n\
\n\
Download the fvttmv python package (whl file) from\n\
here: `https://github.com/watermelonwolverine/fvttmv/releases/tag/{3}` move it into the folder and install it:\n\
\n\
`pip install fvttmv-{3}-py3-none-any.whl`\n\
\n\
Run build file:\n\
\n\
`.\\scripts\\build_for_windows.cmd`\n\
\n\
You should now have a {0}.exe file under dist. After the build succeeded you can delete the venv you\n\
previously created.\n\
\n\
Go to Step 2: Install program\n\
\n\
Step 2: Install program\n\
-----------------------\n\
\n\
Create an empty folder where you want to install the program for example C:\\{0}\n\
\n\
Copy {0}.exe into that folder.\n\
\n\
Create a {0}.conf text file in that folder.\n\
\n\
Copy `{{\"absolute_path_to_foundry_data\":\"INSERT_PATH_HERE\"}}` into {0}.conf\n\
\n\
Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata\n\
(Not the foundrydata folder itself!).\n\
\n\
IMPORTANT: Escape all `\\` with `\\\\` in that path.\n\
\n\
It should look something like this:\n\
\n\
`{{\"absolute_path_to_foundry_data\":\"C:\\\\Users\\\\user\\\\foundrydata\\\\Data\"}}`\n\
\n\
Add the installation path to your PATH system environment variable.\n\
\n\
Uninstallation: Windows\n\
=======================\n\
\n\
Delete {0}.exe and {0}.conf files from the installation directory.\n\
\n\
Remove the path to the installation directory from the PATH system environment variable.\n\
\n\
Installation: Ubuntu 16.04 -20.04\n\
=================================\n\
\n\
Optional: Install Python\n\
------------------------\n\
\n\
An up-to-date Ubuntu 20.04 should have python >= 3.8. Check it with:\n\
\n\
`python3 --version`\n\
\n\
From here on `pythonX` will be used as placeholder for the python you should use. Depending on your system you need to\n\
replace `X` with `3`, `3.8`, `3.9` or `3.10` .\n\
\n\
Install python version>=3.8 if not yet installed.\n\
\n\
`sudo apt install pythonX`\n\
\n\
Step 1: Get the executable\n\
--------------------------\n\
\n\
### Option 1: Download\n\
\n\
Download one of the pre-built `{0}` files from `Releases`\n\
\n\
Go to Step 2: Install the files\n\
\n\
### Option 2: Build it yourself\n\
\n\
Install python if haven't already.\n\
\n\
Install Pillow dependencies (read more here `https://pillow.readthedocs.io/en/stable/installation.html`):\n\
\n\
`sudo apt install pythonX-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev`\n\
\n\
Download or clone repo.\n\
\n\
Create venv inside the repo:\n\
\n\
`sudo apt install pythonX-venv`\n\
\n\
`pythonX -m venv ./venv`\n\
\n\
Activate venv:\n\
\n\
`source venv/bin/activate`\n\
\n\
Install Pillow (should succeed if you installed all the dependencies):\n\
\n\
`pythonX -m pip install Pillow=={1}`\n\
\n\
Install pyInstaller:\n\
\n\
`pythonX -m pip install pyInstaller=={2}`\n\
\n\
Download the fvttmv python package (whl file) from\n\
here: `https://github.com/watermelonwolverine/fvttmv/releases/tag/{3}` move it into the folder and install it:\n\
\n\
`pythonX -m pip install fvttmv-{3}-py3-none-any.whl`\n\
\n\
Now run the build script:\n\
\n\
`./scrips/build_for_ubuntu.sh`\n\
\n\
Step 2: Install the files\n\
-------------------------\n\
\n\
### Option 1: Automatic installation\n\
\n\
Install python if you haven't already.\n\
\n\
Clone the repo if you haven't already.\n\
\n\
Go into the project folder.\n\
\n\
Build the project if you haven't already. If you downloaded a pre-built executable. Create a folder named `dist` and move the file there. \n\
\n\
Inside the project folder run:\n\
\n\
`sudo pythonX scripts/install_on_ubuntu.sh`\n\
\n\
### Option 2: Manual installation\n\
\n\
Copy the `{0}` file either from `dist` from where you downloaded it to `usr/bin/{0}`\n\
\n\
Make the file executable:\n\
\n\
`sudo chmod ugo=rx usr/bin/{0}`\n\
\n\
Create a `{0}.conf` file at `/etc/`\n\
\n\
Copy `{{\"absolute_path_to_foundry_data\":\"INSERT_PATH_HERE\"}}` into `{0}.conf`\n\
\n\
Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata\n\
(Not the foundrydata folder itself!).\n\
\n\
It should look something like this:\n\
\n\
`{{\"absolute_path_to_foundry_data\":\"/home/user/foundrydata/Data\"}}`\n\
\n\
Uninstallation: Ubuntu\n\
======================\n\
\n\
Delete the files /etc/{0}.conf and /usr/bin/{0}".format(
    app_name,
    __version_checker.required_pillow_version_str,
    __version_checker.required_pyinstaller_version_str,
    __version_checker.required_fvttmv_version_str
)

help_text = "\
%s\n\
\n\
%s\n\
\n\
%s" % (about, usage, issues)

read_me = "\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s" % (about, installation, usage, issues)
