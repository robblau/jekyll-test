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
    #os.makedirs()

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

                frontmatter = "---\nlayout: default\ntitle: {title}\n---\n\n".format(title=name)
                content = frontmatter + content

                fh.write(content)



def process_folders(folder):
    """
    Upload folder to S3
    """
    if os.path.exists(os.path.join(folder, "external.conf")):
        # external rst folder - note: we do not recurse further
        print "Folder {} is an external sphinx reference...".format(folder)
    elif os.path.exists(os.path.join(folder, "index.rst")):
        # rst folder - note: we do not recurse further
        print "Folder {} is rst-folder which need converting...".format(folder)
        sphinx_to_markdown(folder)
    else:
        # find folders and recurse into them
        print "no sphinx pre-processing for folder {}...".format(folder)
        for name in os.listdir(folder):
            file_name = os.path.join(folder, name)
            if os.path.isdir(file_name):
                process_folders(file_name)






#
# echo "cloning core..."
# TMP_SPHINX_FOLDER=${TMP_BUILD_FOLDER}_spx
# rm -rf ${TMP_SPHINX_FOLDER}
# mkdir -p ${TMP_SPHINX_FOLDER}
#
# git clone --depth 1 https://github.com/shotgunsoftware/tk-core.git ${TMP_SPHINX_FOLDER}/git/tk-core
# export PYTHONPATH=$PYTHONPATH:${TMP_SPHINX_FOLDER}/git/tk-core/python
#
# echo "converting sphinx -> markdown"
# sphinx-build -b markdown -c ${THIS_DIR}/../sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${TMP_SPHINX_FOLDER}/git/tk-core/docs ${TMP_BUILD_FOLDER}/tk-core
#
# git clone --depth 1 https://github.com/shotgunsoftware/tk-framework-shotgunutils.git ${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils
# export PYTHONPATH=$PYTHONPATH:${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils/python
#
# echo "converting sphinx -> markdown"
# sphinx-build -b markdown -c ${THIS_DIR}/../sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils/docs ${TMP_BUILD_FOLDER}/tk-framework-shotgunutils



process_folders(input_folder)