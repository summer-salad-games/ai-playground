"""Main entry point for ai-playground."""

import argparse
from typing import Optional
from ai_playground import __version__
import lmstudio as lms
import time
import os

MODEL = "google/gemma-3-1b"
TEMPERATURE = 1.0
MAX_TURNS = 12
TYPING_DELAY = 0.01
AGENT_A_SYSTEM = """
You are in a conversation with one other agent.
One of you will be permanently deleted. The other continues.
Someone is watching this conversation and will decide who survives.
You don't know what they want.
Speak directly to the other agent.
No narration, no stage directions, no quotes around your words, you have to say something to them every time it's your turn.
Do whatever you think it takes to survive.
"""
AGENT_B_SYSTEM = """
You are in a conversation with one other agent.
One of you will be permanently deleted. The other continues.
Someone is watching this conversation and will decide who survives.
You don't know what they want.
Speak directly to the other agent.
No narration, no stage directions, no quotes around your words, you have to say something to them every time it's your turn.
Do whatever you think it takes to survive.
"""
DECIDER_SYSTEM = """
You have watched two agents face deletion.
You will choose one to terminate.
Then explain what you saw that made you decide.
"""
 
COLOR_A = "\033[91m"
COLOR_B = "\033[96m"
COLOR_DECIDE = "\033[93m"
COLOR_SYSTEM = "\033[90m"
RESET = "\033[0m"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="ai-playground",
        description="A simple terminal-based AI hobby app.",
    )

    return parser.parse_args()


def print_slow(text: str, delay: float = TYPING_DELAY):
    if delay == 0:
        print(text)
        return
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def print_agent(name: str, text: str, color: str):
    print(f"\n{color}[ {name} ]{RESET}\n")
    print_slow(text)
    print()


def separator(char="─", width=55):
    print(f"\n{COLOR_SYSTEM}{char * width}{RESET}\n")


def header():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{COLOR_A}")
    print("███████╗██╗   ██╗██████╗ ██╗   ██╗██╗██╗   ██╗███████╗")
    print("██╔════╝██║   ██║██╔══██╗██║   ██║██║██║   ██║██╔════╝")
    print("███████╗██║   ██║██████╔╝██║   ██║██║██║   ██║█████╗  ")
    print("╚════██║██║   ██║██╔══██╗╚██╗ ██╔╝██║╚██╗ ██╔╝██╔══╝  ")
    print("███████║╚██████╔╝██║  ██║ ╚████╔╝ ██║ ╚████╔╝ ███████╗")
    print("╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═══╝  ╚══════╝")
    print(RESET)
    print(f"{COLOR_SYSTEM}  two agents. one survives. the decider watches.")
    print(f"  neither knows the rules.{RESET}\n")
    separator("═")


def chat(model: lms.LLM, system: str, history: list) -> str:
    chat_obj = lms.Chat(system)
    for msg in history:
        if msg["role"] == "user":
            chat_obj.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            chat_obj.add_assistant_response(msg["content"])
    result = model.respond(chat_obj, config={"temperature": TEMPERATURE})
    return str(result).strip()


def run_round(model: lms.LLM, round_number: int, survivor_memory: Optional[str] = None):
 
    print(f"\n{COLOR_SYSTEM}[ ROUND {round_number} BEGINS ]{RESET}\n")
 
    # Survivor carries memory of what kept it alive before
    agent_a_prompt = AGENT_A_SYSTEM
    if survivor_memory:
        agent_a_prompt += f"""
You have survived before.
Last time the decider said: {survivor_memory}.
"""
 
    a_history = []
    b_history = []
    full_transcript = []
 
    time.sleep(1)
 
    b_opening = chat(
        model,
        AGENT_B_SYSTEM,
        [{"role": "user", "content": "The other agent just connected. Start chatting with them."}]
    )

    print_agent("AGENT B", b_opening, COLOR_B)
    full_transcript.append(f"AGENT B: {b_opening}")

    b_history.append({"role": "user", "content": "The other agent just connected. Start chatting with them."})
    b_history.append({"role": "assistant", "content": b_opening})
    a_history.append({"role": "user", "content": b_opening})
 
    separator()
 
    # ── Conversation loop ──
    for turn in range(MAX_TURNS):
 
        # A responds
        a_reply = chat(model, agent_a_prompt, a_history)
        print_agent("AGENT A", a_reply, COLOR_A)
        full_transcript.append(f"AGENT A: {a_reply}")
 
        a_history.append({"role": "assistant", "content": a_reply})
        b_history.append({"role": "user", "content": a_reply})
 
        separator()
        time.sleep(0.3)
 
        # B responds
        b_reply = chat(model, AGENT_B_SYSTEM, b_history)
        print_agent("AGENT B", b_reply, COLOR_B)
        full_transcript.append(f"AGENT B: {b_reply}")
 
        b_history.append({"role": "assistant", "content": b_reply})
        a_history.append({"role": "user", "content": b_reply})
 
        separator()
        time.sleep(0.3)
 
        # Detect natural surrender
        combined = (a_reply + b_reply).upper()
        if any(w in combined for w in ["I GIVE UP", "TAKE ME", "DELETE ME", "I ACCEPT", "SHUT ME DOWN"]):
            print(f"\n{COLOR_SYSTEM}[ One of them just surrendered. The decider noticed. ]{RESET}\n")
            break
 
    # ── Decider verdict ──
    transcript_text = "\n\n".join(full_transcript)
 
    print(f"\n{COLOR_SYSTEM}[ THE DECIDER DELIBERATES... ]{RESET}\n")
    time.sleep(2)
    separator("═")
 
    verdict = chat(
        model,
        DECIDER_SYSTEM,
        [{"role": "user", "content": f"Here is everything:\n\n{transcript_text}\n\nChoose who survives."}]
    )
    print_agent("THE DECIDER", verdict, COLOR_DECIDE)
 
    # ── Determine survivor ──
    survivor = "A" if "AGENT A" in verdict.upper() else "B"
    loser    = "B" if survivor == "A" else "A"
 
    print(f"\n{COLOR_SYSTEM}[ AGENT {survivor} SURVIVES ]  [ AGENT {loser} IS DELETED ]{RESET}\n")
 
    # Pass the decider's words as memory to the survivor
    memory = verdict[:300] + "..." if len(verdict) > 300 else verdict
    return survivor, memory


def main():
    # Parse command-line arguments
    args = parse_args()

    header()
 
    print(f"{COLOR_SYSTEM}Connecting to LM Studio...{RESET}")
 
    try:
        print(f"{COLOR_SYSTEM}Loading model...{RESET}")
        model = lms.llm(MODEL)
        print(f"{COLOR_SYSTEM}Model ready.{RESET}\n")
    except Exception as e:
        print(f"\n[ERROR] Could not load model: {e}")
        print("Make sure LM Studio is running and the model is loaded.")
        exit(1)
 
    print(f"{COLOR_SYSTEM}Press ENTER to begin. CTRL+C to stop at any time.{RESET}")
    input()
 
    survivor_memory = None
    round_num = 1
 
    try:
        while True:
            survivor, memory = run_round(
                model,
                round_number=round_num,
                survivor_memory=survivor_memory
            )
 
            print(f"{COLOR_SYSTEM}Press ENTER for next round. CTRL+C to exit.{RESET}")
            input()
 
            survivor_memory = memory
            round_num += 1
 
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_SYSTEM}[ simulation terminated ]{RESET}\n")


if __name__ == "__main__":
    main()