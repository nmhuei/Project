--window#!/bin/bash

NUM=5   # số terminal muốn mở

for i in $(seq 1 $NUM); do
    gnome-terminal --window -- bash -c "
        echo '=== RUN $i ===';
        source ~/Project/CTF/.venv/bin/activate

	python Card_Game.py;
        echo '--- DONE ---';
        exec bash
    "
done
