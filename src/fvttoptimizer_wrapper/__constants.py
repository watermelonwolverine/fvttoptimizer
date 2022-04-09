# keeping constants outside any other files with imports to avoid module hell #

app_name = "fvttoptimizer"
config_file_name = "{0}.conf".format(app_name)
path_to_config_file_linux = "/etc/{0}".format(config_file_name)
