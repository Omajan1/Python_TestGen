import argparse
# import subprocess
import yaml
import os


class Generator():
    def __init__(self, args):
        self.args = args


    def find_template_path(self):
        full_name = f"{self.args.script_lang}_{self.args.file_system}"
        
        if self.args.script_lang == "bash":
            full_name += ".sh"

        script_path = os.path.abspath(f"{os.getcwd()}/template_scripts/{full_name}")
        return script_path
    
    def find_yaml_path(self):
        yaml_name = f"{self.args.format_yaml}"
        return yaml_name
    
    def add_dir(self, yaml_file, og_content, placeholder_dir):
        # Split at the placeholder
        before, after = og_content.split(placeholder_dir, 1)

        text_to_insert = "\n"

        for dir in yaml_file["structure"]["directories"]:
            text_to_insert += "mkdir " + dir["path"] + "\n"

        new_content = before + placeholder_dir + "\n" + text_to_insert + "\n" + after

        with open(self.find_template_path(), "w") as f:
            f.write(new_content)

    def change_size(self):
        pass

    def add_files(self):
        pass

    def change_name(self):
        pass

    def modify_template(self):
        with open(self.find_yaml_path(), "r") as f:
            yaml_ = yaml.safe_load(f)
        
        with open(self.find_template_path(), "r") as f:
            content = f.read()

        # Change script
        self.change_size()
        self.add_dir(yaml_, content, "#PLACEHOLDER# Adding directories #")
        self.add_files()

        pass

    def main(self):
        self.modify_template()
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--script_lang", help="The script language we will generate the code in (bash, powershell (doesnt work as of now))", required=True)
    parser.add_argument("--file_system", help="The file system you want to generate (ext4 (for now))", required=True)
    parser.add_argument("--format_yaml", help="The yaml file in which the specifics of the filesystem are specified, such as filenames and directories", required=False)
    parser.add_argument("--os", help="The os files you want on the filesystem (expirimental, not implemented yet)", required=False)
    parser.add_argument("--output_dir", help="The output directory", required=False, default="./output")

    args = parser.parse_args()

    generator = Generator(args)
    generator.main()