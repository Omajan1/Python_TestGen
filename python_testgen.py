import argparse


class Generator():
    def __init__(self, args):
        self.args = args

    def main():
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", help="The name of the script being outputted", required=True)
    parser.add_argument("--script_lang", help="The script language we will generate the code in (bash, powershell (doesnt work as of now))", required=True)
    parser.add_argument("--size", help="The size of the image being outputted (format=[num][M v G], M is MB, G is GB. 'num' is the amount) (50M, 2G)", required=True)
    parser.add_argument("--file_system", help="The file system you want to generate (ext4 (for now))", required=True)
    parser.add_argument("--format_yaml", help="The yaml file in which the specifics of the filesystem are specified, such as filenames and directories", required=True)
    parser.add_argument("--os", help="The os files you want on the filesystem (expirimental, not implemented yet)", required=True)
    parser.add_argument("--output_file", help="The output directory", required=False, default="./output")

    args = parser.parse_args()

    generator = Generator(args)
    generator.main()