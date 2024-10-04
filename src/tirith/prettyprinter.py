from typing import Dict, List


class TermStyle:
    PURE_RED = "\033[0;31m"
    DARK_GREEN = "\033[0;32m"
    ORANGE = "\033[0;33m"
    DARK_BLUE = "\033[0;34m"
    BRIGHT_PURPLE = "\033[0;35m"
    DARK_CYAN = "\033[0;36m"
    DULL_WHITE = "\033[0;37m"
    PURE_BLACK = "\033[0;30m"
    BRIGHT_RED = "\033[0;91m"
    LIGHT_GREEN = "\033[0;92m"
    YELLOW = "\033[0;93m"
    BRIGHT_BLUE = "\033[0;94m"
    MAGENTA = "\033[0;95m"
    LIGHT_CYAN = "\033[0;96m"
    BRIGHT_BLACK = "\033[0;90m"
    BRIGHT_WHITE = "\033[0;97m"
    CYAN_BACK = "\033[0;46m"
    PURPLE_BACK = "\033[0;45m"
    WHITE_BACK = "\033[0;47m"
    BLUE_BACK = "\033[0;44m"
    ORANGE_BACK = "\033[0;43m"
    GREEN_BACK = "\033[0;42m"
    PINK_BACK = "\033[0;41m"
    GREY_BACK = "\033[0;40m"
    GREY = "\033[38;4;236m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    DARKEN = "\033[2m"
    INVISIBLE = "\033[08m"
    REVERSE_COLOUR = "\033[07m"
    RESET_COLOUR = "\033[0m"
    GREY = "\x1b[90m"

    @staticmethod
    def str_with_style(message: str, color: str) -> str:
        return f"{color}{message}{TermStyle.RESET_COLOUR}"

    @staticmethod
    def success(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.LIGHT_GREEN + TermStyle.BOLD)

    @staticmethod
    def skipped(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.GREY + TermStyle.BOLD)

    @staticmethod
    def fail(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.BRIGHT_RED + TermStyle.BOLD)

    @staticmethod
    def warning(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.YELLOW + TermStyle.BOLD)

    @staticmethod
    def grey(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.GREY)

    @staticmethod
    def green(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.LIGHT_GREEN)

    @staticmethod
    def red(message: str) -> str:
        return TermStyle.str_with_style(message, TermStyle.BRIGHT_RED)


def pretty_print_result_dict(final_result_dict: Dict) -> None:
    """
    Print the `final_result_dict` generated by the core as friendly as possible
    for the user to stdout.

    :param final_result_dict:  Result dictionary generated by core.
    """
    checks = final_result_dict.get("evaluators", [])
    num_passed_checks = 0
    num_failed_checks = 0
    num_skipped_checks = 0

    for check_dict in checks:
        check_id = check_dict["id"]

        if check_dict["passed"]:
            print(TermStyle.success(f"Check: {check_id}"))
            print(f"  {TermStyle.success('PASSED')}")
            num_passed_checks += 1
        elif check_dict["passed"] is None:
            print(TermStyle.skipped(f"Check: {check_id}"))
            print(f"  {TermStyle.skipped('SKIPPED')}")
            num_skipped_checks += 1
        else:
            print(TermStyle.fail(f"Check: {check_id}"))
            print(f"  {TermStyle.fail('FAILED')}")
            num_failed_checks += 1

        for result_num, result_dict in enumerate(check_dict["result"]):
            result_message = result_dict["message"]
            if result_dict["passed"]:
                print(TermStyle.green(f"    {result_num+1}. PASSED: {result_message}"))
            elif check_dict["passed"] is None:
                print(TermStyle.grey(f"    {result_num+1}. SKIPPED: {result_message}"))
            else:
                print(TermStyle.red(f"    {result_num+1}. FAILED: {result_message}"))
        print()

    errors: List[str] = final_result_dict["errors"]
    if errors:
        print(TermStyle.fail("Errors:"))
        for error in errors:
            print(TermStyle.fail(f"- {error}"))
        print()

    print(f"Passed: {num_passed_checks} Failed: {num_failed_checks} Skipped: {num_skipped_checks}")
    print()
    if "eval_expression" in final_result_dict:
        print(f"Final expression used:\n-> {TermStyle.grey(final_result_dict['eval_expression'])}")

    if "final_result" in final_result_dict:
        if final_result_dict["final_result"]:
            print(TermStyle.success("✔ Passed final evaluator"))
        elif final_result_dict["final_result"] is None:
            print(TermStyle.skipped("= Skipped final evaluator"))
        else:
            print(TermStyle.fail("✘ Failed final evaluation"))
