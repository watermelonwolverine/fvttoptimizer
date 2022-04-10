# keeping constants outside any other files with imports to avoid module hell #

app_name = "fvttoptimizer"
config_file_name = "{0}.conf".format(app_name)
path_to_config_file_linux = "/etc/{0}".format(config_file_name)

author = "watermelonwolverine"
url = "https://github.com/%s/%s" % (author, app_name)
issues_url = "%s/issues" % url
