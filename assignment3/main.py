#!/bin/python3
import json #Used to load json
from jinja2 import Environment, FileSystemLoader #Templating

def main(args):
    e = Environment(loader=FileSystemLoader('templates/'))

    template = e.get_template("linux.tmpl")

    menuentry = template.render(title=args['title'], kernel_path='/boot/kernel.1', initrd_path='/boot/initrd.1.gz')

    return menuentry


if __name__ == "__main__":
    with open ("./entries.json") as f:
        x = json.load(f)

    menu = ""
    for item in x:
        menu_entry = main(item)
        menu += menu_entry
        menu += "\n\n"

    with open ("/etc/grub.d/40_custom", "w") as f:
        f.write("#!/bin/sh\n")
        f.write("exec tail -n +3 50\n")
        f.write("#Comment that should be here but isn't here\n")
        f.write(menu)

