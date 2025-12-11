import argparse
# import subprocess
import yaml 
import os
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class Generator():
    def __init__(self, args):
        self.args = args
        self.config = self.load_config()

        self.mod_yaml_paths = []
        self.template_paths = []

    def load_config(self):
        with open("./config/config.json") as f:
            json_dict = json.load(f)

        return json_dict

    def find_template_path(self):
        logging.info("Finding template script to use...")

        for script_lang_ in self.args.script_lang:
            # Getting full script name
            full_name = f"{script_lang_}_{self.args.file_system}"
            
            if script_lang_ == "bash":
                full_name += ".sh"
            elif script_lang_ == "powershell":
                full_name += ".ps1"

            # Getting full path
            script_path = os.path.abspath(f"{os.getcwd()}/template_scripts/{full_name}")

            if os.path.exists(script_path):
                logging.info(f"Found template file to use: {script_path}")

                self.template_paths.append(script_path)
            else:
                logging.error("Template script path not found!")
                logging.info(f"Template script path we tried: {script_path}")

                return False
        
        if len(self.template_paths) == len(self.args.script_lang):
            return True

    
    def find_mod_yaml_path(self):
        logging.info("Finding yaml files...")

        for mod_yaml_name in self.args.yaml:
            yaml_path = os.path.abspath(mod_yaml_name)

            if os.path.exists(yaml_path):
                logging.info(f"Found mod yaml file to use: {yaml_path}")

                self.mod_yaml_paths.append(yaml_path)
            else:
                logging.error("Mod yaml path not found!")
                logging.info(f"Mod yaml path we tried: {yaml_path}")

                return False
        
        if len(self.mod_yaml_paths) == len(self.args.yaml):
            return True
    
    def add_dir(self, placeholder_dir):
        with open(self.find_template_path(), "r") as f:
            content = f.read()
        
        # Split at the placeholder
        before, after = content.split(placeholder_dir, 1)

        # Loop through dir
        text_to_insert = ""

        for dir in self.yaml_file["structure"]["directories"]:
            text_to_insert += "mkdir " + dir["path"] + "\n"

        new_content = before + placeholder_dir + "\n" + text_to_insert + "\n" + after

        # Add to file
        with open(self.find_template_path(), "w") as f:
            f.write(new_content)

    def change_size_name(self):
        with open(self.find_template_path(), "r") as f:
            content = f.read()

        # Replace
        new_content = content.replace("--NAME--", self.yaml_file["filesystem"]["image_name"])
        new_content = new_content.replace("--SIZE--", str(self.yaml_file["filesystem"]["size_mb"]))

        # Add to file
        with open(self.find_template_path(), "w") as f:
            f.write(new_content)

    def generate_script(self, template, yaml_file):
        # Vars
        commands_final = ""
        image_name = ""
        image_size = ""
        
        # Load in files
        with open(template) as template:
            template_copy = template.read()
        
        with open(yaml_file, "r", encoding="utf-8") as f:
            yaml_copy = yaml.safe_load(f)

        # Init vars
        image_name = yaml_copy["filesystem"]["image_name"]
        image_size = yaml_copy["filesystem"]["size_mb"]

        # Go through logic of yaml line by line
        def append_command(self, yaml_file_structure):
            for command in yaml_file_structure:
                for key, val in command.items():

                    if key == "base":
                        for base_image_name in val:
                            base_confirmation = self.base_excists(base_image_name)

                            if base_confirmation:
                                with open(base_confirmation, "r", encoding="utf-8") as f:
                                    base_yaml = yaml.safe_load(f)

                                append_command(self, base_yaml["structure"])
                            else: 
                                logging.warning(f"Base image not found, looked for {base_image_name}")

        append_command(self, yaml_file_structure=yaml_copy["structure"])

        pass

    def base_excists(self, base_name):
        for base_loc_in_config in self.config["system"]["base_location"]:
            base_location = os.path.abspath(f"{base_loc_in_config}{base_name}.yaml")

            if os.path.exists(base_location):
                return base_location
        return False

    def main(self):
        if not self.find_template_path():
            logging.error("Error, closing program...")
            exit(code=1)
        
        if not self.find_mod_yaml_path():
            logging.error("Error, closing program...")
            exit(code=1)

        for template in self.template_paths:
            for yaml_file in self.mod_yaml_paths:
                self.generate_script(template=template, yaml_file=yaml_file)
        pass

        


def parse_list(value):
    return value.split(",")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--script_lang", help="The script language we will generate the code in (bash, powershell (doesnt work as of now))", required=True, type=parse_list)
    parser.add_argument("--file_system", help="The file system you want to generate (ext4 (for now))", required=True)

    parser.add_argument("--yaml", help="The yaml file which will specify all modifications (besides the mod file) like directories, files etc.", required=True, type=parse_list)

    parser.add_argument("--output_dir", help="The output directory", required=False, default="./output")

    args = parser.parse_args()

    generator = Generator(args)
    generator.main()