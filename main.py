from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

if __name__ == "__main__":
    run_agent("Review all open PRs in rakeshkumar2002/rk-terminal-portfolio")