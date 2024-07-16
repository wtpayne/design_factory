while true; do
    # Wait for the file to change
    inotifywait -e modify README.md

    # Run the mermaid command
    mmdc -i README.md -o README.png --width 2048 --height 2048 --scale 2

    # Optionally, you can add a sleep command to prevent rapid execution
    # sleep 1
done