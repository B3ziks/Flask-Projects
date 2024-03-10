#!/bin/bash

# Function to activate .venv and run a python script
run_flask_app() {
  source .venv/bin/activate
  cd "$1" || exit
  python "$2"
  deactivate
  cd ..
}

echo "Select the Flask app to run:"
echo "1) PDF Merger"
echo "2) Todo List"
echo "3) Background Remover"
echo "4) Bookmarks"

read -r app_choice

case $app_choice in
  1)
    run_flask_app "." "pdf_merger.py"
    ;;
  2)
    run_flask_app "todo" "todo_list.py"
    ;;
  3)
    run_flask_app "." "background_remover.py"
    ;;
  4)
    run_flask_app "bookmarks" "bookmarks.py"
    ;;
  *)
    echo "Invalid choice."
    ;;
esac