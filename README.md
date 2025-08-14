# 🎮 Button Game - The Ultimate Elimination Challenge

A fun, interactive elimination game where players strategically select numbers to avoid being the farthest from the average. Built with Python and Streamlit for seamless browser gameplay.

## 🌟 Features

### 🕹️ Core Gameplay
- Players take turns selecting numbered buttons (0-99)
- System calculates the average of all selections
- Player farthest from the average gets eliminated
- Last remaining player wins!

### 🎯 Special Rules & Mechanics
- **2-Player Mode**: Lowest number wins (equal numbers = both lose)
- **3-Player Mode**: If two choose same number, they lose and third wins
- **Tie-Breakers**: Tied players compete in sudden-death rounds
- **Duplicate Protection**: Players choosing same numbers get eliminated
- **Smart Elimination**: Handles all edge cases automatically

### 🖥️ Technical Highlights
- Beautiful Streamlit interface with animated buttons
- Responsive design works on all devices
- Session state management for smooth gameplay
- Loading animations between screens
- Color-coded visual feedback

## 🚀 How It Works

1. **Setup**: Choose local multiplayer and enter player names
2. **Gameplay**: Each player selects a number when their turn comes
3. **Calculation**: System computes average after all selections
4. **Elimination**: Farthest player(s) get eliminated
5. **Repeat**: Continue until one player remains

## 🛠️ Installation


1. Clone the repository:
```bash
git clone https://github.com/yourusername/button-game.git
cd button-game
```
2.Install dependencies:
```bash
pip install streamlit
```
3.Run the game:
```bash
streamlit run game.py
```

## 🌐 Deployment  

The game is live and playable at:  
🔗 [https://buttongame.streamlit.app/](https://buttongame.streamlit.app/)

## 📜 Rules Summary

- **Strategic Selection**: Choose numbers carefully to stay close to the average  
- **Special Scenarios**: Unique rules for 2-player and 3-player games  
- **Tie Resolution**: Sudden-death rounds for tied players  
- **Duplicate Penalty**: Matching numbers cause instant elimination  
- **Group Elimination**: All lose if identical numbers are chosen  

## 🔮 Future Plans

- [ ] Online multiplayer functionality  
- [ ] Player profiles and statistics tracking  
- [ ] Custom rule configurations  
- [ ] Themed button designs and skins  
- [ ] Competitive tournament mode  

## 🤝 Contributing

Contributions welcome! Please:  
1. Open an issue to discuss proposed changes  
2. Submit pull requests for review  
3. Follow existing code style  

## 📄 License  

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.



