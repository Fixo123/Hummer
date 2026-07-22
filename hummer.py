#!/data/data/com.termux/files/usr/bin/python3
"""
hammer.py — HTTP Load Generator for Termux
"Test your limits before they test you."
Coded by Fix0 Dev — Terminal Aesthetics Division
"""

import asyncio
import aiohttp
import argparse
import time
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional
import signal

# ─── Color Palette ──────────────────────────────────────────
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK = "\033[30m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"

# ─── Banner ──────────────────────────────────────────────────
BANNER = f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {BOLD}{RED}██████╗ {YELLOW}██╗  {GREEN}██╗ {CYAN}██╗  {BLUE}██╗ {PURPLE}███████╗ {RED}██████╗ {CYAN}║
║  {RED}██╔══██╗{YELLOW}██║  {GREEN}██║ {CYAN}╚██╗{BLUE}██╔╝ {PURPLE}██╔════╝ {RED}██╔══██╗{CYAN}║
║  {RED}██████╔╝{YELLOW}███████║ {CYAN} ╚████╔╝  {PURPLE}█████╗  {RED}██████╔╝{CYAN}║
║  {RED}██╔═══╝ {YELLOW}██╔══██║ {CYAN}  ╚██╔╝   {PURPLE}██╔══╝  {RED}██╔══██╗{CYAN}║
║  {RED}██║     {YELLOW}██║  ██║ {CYAN}   ██║    {PURPLE}███████╗{RED}██║  ██║{CYAN}║
║  {RED}╚═╝     {YELLOW}╚═╝  ╚═╝ {CYAN}   ╚═╝    {PURPLE}╚══════╝{RED}╚═╝  ╚═╝{CYAN}║
║                                                              ║
║        {BOLD}{WHITE}⚡ LOAD GENERATOR v2.0 — TERMUX EDITION ⚡{WHITE}         {CYAN}║
║        {ITALIC}{YELLOW}Test your limits before they test you{YELLOW}{ITALIC}          {CYAN}║
║                                                              ║
║        {BOLD}{GREEN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{GREEN}{BOLD}        {CYAN}║
║        {DIM}{WHITE}🔧 Coded by {BOLD}{RED}Fix0 Dev{WHITE}{DIM} — Terminal Aesthetics Division{WHITE}{DIM}  {CYAN}║
║        {DIM}{WHITE}📡 Protocol: HTTP/HTTPS  |  ⚙️  Engine: asyncio{WHITE}{DIM}     {CYAN}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""

class Hammer:
    def __init__(self, url: str, concurrency: int = 50, duration: int = 10):
        self.url = url
        self.concurrency = concurrency
        self.duration = duration
        self.results = []
        self.running = True
        self.request_count = 0
        self.start_time = 0
        signal.signal(signal.SIGINT, self._shutdown)

    def _shutdown(self, sig, frame):
        print(f"\n{YELLOW}⚠️  Shutting down gracefully...{RESET}")
        self.running = False

    async def _make_request(self, session: aiohttp.ClientSession, id: int) -> Dict:
        start = time.time()
        try:
            async with session.get(self.url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                elapsed = time.time() - start
                return {
                    "id": id,
                    "status": resp.status,
                    "elapsed": elapsed,
                    "success": resp.status < 400,
                    "error": None
                }
        except asyncio.TimeoutError:
            return {
                "id": id,
                "status": 0,
                "elapsed": time.time() - start,
                "success": False,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "id": id,
                "status": 0,
                "elapsed": time.time() - start,
                "success": False,
                "error": str(e)[:50]
            }

    async def run(self):
        os.system('clear')
        print(BANNER)
        
        # ─── Target Info ──────────────────────────────────────
        print(f"{CYAN}┌{'─'*53}┐{RESET}")
        print(f"{CYAN}│{RESET} {BOLD}🎯 TARGET{RESET}{' ' * 42}{CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}   {WHITE}URL:{RESET}        {BOLD}{self.url}{RESET}{' ' * (37 - len(self.url))}{CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}   {WHITE}Concurrency:{RESET} {BOLD}{self.concurrency}{RESET} connections{' ' * (26 - len(str(self.concurrency)))}{CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}   {WHITE}Duration:{RESET}    {BOLD}{self.duration}{RESET} seconds{' ' * (28 - len(str(self.duration)))}{CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}   {WHITE}Status:{RESET}      {GREEN}●{RESET} READY{' ' * 32}{CYAN}│{RESET}")
        print(f"{CYAN}└{'─'*53}┘{RESET}")
        print(f"\n{YELLOW}⚡ Press {BOLD}Ctrl+C{RESET}{YELLOW} to stop early{RESET}\n")

        self.start_time = time.time()
        req_id = 0
        pending = set()
        connector = aiohttp.TCPConnector(limit=self.concurrency * 2)
        timeout = aiohttp.ClientTimeout(total=None)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while self.running and (time.time() - self.start_time) < self.duration:
                while len(pending) < self.concurrency and self.running:
                    req_id += 1
                    task = asyncio.create_task(self._make_request(session, req_id))
                    pending.add(task)

                done, pending = await asyncio.wait(
                    pending,
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=0.5
                )

                for task in done:
                    result = task.result()
                    self.results.append(result)
                    self.request_count += 1
                    
                    elapsed = time.time() - self.start_time
                    progress = min(elapsed / self.duration, 1.0)
                    bar_length = 40
                    filled = int(bar_length * progress)
                    
                    # ─── Gradient Bar ────────────────────────
                    if progress < 0.33:
                        bar_color = RED
                    elif progress < 0.66:
                        bar_color = YELLOW
                    else:
                        bar_color = GREEN
                    
                    bar = f"{bar_color}{'█' * filled}{WHITE}{'░' * (bar_length - filled)}{RESET}"
                    
                    # ─── Live Stats ──────────────────────────
                    success_rate = 0
                    if self.request_count > 0:
                        success_rate = sum(1 for r in self.results if r["success"]) / self.request_count * 100
                    
                    avg_time = 0
                    if self.request_count > 0:
                        times = [r["elapsed"] for r in self.results if r["success"]]
                        if times:
                            avg_time = sum(times) / len(times) * 1000
                    
                    sys.stdout.write(
                        f"\r{CYAN}┃{RESET} {bar} {CYAN}┃{RESET} "
                        f"{BOLD}{self.request_count:6d}{RESET} req  "
                        f"{GREEN}{success_rate:5.1f}%{RESET} OK  "
                        f"{WHITE}{avg_time:5.1f}ms{RESET}  "
                        f"{DIM}{elapsed:4.1f}s/{self.duration}s{RESET}"
                    )
                    sys.stdout.flush()

                await asyncio.sleep(0.01)

            # Cancel remaining tasks
            for task in pending:
                task.cancel()

        print("\n\n")
        self._print_summary()

    def _print_summary(self):
        total = len(self.results)
        if total == 0:
            print(f"{RED}✖ No requests completed.{RESET}")
            return

        success = sum(1 for r in self.results if r["success"])
        failed = total - success
        times = [r["elapsed"] for r in self.results if r["success"]]
        errors = [r["error"] for r in self.results if r["error"]]
        error_counts = {}
        for err in errors:
            if err:
                error_counts[err] = error_counts.get(err, 0) + 1

        # ─── Summary Box ────────────────────────────────────
        print(f"{CYAN}╔{'═'*55}╗{RESET}")
        print(f"{CYAN}║{RESET} {BOLD}{GREEN}✅ STRESS TEST COMPLETE{RESET}{' ' * 31}{CYAN}║{RESET}")
        print(f"{CYAN}╠{'═'*55}╣{RESET}")
        
        print(f"{CYAN}║{RESET} {WHITE}📊 Total Requests:{RESET}  {BOLD}{total:8d}{RESET}{' ' * 25}{CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {WHITE}✅ Successful:{RESET}      {BOLD}{GREEN}{success:8d}{RESET}  {GREEN}({success/total*100:5.1f}%){RESET}{' ' * 14}{CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {WHITE}❌ Failed:{RESET}          {BOLD}{RED}{failed:8d}{RESET}  {RED}({failed/total*100:5.1f}%){RESET}{' ' * 14}{CYAN}║{RESET}")
        
        if times:
            avg = sum(times) / len(times) * 1000
            p95 = sorted(times)[int(len(times) * 0.95)] * 1000 if times else 0
            print(f"{CYAN}║{RESET} {WHITE}⚡ Avg Response:{RESET}    {BOLD}{avg:7.1f}{RESET} ms{' ' * 22}{CYAN}║{RESET}")
            print(f"{CYAN}║{RESET} {WHITE}📈 95th Percentile:{RESET} {BOLD}{p95:7.1f}{RESET} ms{' ' * 22}{CYAN}║{RESET}")
            print(f"{CYAN}║{RESET} {WHITE}📉 Min Response:{RESET}    {BOLD}{min(times)*1000:7.1f}{RESET} ms{' ' * 22}{CYAN}║{RESET}")
            print(f"{CYAN}║{RESET} {WHITE}📈 Max Response:{RESET}    {BOLD}{max(times)*1000:7.1f}{RESET} ms{' ' * 22}{CYAN}║{RESET}")
        
        # ─── Error Breakdown ──────────────────────────────
        if error_counts:
            print(f"{CYAN}╠{'═'*55}╣{RESET}")
            print(f"{CYAN}║{RESET} {YELLOW}⚠️  Error Breakdown:{RESET}{' ' * 32}{CYAN}║{RESET}")
            for err, count in list(error_counts.items())[:3]:
                err_short = err[:30] + "..." if len(err) > 30 else err
                print(f"{CYAN}║{RESET}   {RED}✖{RESET} {err_short:<30} {BOLD}{count:3d}x{RESET}{' ' * 13}{CYAN}║{RESET}")
        
        print(f"{CYAN}╠{'═'*55}╣{RESET}")
        
        # ─── Report ────────────────────────────────────────
        filename = f"hammer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump({
                "target": self.url,
                "concurrency": self.concurrency,
                "duration": self.duration,
                "total_requests": total,
                "success_rate": success/total,
                "avg_response_ms": avg if times else 0,
                "p95_response_ms": p95 if times else 0,
                "results": self.results,
                "errors": error_counts
            }, f, indent=2)
        
        print(f"{CYAN}║{RESET} {GREEN}💾 Report saved:{RESET} {BOLD}{filename}{RESET}{' ' * (32 - len(filename))}{CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {ITALIC}{DIM}🔧 Coded by Fix0 Dev — Terminal Aesthetics Division{DIM}{ITALIC}{' ' * 7}{CYAN}║{RESET}")
        print(f"{CYAN}╚{'═'*55}╝{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Hammer — HTTP Load Generator for Termux",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"{CYAN}🔧 Coded by {RED}Fix0 Dev{CYAN} — Terminal Aesthetics Division{RESET}"
    )
    parser.add_argument("url", help="Target URL (e.g., http://192.168.1.100:8080)")
    parser.add_argument("-c", "--concurrency", type=int, default=50,
                       help=f"{YELLOW}Concurrent requests (default: 50){RESET}")
    parser.add_argument("-d", "--duration", type=int, default=10,
                       help=f"{YELLOW}Test duration in seconds (default: 10){RESET}")
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        args.url = "http://" + args.url

    hammer = Hammer(args.url, args.concurrency, args.duration)
    asyncio.run(hammer.run())

if __name__ == "__main__":
    main()
