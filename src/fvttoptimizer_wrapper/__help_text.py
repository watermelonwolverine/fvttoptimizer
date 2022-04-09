help_text = \
    "About\n\
    =====\n\
    \n\
    Optimize images by (re-)saving them as webp. Works on single files as well as on folders.\n\
    \n\
    IMPORTANT: Shut down Foundry VTT optimizing any files.\n\
    \n\
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
    `fvttoptimizer [--verbose-info, --verbose-debug, --version, --help, --quality value, --override-percent value, --skip-webp, --skip-existing, --recursive] target`\n\
    \n\
    `src`: Source path which should be moved or checked\\n\
    `*srcs`: Optional additional source paths\\n\
    `dst`: Path to destination folder or file, needed when not using the --check option\n\
    \n\
    Options\n\
    -------\n\
    \n\
    `--verbose-info`: Enables verbose output to console\\n\
    `--verbose-debug`: Enables very verbose output to console\\n\
    `--version`: Prints version and exits\\n\
    `--help`: Display help and exit \\n\
    `--skip-existing`: Ignores files of which a webp already exists. For example image.png will not be converted if a\n\
    image.webp is already in the same folder \\n\
    `--skip-webp`: Don't touch webp files at all \\n\
    `--quality`: The quality setting for the webp compression. Default is 75 \\n\
    `--override-percent`: How much smaller the new file needs to be to replace the old one. For example if this value is 25%\n\
    the file size after optimizing needs to be 25% smaller than the original. Default is 25 \\n\
    `--recursive`: If the optimization should be done recursively to all sub folders of the target folder.\n\
    \n\
    Examples\n\
    --------\n\
    \n\
    Optimizing a file:\n\
    \n\
    Ubuntu:  \n\
    `fvttoptimizer path/to/file.png`\n\
    \n\
    Windows:  \n\
    `fvttoptimizer path\to\file.png`\n\
    \n\
    Optimizing a folder and all it's sub folders:\n\
    \n\
    Ubuntu:\n\
    `fvttoptimizer --recursive pathto/folder`\n\
    \n\
    Windows:\n\
    `fvttoptimizer.exe --recursive path\to\folder`\n\
    \n\
    Use single quotes when moving a file with a space:\n\
    \n\
    Ubuntu:\n\
    `fvttoptimizer 'some folder/some file.jpg'`\n\
    \n\
    Windows:\n\
    `fvttoptimizer.exe 'some folder\some file.jpg'`\n\
    \n\
    Change parameters:\n\
    \n\
    Ubuntu:\n\
    `fvttoptimizer --quality 50 --override-percent 50 file.jpg`\n\
    \n\
    Windows:\n\
    `fvttoptimizer --quality 50 --override-percent 50 file.jpg`\n\
    \n\
    Known Issues and Quirks\n\
    =======================\n\
    \n\
    Windows\n\
    -------\n\
    \n\
    The program only works in powershell not in cmd.\n\
    \n\
    When one of the paths has `\'` at the end, the arguments will get mixed up. This is a problem with how python handles\n\
    arguments and probably can't be fixed. For example on Windows `fvttoptimizer.exe '\folder name with spaces\'`\n\
    will fail but `fvttoptimizer.exe '\folder name with spaces'` will succeed.\n\
    "
