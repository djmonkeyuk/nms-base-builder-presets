"""Script for generating .md files from preset directories."""
import json
import os
import re
import time
import urllib
from collections import OrderedDict

DOCS_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.realpath(os.path.join(DOCS_PATH, ".."))
EXCLUDE_FOLDERS = ["docs", "images", "sounds"]
GITHUB_URL = "https://github.com/djmonkeyuk/nms-base-builder-presets/blob/master"
GITHUB_PAGES_URL = "https://djmonkeyuk.github.io/nms-base-builder-presets/"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/djmonkeyuk/nms-base-builder-presets/master"
GITHUB_BLOB_URL = "https://github.com/djmonkeyuk/nms-base-builder-presets/blob/master/"
MISSING_THUMB_URL = "https://raw.githubusercontent.com/djmonkeyuk/nms-base-builder-presets/master/images/missing_thumbnail.jpg"


WELCOME_MESSAGE = """

## Join the Discord Community!

Before exploring the preset directory, please know that there is now a dedicated Discord community for both the No Man's Sky Base Building [Add-on for Blender](https://www.nexusmods.com/nomanssky/mods/984) And the [Standalone Building App](https://www.nexusmods.com/nomanssky/mods/2598). There are preset and prefab sharing channels which is a much more interactive and responsive way of sharing your builds! :)

[Discord Invite Link](https://discord.gg/Mmz3rpq4Px)

The Discord channel also contains information about a new indie game I've been developing titled - [_Tales from The Dancing Moon_](https://store.steampowered.com/app/1782420/Tales_from_The_Dancing_Moon/). If you've enjoyed my No Man's Sky tools, then please try it out! :)

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

Please visit the [GitHub](https://github.com/djmonkeyuk/nms-base-builder-presets) page for details on how to contribute.
"""

def get_categories():
    contents = os.listdir(ROOT_PATH)
    folders = [folder for folder in contents if "." not in folder]
    categories = [folder for folder in folders if folder not in EXCLUDE_FOLDERS]
    return categories

def get_nice_name(label):
    """Uber regex conversion to get nice space seperation.

    Taken from : https://stackoverflow.com/questions/5020906/python-convert-camel-case-to-space-delimited-using-regex-and-taking-acronyms-in
    """
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', label)

def get_timestamp(path):
    with open(path, "r") as stream:
        data = json.load(stream)
        return data.get("timestamp", 0)

def sorted_ls(path, ext="json"):
    all_files = [x for x in os.listdir(path) if x.endswith(".{}".format(ext))]
    all_files_full = [os.path.join(path, x) for x in all_files]
    sorted_items = reversed(list(sorted(all_files_full, key=get_timestamp)))
    return [os.path.basename(x) for x in sorted_items]

def get_time(file_path):
    with open(file_path, "r") as stream:
        data = json.load(stream)
        return time.strftime('%Y-%m-%d', time.localtime(data.get("timestamp", 0)))

def extract_author_and_name(basename):
    author, name = basename.split("_", 1)
    name = name.split(".")[0]
    return author, name

def get_presets(category):
    """Get all Presets."""
    full_path = os.path.join(ROOT_PATH, category)
    items = sorted_ls(full_path)
    info = OrderedDict()
    for item in items:
        basename = os.path.basename(item)
        full_local_path = "/".join([ROOT_PATH, category, item])
        full_online_path = "/".join([GITHUB_RAW_URL, category, item])
        author, name = extract_author_and_name(basename)
        info[item] = {
            "author": author,
            "name": name,
            "date": get_time(full_local_path),
            "full_path": full_online_path,
            "image_path": "/".join([GITHUB_RAW_URL, "images", category, item.replace(".json", ".jpg")]),
            "audio_path": "/".join([GITHUB_BLOB_URL, "sounds", category, item.replace(".json", ".mp3") + "?raw=true"]),
            "local_image_path": os.path.join(ROOT_PATH, "images", category, item.replace(".json", ".jpg"))
        }
    return info

def get_first_image(category):
    category_path = os.path.join(ROOT_PATH, "images", category)
    default = os.path.join(GITHUB_RAW_URL, "images", "missing_thumbnail.jpg")

    if not os.path.exists(category_path):
        return default

    # Get First Item.
    full_path = os.path.join(ROOT_PATH, category)
    items = sorted_ls(full_path)
    for item in items:
        local_url = os.path.join(ROOT_PATH, "images", category, item.replace(".json", ".jpg"))
        git_hub_url = os.path.join(GITHUB_RAW_URL, "images", category, item.replace(".json", ".jpg"))
        if os.path.exists(local_url):
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
        name = get_nice_name(data["name"])
        author = data["author"]
        date = data["date"]
        full_path = data["full_path"]
        image_path = data["image_path"]
        audio_path = data["audio_path"]
        local_image_path = data["local_image_path"]
        if not os.path.isfile(local_image_path):
            image_path = MISSING_THUMB_URL

        # Create a HTML table as markdown is fairly limiting.
        if category == "Byte Beats":
            content += ("""<tr>
                <td width=\"40%\"><audio controls>
                    <source src="{}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio></td>
                <td valign="top" width=\"60%\"><b>Name:</b> {} <br /> <b>Author:</b> {} <br /><b>Date:</b> {} <br /> <b><a href=\"{}\">Download (Right-Click -> Save link as...)</a></b></td>
            </tr>
            """).format(audio_path, name, author, date, full_path)
        else:
            content += (
                """<tr>
            <td width=\"40%\"><img src=\"{}\"></td>
            <td valign="top" width=\"60%\"><b>Name:</b> {} <br /> <b>Author:</b> {} <br /><b>Date:</b> {} <br /> <b><a href=\"{}\">Download (Right-Click -> Save link as...)</a></b></td>
        </tr>""").format(image_path, name, author, date, full_path)

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
