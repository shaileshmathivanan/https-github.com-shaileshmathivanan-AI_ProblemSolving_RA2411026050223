# Tic-Tac-Toe AI

This project is a web-based Tic-Tac-Toe game powered by an AI that uses Minimax and Alpha-Beta pruning algorithms to determine the best moves. The game is built using Flask for the backend and includes a simple user interface.

## Features

- Play against an AI that uses advanced algorithms to make decisions.
- Reset the game board at any time.
- View the performance comparison between the two AI algorithms.

## Project Structure

```
tic-tac-toe-ai
├── app.py               # Main Flask application
├── ai.py                # AI logic for Tic-Tac-Toe
├── templates            # HTML templates
│   └── index.html      # Game UI template
├── static               # Static files (CSS, JS)
│   ├── css
│   │   └── styles.css   # Styles for the game UI
│   └── js
│       └── app.js       # JavaScript for game interactions
├── docs                 # Documentation files
│   ├── index.html       # Documentation homepage
│   └── assets
│       ├── css
│       │   └── styles.css # Styles for documentation
│       └── js
│           └── app.js     # JavaScript for documentation
├── requirements.txt     # Python dependencies
├── .gitignore           # Files to ignore in Git
├── .github
│   └── workflows
│       └── deploy.yml    # GitHub Actions for deployment
├── LICENSE              # Licensing information
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tic-tac-toe-ai.git
   cd tic-tac-toe-ai
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000` to play the game.

## Usage

- Select your player (X or O) and start playing against the AI.
- You can reset the game at any time using the reset button.
- The AI will make its move based on the selected algorithm (Minimax or Alpha-Beta).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.