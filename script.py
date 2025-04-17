import argparse
import sys
import time
import shlex


class InteractiveCLI:
    def __init__(self, prompt: str = "> ", version: str = "1.0.0"):
        self.prompt = prompt
        self.version = version
        self.running = False
        self.parser = self.create_parser()

    def create_parser(self):
        """创建参数解析器"""
        parser = argparse.ArgumentParser(
            description="An interactive command-line program with typewriter effect.",
            add_help=False
        )

        parser.add_argument(
            "-h", "--help",
            action="store_true",
            help="show this help message and exit"
        )
        parser.add_argument(
            "-v", "--version",
            action="store_true",
            help="show program's version number and exit"
        )
        parser.add_argument(
            "-p", "--prompt",
            dest="prompt",
            type=str,
            help="temporarily change the command prompt"
        )

        return parser

    def typewriter_effect(self, text: str, delay: float = 0.1):
        """模拟打字机效果输出文本"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def echo_input(self, user_input: str):
        """回显用户输入"""
        print(f"\033[3m\033[90mUser: {user_input}\033[0m")

    def show_version(self):
        """显示版本信息"""
        self.typewriter_effect(f"Interactive CLI Version {self.version}")

    def show_help(self):
        """显示帮助信息"""
        help_text = """
Available commands:
  help                  - Show this help message
  version               - Show program version
  exit/quit             - Exit the program
  python script.py [options] - Execute as command line args
Options:
  -h, --help           - Show help
  -v, --version        - Show version
  -p PROMPT, --prompt PROMPT - Change prompt temporarily
"""
        self.typewriter_effect(help_text)

    def handle_cli_args(self, args_str: str):
        """处理交互模式下输入的类命令行参数"""
        try:
            # 使用shlex来正确处理带引号的参数
            args = self.parser.parse_args(shlex.split(args_str)[2:])  # 跳过"python script.py"

            if args.help:
                self.show_help()
            elif args.version:
                self.show_version()
            elif args.prompt:
                old_prompt = self.prompt
                self.prompt = args.prompt
                self.typewriter_effect(f"Prompt changed from '{old_prompt}' to '{self.prompt}'")

        except SystemExit:
            # 防止argparse调用sys.exit()
            pass
        except Exception as e:
            self.typewriter_effect(f"Error parsing arguments: {str(e)}")

    def start(self):
        """启动交互式会话"""
        self.running = True
        self.typewriter_effect(f"Interactive CLI (Version {self.version})")
        self.typewriter_effect("Type 'help' for available commands.")

        while self.running:
            try:
                user_input = input(self.prompt).strip()

                if not user_input:
                    continue

                self.echo_input(user_input)

                # 检查是否是类命令行输入
                if user_input.startswith("python script.py"):
                    self.handle_cli_args(user_input)
                # 处理内置命令
                elif user_input.lower() in ('exit', 'quit'):
                    self.typewriter_effect("Goodbye!")
                    self.running = False
                elif user_input.lower() == 'version':
                    self.show_version()
                elif user_input.lower() == 'help':
                    self.show_help()
                else:
                    # 处理其他输入
                    response = self.process_input(user_input)
                    self.typewriter_effect(response)

            except KeyboardInterrupt:
                self.typewriter_effect("\nUse 'exit' or 'quit' to end the session.")
            except EOFError:
                self.typewriter_effect("\nGoodbye!")
                self.running = False

    def process_input(self, user_input: str) -> str:
        """处理用户输入并生成响应"""
        return f"System: You said '{user_input}'"


def main():
    # 解析真正的命令行参数
    cli = InteractiveCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    # 处理命令行参数
    if args.help:
        print("Usage: python script.py [options]")
        print("Options:")
        print("  -h, --help     show this help message and exit")
        print("  -v, --version  show program's version number and exit")
        print("  -p PROMPT, --prompt PROMPT")
        print("                set the command prompt (default: '> ')")
        sys.exit(0)

    if args.version:
        cli.show_version()
        sys.exit(0)

    if args.prompt:
        cli.prompt = args.prompt

    # 启动交互模式
    cli.start()


if __name__ == "__main__":
    main()
