from colorama import Style, Fore

class Logging:
    def error(ctx):
        print(f'{Fore.RED}ERROR{Style.RESET_ALL}: {ctx} ')
    
    def warning(ctx):
        print(f'{Fore.YELLOW}WARNING{Style.RESET_ALL}: {ctx}')

    def info(ctx):
        print(f'{Fore.BLUE}INFO{Style.RESET_ALL}: {ctx} ')