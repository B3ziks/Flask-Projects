@echo off
echo Select the Flask app to run:
echo 1) PDF Merger
echo 2) Todo List
echo 3) Background Remover
echo 4) Bookmarks

set /p app_choice=Enter your choice:

if "%app_choice%"=="1" (
  .venv\Scripts\activate
  python pdf_merger.py
  .venv\Scripts\deactivate
) else if "%app_choice%"=="2" (
  cd todo
  ..\.venv\Scripts\activate
  python todo_list.py
  ..\.venv\Scripts\deactivate
  cd ..
) else if "%app_choice%"=="3" (
  .venv\Scripts\activate
  python background_remover.py
  .venv\Scripts\deactivate
) else if "%app_choice%"=="4" (
  cd bookmarks
  ..\.venv\Scripts\activate
  python bookmarks.py
  ..\.venv\Scripts\deactivate
  cd ..
) else (
  echo Invalid choice.
)