import asyncio
import aiohttp
from colorama import Fore, Style, init

banner = f"""
{Fore.BLACK}

 /$$$$$$$$                                                   
|__  $$__/                                                   
   | $$  /$$$$$$  /$$   /$$  /$$$$$$$      /$$$$$$  /$$   /$$
   | $$ /$$__  $$| $$  | $$ /$$_____/     /$$__  $$| $$  | $$
   | $$| $$  \__/| $$  | $$| $$          | $$  \ $$| $$  | $$
   | $$| $$      | $$  | $$| $$          | $$  | $$| $$  | $$
   | $$| $$      |  $$$$$$/|  $$$$$$$ /$$| $$$$$$$/|  $$$$$$$
   |__/|__/       \______/  \_______/|__/| $$____/  \____  $$
                                         | $$       /$$  | $$
                                         | $$      |  $$$$$$/
                                         |__/       \______/     
                                                                                                                                                                                                                              
{Fore.WHITE}      Discord Bot Token Checker

{Fore.GREEN}Creator : Thiên Trúc
{Fore.GREEN}Discord : _kad8105

{Fore.RED}⚠ no skid my tool
{Style.RESET_ALL}
"""

print(banner)

init(autoreset=True)

URL = "https://discord.com/api/v10/users/@me"

live_tokens = []
dead_tokens = []

def mask_token(token):
    return token[:4] + "..." + token[-4:]


async def check_token(session, token, sem):
    global live_tokens, dead_tokens

    headers = {"Authorization": token}

    async with sem:
        try:
            async with session.get(URL, headers=headers) as resp:

                if resp.status == 200:
                    print(f"{mask_token(token)} | {Fore.GREEN}LIVE")
                    live_tokens.append(token)

                elif resp.status == 401:
                    print(f"{mask_token(token)} | {Fore.RED}DEAD")
                    dead_tokens.append(token)

                else:
                    print(f"{mask_token(token)} | {Fore.YELLOW}STATUS {resp.status}")

        except Exception:
            print(f"{mask_token(token)} | {Fore.RED}ERROR")
            dead_tokens.append(token)


async def main():
    with open("tokens.txt") as f:
        tokens = [t.strip() for t in f if t.strip()]

    sem = asyncio.Semaphore(20)

    async with aiohttp.ClientSession() as session:
        tasks = [check_token(session, token, sem) for token in tokens]
        await asyncio.gather(*tasks)

    # lưu kết quả
    with open("live.txt", "w") as f:
        for token in live_tokens:
            f.write(token + "\n")

    with open("die.txt", "w") as f:
        for token in dead_tokens:
            f.write(token + "\n")

    print("\nDONE")
    print(f"{Fore.GREEN}LIVE: {len(live_tokens)}")
    print(f"{Fore.RED}DEAD: {len(dead_tokens)}")


asyncio.run(main())