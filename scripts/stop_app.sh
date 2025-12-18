#!/bin/bash
echo "Stopping O&M Assistant..."

# Find and kill streamlit processes
pkill -f "streamlit run" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Streamlit processes stopped"
else
    echo "No streamlit processes found"
fi

# Kill processes using port 8501
lsof -ti:8501 | xargs kill -9 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Processes using port 8501 stopped"
else
    echo "No processes using port 8501"
fi

echo "O&M Assistant stopped"