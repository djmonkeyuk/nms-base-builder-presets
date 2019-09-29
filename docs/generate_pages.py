"""Script for generating .md files from preset directories."""
import os

DOCS_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.realpath(os.path.join(DOCS_PATH, ".."))
EXCLUDE_FOLDERS = ["docs", "images"]
GITHUB_URL = "https://github.com/charliebanks/nms-base-builder-presets/blob/master"
GITHUB_PAGES_URL = "https://charliebanks.github.io/nms-base-builder-presets/"
GITHUB_RAWR_URL = "https://raw.githubusercontent.com/charliebanks/nms-base-builder-presets/master"

def get_categories():
    contents = os.listdir(ROOT_PATH)
    folders = [folder for folder in contents if "." not in folder]
    categories = [folder for folder in folders if folder not in EXCLUDE_FOLDERS]
    return categories

def get_presets(category):
    """Get all Presets."""
    full_path = os.path.join(ROOT_PATH, category)
    items = os.listdir(full_path)
    info = {}
    for item in items:
        basename = os.path.basename(item)
        info[item] = {
            "author": basename.split("_")[0],
            "name": basename.split("_")[-1].split(".")[0],
            "full_path": "/".join([GITHUB_RAWR_URL, category, item])
        }
    return info

def generate_homepage():
    content = "# No Man's Sky Base Builder Presets  \n\n"
    content += "## Categories  \n\n"
    

    categories = get_categories()
    for category in categories:
        category_url = category.replace(" ", "%20")
        content += "# [{}]({})  \n\n".format(category, os.path.join(GITHUB_PAGES_URL, category_url))
        content += "___\n\n"

    md_file = os.path.join(DOCS_PATH, "index.md")
    with open(md_file, "w") as stream:
        stream.write(content) 

def generate_category(category):
    preset_info = get_presets(category)
    content = "# No Man's Sky Base Builder Presets  \n\n"
    content += "## [< Back]({}) :: Category:: {}\n\n".format(GITHUB_PAGES_URL, category)
    content += "___\n\n"
    for preset, data in preset_info.items():
        name = data["name"]
        author = data["author"]
        full_path = data["full_path"]
        content += "__Name__: {}  \n".format(name)
        content += "__Author__: {}  \n".format(author)
        content += "[__Download__]({})  \n\n".format(full_path)
        content += "___\n\n"

    md_file = os.path.join(DOCS_PATH, category + ".md")
    with open(md_file, "w") as stream:
        stream.write(content) 
    return

def generate():
    """Main generate."""
    generate_homepage()
    categories = get_categories()
    for category in categories:
        generate_category(category)

if __name__ == "__main__":
    generate()