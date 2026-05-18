from colorama import init, Fore, Style
from collectors import collect_all_reviews
from analyzer   import generate_final_review

init(autoreset=True)


def banner():
    print(Fore.CYAN + """
╔══════════════════════════════════════════════════════╗
║        🔍  AI Product Review Analyzer  🔍            ║
║   Google · YouTube · Amazon · Gemini · Groq          ║
╚══════════════════════════════════════════════════════╝
""")


def show_result(result):
    if "error" in result:
        print(Fore.RED + f"\n❌  {result['error']}\n")
        return

    sep = "═" * 60
    print(Fore.GREEN  + f"\n{sep}")
    print(Fore.YELLOW + f"  📦  PRODUCT  : {result['product'].upper()}")
    print(Fore.WHITE  + f"  📊  Reviews  : {result['total_reviews_analyzed']}")
    print(Fore.WHITE  + f"  🌐  Sources  : {', '.join(result['sources'])}")
    print(Fore.GREEN  + sep)

    print(Fore.CYAN   + "\n✨  GEMINI AI ANALYSIS\n" + "─" * 60)
    print(Fore.WHITE  + result["gemini_analysis"])

    print(Fore.MAGENTA + "\n⚡  GROQ AI ANALYSIS\n" + "─" * 60)
    print(Fore.WHITE   + result["groq_analysis"])

    print(Fore.YELLOW + "\n🚀  STEP 4 — MARKETING OUTPUT\n" + "─" * 60)
    print(Fore.WHITE + result["marketing_content"])

    if result["links"]:
        print(Fore.BLUE + "\n🔗  Source Links\n" + "─" * 60)
        for idx, link in enumerate(result["links"], 1):
            print(Fore.BLUE + f"  {idx}. {link}")

    print(Fore.GREEN + f"\n{sep}\n")


def main():
    banner()

    while True:
        print(Fore.WHITE + "Enter product name (or 'quit' to exit):")
        product = input(Fore.YELLOW + "  >> ").strip()

        if product.lower() in ("quit", "exit", "q"):
            print(Fore.CYAN + "\n👋  Bye! Keep reviewing.\n")
            break

        if not product:
            print(Fore.RED + "  ⚠️   Product name cannot be empty!\n")
            continue

        reviews = collect_all_reviews(product)
        result  = generate_final_review(product, reviews)
        show_result(result)

        again = input(Fore.WHITE + "Analyze another product? (y/n): ").strip().lower()
        if again != "y":
            print(Fore.CYAN + "\n👋  Bye!\n")
            break


if __name__ == "__main__":
    main()