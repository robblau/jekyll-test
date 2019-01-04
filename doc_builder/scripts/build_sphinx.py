import sys
import uuid
import shutil
import pprint
import subprocess
import tempfile
import commands
from ruamel.yaml import YAML
import os

input_folder = os.path.abspath(sys.argv[1])
print "Sphinx doc generation"
print "will process sphinx structure in %s" % input_folder
print ""


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sphinx_config_path = os.path.join(root_path, "sphinx")


def add_to_pythonpath(path):
    """
    Prepends to PYTHONPATH and sys.path

    :param path: The path to add
    """
    pythonpath = os.environ.get("PYTHONPATH", "").split(":")
    path = os.path.expanduser(os.path.expandvars(path))
    pythonpath.insert(0, path)
    sys.path.insert(0, path)
    os.environ["PYTHONPATH"] = ":".join(pythonpath)


def add_frontmatter_to_files(folder):
    """
    adds frontmatter to all md files, recursively
    """
    # for each generated markdown file, add a jekyll frontmatter chunk
    for name in os.listdir(folder):
        filename = os.path.join(folder, name)

        if os.path.isdir(filename):
            add_frontmatter_to_files(filename)

        if filename.endswith(".md"):
            with open(filename, "rt") as fh:
                content = fh.read()

            with open(filename, "wt") as fh:
                # ---
                # layout: default
                # title: Release Notes
                # nav_order: 11
                # ---

                # title is the filename without extension, capitalized
                (name_no_ext, _) = os.path.splitext(name)

                frontmatter = "---\nlayout: default\ntitle: {title}\n---\n\n- TOC\n{{:toc}}\n\n".format(
                    title=name_no_ext.capitalize()
                )
                content = frontmatter + content

                fh.write(content)






def sphinx_to_markdown(folder):

    # move the folder to be named .rst and replace with md build
    source_folder = "{}_rst".format(folder)
    shutil.move(folder, source_folder)

    cmd = "sphinx-build -b markdown -c {config_path} {input} {output}".format(config_path=sphinx_config_path, input=source_folder, output=folder)
    print "executing {}".format(cmd)

    (ret_code, output) = commands.getstatusoutput(cmd)
    print output

    if ret_code != 0:
        print "error - aborting."
        sys.exit(1)

    #add_frontmatter_to_files(folder)



if os.path.exists(os.path.join(input_folder, "index.rst")):
    print 'detected sphinx build...'
    sphinx_to_markdown(input_folder)

yaml_file = os.path.join(input_folder, "sphinx.yml")

if os.path.exists(yaml_file):
    print 'detected sphinx config...'

    yaml = YAML(typ='safe')
    with open(yaml_file, "rt") as fh:
        yaml_data = yaml.load(fh)
    pprint.pprint(yaml_data)

    repo_data = yaml_data.get("repositories")

    temp_folder = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
    sphinx_folder = os.path.join(input_folder, "sphinx")

    os.makedirs(temp_folder)
    os.makedirs(sphinx_folder)

    index_files = []

    for (name, params) in repo_data.iteritems():

        (repo_name, _) = os.path.splitext(os.path.basename(params["git_url"]))

        git_folder = os.path.join(temp_folder, repo_name)
        target_folder = os.path.join(sphinx_folder, repo_name)

        index_files.append("{}/index".format(repo_name))

        (ret_code, output) = commands.getstatusoutput(
            "git clone --depth=50 {repo} {folder}".format(repo=params["git_url"], folder=git_folder)
        )
        print output

        # check out latest tag
        cmd = "cd {}; git checkout $(git describe --tags $(git rev-list --tags --max-count=1))".format(git_folder)
        (ret_code, output) = commands.getstatusoutput(cmd)
        print output

        cmd = "cd {}; git describe --tags".format(git_folder)
        (ret_code, output) = commands.getstatusoutput(cmd)
        print output

        # add python source to pythonpath
        add_to_pythonpath(os.path.join(git_folder, "python"))

        # copy docs folder
        shutil.move(os.path.join(git_folder, "docs"), target_folder)


    # construct an index.rst to link up all the docs
    with open(os.path.join(sphinx_folder, "index.rst"), "wt") as fh:
        fh.write(".. toctree::\n")
        for index_file in index_files:
            fh.write("\t{}\n".format(index_file))

    sphinx_to_markdown(sphinx_folder)



