# ♛ Chess Web App

A modern, web-based chess application with AI opponent powered by the Stockfish chess engine. Built with Python Flask backend and a clean, responsive HTML/CSS/JavaScript frontend.

##  What This App Is

This is a complete chess web application that allows you to:
- Play chess against the powerful Stockfish AI engine
- Play with a clean, intuitive drag-and-drop interface
- View real-time move history and game status
- Get hints from Stockfish during your games
- Access your chess games from any device on your home network

Perfect for chess enthusiasts who want a self-hosted, ad-free chess experience with a strong AI opponent.

##  Features

### Core Features
- **Full Chess Implementation**: Complete chess rules, legal move validation, check/checkmate detection
- **Stockfish AI Opponent**: Integrates with the world's strongest open-source chess engine
- **Beautiful UI**: Clean, responsive design that works on desktop and mobile
- **Move History**: Complete game notation with move-by-move history
- **Game Status**: Real-time updates for check, checkmate, and turn indicators
- **Hint System**: Get move suggestions from Stockfish during your games

### Technical Features
- **Python Flask Backend**: Robust, scalable web server
- **REST API**: Clean API endpoints for game management
- **Real-time Updates**: Immediate response to moves and game state changes
- **Cross-platform**: Runs on Windows, Linux, and macOS
- **Home Server Ready**: Designed for self-hosting on your home network

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- Stockfish chess engine binary

### Installation

1. **Clone or Download** this project to your server

2. **Install Python Dependencies**:
   ```bash
   cd chess-webapp
   pip install -r requirements.txt
   ```

3. **Install Stockfish**:
   
   **Easy Installation (Recommended):**
   ```bash
   python install_stockfish.py
   ```
   
   **Manual Installation:**
   
   **On Windows:**
   - Download from [Stockfish Official Site](https://stockfishchess.org/download/)
   - Extract and place `stockfish.exe` in the project directory, or
   - Install to `C:\Program Files\Stockfish\stockfish.exe`

   **On Linux:**
   ```bash
   sudo apt-get install stockfish
   ```

   **On macOS:**
   ```bash
   brew install stockfish
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access Your Chess Game**:
   - Local: http://localhost:5000
   - Network: http://YOUR_SERVER_IP:5000

##  Home Server Deployment

### Running as a Service (Linux)

Create a systemd service for automatic startup:

1. Create service file:
   ```bash
   sudo nano /etc/systemd/system/chess-webapp.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=Chess Web App
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/chess-webapp
   ExecStart=/usr/bin/python3 app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl enable chess-webapp
   sudo systemctl start chess-webapp
   ```

### Network Access Setup

To access from other devices on your network:

1. **Find your server's IP address**:
   ```bash
   # Linux/macOS
   ifconfig
   # Windows
   ipconfig
   ```

2. **Configure your router** (optional):
   - Port forward port 5000 for external access
   - Set up dynamic DNS for remote access

3. **Firewall Configuration**:
   ```bash
   # Linux (ufw)
   sudo ufw allow 5000

   # Windows: Allow Python through Windows Firewall
   ```

##  How to Use

1. **Start a New Game**: Click the "New Game" button to begin
2. **Make Moves**: Click on a piece, then click on a valid destination square
3. **AI Response**: Stockfish will automatically respond with its move
4. **Get Hints**: Use the "Get Hint" button to see Stockfish's suggested move
5. **View History**: Check the move history panel for complete game notation
6. **Game Status**: Monitor check status, turn indicator, and move count

##  Project Structure

```
chess-webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── style.css         # Stylesheet
└── [future files]
    ├── CHANGELOG.md      # Version history (to be created)
    └── .gitignore        # Git exclusions (to be created)
```

##  Configuration

### Stockfish Settings
You can modify Stockfish difficulty in `app.py`:
```python
self.stockfish.set_depth(15)  # Increase for harder AI (slower)
```

### Server Settings
Change host/port in `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Set debug=False for production
```

##  Troubleshooting

### Common Issues

**"Stockfish not found" Error:**
- Ensure Stockfish is installed and in your PATH
- Try specifying the full path in `app.py`:
  ```python
  self.stockfish = Stockfish(path="/full/path/to/stockfish")
  ```

**Can't Access from Other Devices:**
- Check that the server is running with host='0.0.0.0'
- Verify firewall settings
- Ensure devices are on the same network

**Game Not Loading:**
- Check browser console for JavaScript errors
- Verify all static files are being served correctly
- Try refreshing the page

##  Development

### Adding Features
The application is structured for easy extension:
- Game logic: Modify the `ChessGame` class in `app.py`
- Frontend: Update `templates/index.html` and `static/style.css`
- API: Add new routes in `app.py`

### Testing
Currently manual testing via web interface. Future versions may include automated tests.

##  Requirements

### System Requirements
- **Python**: 3.7+
- **RAM**: 512MB minimum (1GB recommended)
- **Storage**: 100MB for application + Stockfish binary
- **Network**: Local network access for multi-device usage

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

##  Security Notes

- This application is designed for home network use
- No user authentication implemented (single-user design)
- Change the secret key in `app.py` for production use
- Consider using HTTPS for external access

##  License

[Add your chosen license here]

##  Contributing

This is a personal project, but suggestions and improvements are welcome!

##  Future Enhancements

Potential features for future versions:
- Multiple game modes (puzzles, time controls)
- User accounts and game history storage
- Tournament brackets
- Analysis board with position evaluation
- Opening book integration
- Mobile app version

---

**Enjoy your self-hosted chess games! ♛**