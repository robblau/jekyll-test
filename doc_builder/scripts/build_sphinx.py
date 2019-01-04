import sys
import shutil
import subprocess
import commands
import os

input_folder = os.path.abspath(sys.argv[1])
print "Sphinx doc generation"
print "will process sphinx structure in %s" % input_folder
print ""


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sphinx_config_path = os.path.join(root_path, "sphinx")


def sphinx_to_markdown(folder):

    source_folder = "{}.rst".format(folder)
    shutil.move(folder, source_folder)

    cmd = "sphinx-build -b markdown -c {config_path} -D project='foo' -D release='bar' -D version='0.0.0' {input} {output}".format(config_path=sphinx_config_path, input=source_folder, output=folder)
    print "executing {}".format(cmd)

    (ret_code, output) = commands.getstatusoutput(cmd)
    print output

    if ret_code != 0:
        print "error - aborting."
        sys.exit(1)

    # for each generated markdown file, add a jekyll frontmatter chunk
    for name in os.listdir(folder):
        filename = os.path.join(folder, name)
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





if os.path.exists(os.path.join(input_folder, "index.rst")):
    print 'detected sphinx build...'
    sphinx_to_markdown(input_folder)

if os.path.exists(os.path.join(input_folder, "sphinx.yml")):
    print 'detected sphinx config...'
