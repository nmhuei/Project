#!/usr/bin/env python3
import subprocess
import shlex
import sys

def parse_command(cmd):
    """
    Parse command line:
    - pipe |
    - input redirection <
    - output redirection >
    """
    tokens = shlex.split(cmd)

    commands = []
    current = []
    infile = None
    outfile = None

    it = iter(tokens)
    for tok in it:
        if tok == "|":
            commands.append(current)
            current = []
        elif tok == "<":
            infile = next(it, None)
        elif tok == ">":
            outfile = next(it, None)
        else:
            current.append(tok)

    commands.append(current)
    return commands, infile, outfile


def run_command(cmdline):
    commands, infile, outfile = parse_command(cmdline)

    processes = []
    prev_stdout = None

    for i, cmd in enumerate(commands):
        stdin = prev_stdout
        stdout = subprocess.PIPE

        # input redirection (only for first command)
        if i == 0 and infile:
            stdin = open(infile, "r")

        # output redirection (only for last command)
        if i == len(commands) - 1 and outfile:
            stdout = open(outfile, "w")

        p = subprocess.Popen(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE,
            text=True
        )

        if prev_stdout:
            prev_stdout.close()

        prev_stdout = p.stdout
        processes.append(p)

    # get output of last process
    out, err = processes[-1].communicate()

    if out:
        print(out, end="")
    if err:
        print(err, file=sys.stderr)


def shell():
    while True:
        try:
            cmd = input("pysh> ").strip()
            if not cmd:
                continue
            if cmd in ("exit", "quit"):
                break

            run_command(cmd)

        except KeyboardInterrupt:
            print()
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    shell()
