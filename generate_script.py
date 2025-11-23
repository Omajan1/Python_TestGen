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
        yaml_path = f"{self.args.format_yaml}"
        

    def modify_template(self):
        with open(yaml_path, "r") as f:
            yaml = yaml.safe_load(f)
        
        with open(script_path, "r") as f:
            content = f.read()

        # 2) Create directories
        for d in structure.get("directories", []):
            

        content = content.replace("#PLACEHOLDER#", "paste from loop")


    def main(self):
        script_path = self.find_template()
        self.modify_template(script_path)
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