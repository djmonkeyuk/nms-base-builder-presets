"""Script for generating .md files from preset directories."""
import os
import urllib

DOCS_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.realpath(os.path.join(DOCS_PATH, ".."))
EXCLUDE_FOLDERS = ["docs", "images"]
GITHUB_URL = "https://github.com/charliebanks/nms-base-builder-presets/blob/master"
GITHUB_PAGES_URL = "https://charliebanks.github.io/nms-base-builder-presets/"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/charliebanks/nms-base-builder-presets/master"
MISSING_THUMB_URL = "https://raw.githubusercontent.com/charliebanks/nms-base-builder-presets/master/images/missing_thumbnail.jpg"


WELCOME_MESSAGE = """
## Welcome

Explore this website to find base building Presets created by the community 
to be used with the _[No Man's Sky Base Builder](https://www.nexusmods.com/nomanssky/mods/984)_ for _Blender_.

Within these categories are a series of `JSON` files which correspond to a 
particular preset.

These can be downloaded and placed into your No Man's Sky Base Builder user 
folder located here.

```
%USERPROFILE%/NoMansSkyBaseBuilder/presets/
```

They will then appear in the Preset list within the tool.
"""

CONTRIBUTION_MESSAGE = """
## Contribute

Please visit the [GitHub](https://github.com/charliebanks/nms-base-builder-presets) page for details on how to contribute.
"""

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
            "full_path": "/".join([GITHUB_RAW_URL, category, item]),
            "image_path": "/".join([GITHUB_RAW_URL, "images", category, item.replace(".json", ".jpg")]),
            "local_image_path": os.path.join(ROOT_PATH, "images", category, item.replace(".json", ".jpg"))
        }
    return info

def get_first_image(category):
    category_path = os.path.join(ROOT_PATH, "images", category)
    default = os.path.join(GITHUB_RAW_URL, "images", "missing_thumbnail.jpg")
    
    if not os.path.exists(category_path):
        return default

    images = [each for each in os.listdir(category_path) if each.endswith(".jpg")]
    if images:
        git_hub_url = os.path.join(GITHUB_RAW_URL, "images", category, images[0])
        return git_hub_url
    
    return default

def generate_homepage():
    content = "# No Man's Sky Base Builder Presets  \n\n"
    content+= WELCOME_MESSAGE
    content+= CONTRIBUTION_MESSAGE
    content += "\n\n## Categories  \n\n"
    content += (
        """<table cellpadding="10">
        <tbody>"""
    )
    categories = get_categories()
    for category in categories:
        category_url = category.replace(" ", "%20")
        first_image = get_first_image(category)
        category_link = os.path.join(GITHUB_PAGES_URL, category_url)

        content += (
            """<tr>
            <td width=\"40%\"><a href=\"{}\"><img src=\"{}\"></a></td>
            <td valign="top" width=\"60%\"><h2><a href=\"{}\">{}</a></h2></td>
        </tr>""").format(category_link, first_image, category_link, category)

    content += """
</tbody>
</table>
"""
    md_file = os.path.join(DOCS_PATH, "index.md")
    with open(md_file, "w") as stream:
        stream.write(content) 

def generate_category(category):
    preset_info = get_presets(category)
    # Header.
    content = "# No Man's Sky Base Builder Presets  \n\n"
    content += "## [< Back]({}) :: {}\n\n".format(GITHUB_PAGES_URL, category)
    content += "___\n\n"

    content += """
<table cellpadding="10">
<thead>
    <tr>
        <th>Image</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    """
    # Items.
    for data in preset_info.values():
        # Get data.
        name = data["name"]
        author = data["author"]
        full_path = data["full_path"]
        image_path = data["image_path"]
        local_image_path = data["local_image_path"]
        if not os.path.isfile(local_image_path):
            image_path = MISSING_THUMB_URL

        # Create a HTML table as markdown is fairly limiting.
        content += (
            """<tr>
            <td width=\"40%\"><img src=\"{}\"></td>
            <td valign="top" width=\"60%\"><b>Name:</b> {} <br /> <b>Author:</b> {} <br /> <b><a href=\"{}\">Download (Right-Click -> Save link as...)</a></b></td>
        </tr>""").format(image_path, name, author, full_path)

    content += """
</tbody>
</table>
    """


    md_file = os.path.join(DOCS_PATH, category + ".md")
    with open(md_file, "w") as stream:
        stream.write(content) 

def generate():
    """Main generate."""
    generate_homepage()
    categories = get_categories()
    for category in categories:
        generate_category(category)

if __name__ == "__main__":
    generate()
