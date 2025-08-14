import streamlit as st
import time
import uuid
from utils import init_session

init_session()
num_cols = 5

# Reusable loading function
def show_loading_screen(message="Loading...", duration=1.5):
    with st.spinner(message):
        time.sleep(duration)

# 🎨 Global Styles
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #f0f0f0;
}
.card-button {
    display: inline-block;
    width: 280px;
    height: 120px;
    margin: 20px;
    padding: 20px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    border-radius: 16px;
    background: linear-gradient(145deg, #1f1f1f, #2c2c2c);
    color: #f0f0f0;
    box-shadow: 0 0 15px rgba(247, 55, 24, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid #F73718;
}
.card-button:hover {
    background: linear-gradient(145deg, #2c2c2c, #1f1f1f);
    box-shadow: 0 0 25px rgba(247, 55, 24, 0.6);
    transform: scale(1.05);
    color: #ffffff;
}
.selected {
    background: linear-gradient(145deg, #F73718, #ff5e3a) !important;
    border: 2px solid #ffffff !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize necessary session state variables if not present
if "page" not in st.session_state:
    st.session_state.page = "home"
if "names" not in st.session_state:
    st.session_state.names = []
if "selections" not in st.session_state:
    st.session_state.selections = []
if "current_player" not in st.session_state:
    st.session_state.current_player = 0
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None
if "eliminated_players" not in st.session_state:
    st.session_state.eliminated_players = []
if "in_tie_breaker" not in st.session_state:
    st.session_state.in_tie_breaker = False
if "active_players" not in st.session_state:
    st.session_state.active_players = []

# � Home Page
if st.session_state.page == "home":
    st.title("🎮 Button Game")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎮 On Same Device"):
            show_loading_screen("Loading local game...")
            st.session_state.page = "player_count"
            st.session_state.mode = "local"
            st.rerun()
    with col2:
        if st.button("🌐 Remote Device"):
            show_loading_screen("Loading remote game...")
            st.session_state.page = "remote_mode"
            st.session_state.mode = "remote"
            st.rerun()
    with col3:
        if st.button("📜 Rules"):
            show_loading_screen("Loading rules...")
            st.session_state.page = "rules"
            st.rerun()

# 📜 Rules Page
if st.session_state.page == "rules":
    st.title("📜 Game Rules")
    
    # Add a home button at the top right
    home_col, _ = st.columns([1, 5])
    with home_col:
        if st.button("🏠 Home", use_container_width=True):
            show_loading_screen("Returning home...")
            st.session_state.page = "home"
            st.rerun()
    
    st.markdown("""
    <div style='background-color: #1f1f1f; padding: 20px; border-radius: 10px; border-left: 5px solid #F73718; margin-top: 20px;'>
        <h3 style='color: #F73718;'>How to Play:</h3>
        <ol>
            <li>Each player selects a button with a number when it's their turn</li>
            <li>The game calculates the average of all selected numbers</li>
            <li>The player whose number is farthest from the average is eliminated</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='margin-top: 30px; background-color: #1f1f1f; padding: 20px; border-radius: 10px; border-left: 5px solid #F73718;'>
        <h3 style='color: #F73718;'>Special Rules:</h3>
        <ol>
            <li><b>Two Players:</b> The player with the lower number wins (if numbers are equal, both lose)</li>
            <li><b>Three Players:</b> If two choose the same number, they lose and the third player wins</li>
            <li><b>Tie-Breaker:</b> If players are tied at the bottom, they play a special round where the lowest number wins</li>
            <li><b>Same Numbers:</b> If all remaining players choose the same number, they're all eliminated</li>
            <li><b>Duplicate Numbers:</b> Players who choose duplicate numbers are immediately eliminated</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional styled home button at the bottom
    if st.button("← Back to Home", key="bottom_home_button"):
        show_loading_screen("Returning home...")
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("← Back to Home"):
        show_loading_screen("Returning home...")
        st.session_state.page = "home"
        st.rerun()

# 👥 Player Count
if st.session_state.page == "player_count":
    st.subheader("Enter Number of Players")
    num_players = st.number_input("Players", min_value=2, max_value=100, step=1)
    if st.button("Continue"):
        show_loading_screen("Loading names input...")
        st.session_state.num_players = num_players
        st.session_state.page = "name_input"
        st.rerun()

# 🧑‍🤝‍🧑 Name Input
if st.session_state.page == "name_input":
    st.subheader("Enter Player Names")
    all_named = True
    names = []
    for i in range(st.session_state.num_players):
        name = st.text_input(f"Player {i+1} Name", max_chars=200, key=f"name_{i}")
        if name.strip() == "":
            all_named = False
        names.append(name.strip())
    st.session_state.names = names
    st.session_state.active_players = names.copy()  # Initialize active players

    # Check for duplicate names (non-empty)
    unique_names = set(n for n in names if n != "")
    has_duplicates = len(unique_names) != len([n for n in names if n != ""])

    if has_duplicates:
        st.error("Player names must be unique. Please fix duplicates.")

    if all_named and not has_duplicates:
        if st.button("Continue"):
            show_loading_screen("Starting game...")
            st.session_state.page = "player_turn"
            st.session_state.current_player = 0
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue Anyway") and not has_duplicates:
                show_loading_screen("Starting game...")
                for i in range(len(names)):
                    if names[i].strip() == "":
                        names[i] = f"Player {i+1}"
                st.session_state.names = names
                st.session_state.active_players = names.copy()
                st.session_state.page = "player_turn"
                st.session_state.current_player = 0
                st.rerun()
        with col2:
            if has_duplicates:
                st.warning("Duplicate names detected. Please enter unique names.")
            else:
                st.warning("Some names are missing.")

# 🎮 Player Turn Page
if st.session_state.page == "player_turn":
    # Only show turn for active players
    active_indices = [i for i, name in enumerate(st.session_state.names) 
                     if name in st.session_state.active_players]
    current_active_index = active_indices[st.session_state.current_player]
    name = st.session_state.names[current_active_index]
    
    st.subheader(f"{name}'s Turn")

    rows = 100 // num_cols
    for row in range(rows):
        cols = st.columns([1] * num_cols)
        for col_idx in range(num_cols):
            idx = row * num_cols + col_idx
            with cols[col_idx]:
                with st.form(f"form_{idx}"):
                    is_selected = st.session_state.get("selected_button") == idx
                    btn_label = f"🕹️ {idx:03}"
                    if st.form_submit_button(btn_label, use_container_width=True):
                        st.session_state.selected_button = idx

                    if is_selected:
                        st.markdown(
                            f"""<style>
                            div[data-testid="stForm"][aria-label="form_{idx}"] {{
                                padding: 10px 20px;
                                background: linear-gradient(145deg, #F73718, #ff5e3a);
                                border: 2px solid #ffffff !important;
                                border-radius: 10px;
                                color: white !important;
                                font-weight: bold;
                            }}
                            </style>""",
                            unsafe_allow_html=True
                        )

    if st.session_state.get("selected_button") is not None:
        if st.button("✅ Submit Selection"):
            show_loading_screen("Submitting selection...")
            st.session_state.selections.append(st.session_state.selected_button)
            st.session_state.selected_button = None
            
            # Move to next active player
            if st.session_state.current_player + 1 < len(active_indices):
                st.session_state.current_player += 1
                st.session_state.page = "player_turn"
            else:
                st.session_state.page = "results"
            st.rerun()

# 📊 Results Page with updated rules
if st.session_state.page == "results":
    if hasattr(st.session_state, 'in_tie_breaker') and st.session_state.in_tie_breaker:
        # This is a tie-breaker round result
        st.session_state.in_tie_breaker = False
        
        # In tie-breaker, the player with smallest number wins (rule 2)
        selections = st.session_state.selections
        min_selection = min(selections)
        winner_idx = selections.index(min_selection)
        winner = st.session_state.names[winner_idx]
        
        # Eliminate all other players in the tie-breaker
        eliminated = [name for i, name in enumerate(st.session_state.names) if i != winner_idx]
        st.session_state.eliminated = eliminated
        
        # Update active players
        st.session_state.active_players = [winner]
        st.session_state.eliminated_players.extend(eliminated)
        
        # Restore main game players and add the tie-breaker winner
        st.session_state.names = st.session_state.main_game_names
        st.session_state.selections = st.session_state.main_game_selections
        
        # Add the winner back to active players
        st.session_state.active_players.append(winner)
        
        # Clear tie-breaker state
        del st.session_state.main_game_names
        del st.session_state.main_game_selections
        
        # If only one player remains (winner plus no others), they win
        if len(st.session_state.active_players) == 1:
            st.session_state.winner = st.session_state.active_players[0]
            st.session_state.page = "winner"
        else:
            st.session_state.page = "elimination"
        st.rerun()
    
    if len(st.session_state.selections) == 0:
        st.error("No selections made. Cannot calculate average.")
        if st.button("Restart"):
            show_loading_screen("Restarting game...")
            st.session_state.page = "home"
            st.session_state.names = []
            st.session_state.selections = []
            st.session_state.current_player = 0
            st.rerun()
    else:
        # Check for rule 5: if all remaining players choose the same number, they all lose
        if len(set(st.session_state.selections)) == 1:
            st.session_state.eliminated = st.session_state.active_players.copy()
            st.session_state.eliminated_players.extend(st.session_state.eliminated)
            st.session_state.active_players = []
            st.session_state.page = "all_eliminated"
            st.rerun()
        
        # Check for rule 4: if 3 players and two choose same number
        if len(st.session_state.active_players) == 3:
            selection_counts = {}
            for sel in st.session_state.selections:
                selection_counts[sel] = selection_counts.get(sel, 0) + 1
            
            # Find if any number was chosen by exactly 2 players
            for num, count in selection_counts.items():
                if count == 2:
                    # The two players who chose this number lose, the other wins
                    eliminated_indices = [i for i, sel in enumerate(st.session_state.selections) if sel == num]
                    st.session_state.eliminated = [name for i, name in enumerate(st.session_state.active_players) if i in eliminated_indices]
                    st.session_state.winner = [name for i, name in enumerate(st.session_state.active_players) if i not in eliminated_indices][0]
                    st.session_state.eliminated_players.extend(st.session_state.eliminated)
                    st.session_state.active_players = [st.session_state.winner]
                    st.session_state.page = "three_player_elimination"
                    st.rerun()
        
        avg = sum(st.session_state.selections) / len(st.session_state.selections)
        diffs = [abs(choice - avg) for choice in st.session_state.selections]

        max_diff = max(diffs)
        min_diff = min(diffs)

        # Find all indices who have max_diff (farthest)
        farthest_indices = [i for i, d in enumerate(diffs) if d == max_diff]
        closest_indices = [i for i, d in enumerate(diffs) if d == min_diff]

        # NEW RULE: If only two players remain, the one with lowest number wins
        if len(st.session_state.active_players) == 2:
            if st.session_state.selections[0] == st.session_state.selections[1]:
                # If both choose same number, eliminate both (rule 5)
                st.session_state.eliminated = st.session_state.active_players.copy()
                st.session_state.eliminated_players.extend(st.session_state.eliminated)
                st.session_state.active_players = []
                st.session_state.page = "all_eliminated"
                st.rerun()
            else:
                # Player with lower number wins
                if st.session_state.selections[0] < st.session_state.selections[1]:
                    winner_idx = 0
                    loser_idx = 1
                else:
                    winner_idx = 1
                    loser_idx = 0
                
                st.session_state.winner = st.session_state.active_players[winner_idx]
                st.session_state.eliminated = [st.session_state.active_players[loser_idx]]
                st.session_state.eliminated_players.extend(st.session_state.eliminated)
                st.session_state.active_players = [st.session_state.winner]
                st.session_state.page = "winner"
                st.rerun()

        # Check for rule 3: if players choose same number, only those who choose same number are eliminated
        selection_counts = {}
        for sel in st.session_state.selections:
            selection_counts[sel] = selection_counts.get(sel, 0) + 1
        
        # Find numbers chosen by more than one player
        duplicate_numbers = [num for num, count in selection_counts.items() if count > 1]
        if duplicate_numbers:
            # Eliminate all players who chose duplicate numbers
            eliminated_indices = [i for i, sel in enumerate(st.session_state.selections) if sel in duplicate_numbers]
            st.session_state.eliminated = [st.session_state.active_players[i] for i in eliminated_indices]
            st.session_state.eliminated_players.extend(st.session_state.eliminated)
            
            # Remove eliminated players from active players
            st.session_state.active_players = [name for i, name in enumerate(st.session_state.active_players) 
                                             if i not in eliminated_indices]
            
            # Update selections to only include active players
            st.session_state.selections = [sel for i, sel in enumerate(st.session_state.selections) 
                                         if i not in eliminated_indices]
            
            # If only one player remains, they win
            if len(st.session_state.active_players) == 1:
                st.session_state.winner = st.session_state.active_players[0]
                st.session_state.page = "winner"
                st.rerun()
            else:
                st.session_state.page = "elimination"
                st.rerun()
        
        # Normal elimination logic
        if len(farthest_indices) > 1:
            # If exactly 2 players are tied at the bottom, they play a tie-breaker
            if len(farthest_indices) == 2:
                st.session_state.tied_players = [st.session_state.active_players[i] for i in farthest_indices]
                st.session_state.tied_indices = farthest_indices
                st.session_state.page = "tie_breaker_explanation"
                st.session_state.tie_breaker_mode = "two_player"
                st.rerun()
            else:
                # For more than 2 tied players, eliminate all but one (smallest number)
                # Find the player with the smallest number among tied players
                tied_selections = [st.session_state.selections[i] for i in farthest_indices]
                min_selection = min(tied_selections)
                winner_idx_in_tied = tied_selections.index(min_selection)
                winner_idx = farthest_indices[winner_idx_in_tied]
                
                # Eliminate all other tied players
                eliminated_indices = [i for i in farthest_indices if i != winner_idx]
                st.session_state.eliminated = [st.session_state.active_players[i] for i in eliminated_indices]
                st.session_state.eliminated_players.extend(st.session_state.eliminated)
                
                # Remove eliminated players from active players
                st.session_state.active_players = [name for i, name in enumerate(st.session_state.active_players) 
                                                 if i not in eliminated_indices]
                
                # Update selections to only include active players
                st.session_state.selections = [sel for i, sel in enumerate(st.session_state.selections) 
                                             if i not in eliminated_indices]
                
                # If only one player remains, they win
                if len(st.session_state.active_players) == 1:
                    st.session_state.winner = st.session_state.active_players[0]
                    st.session_state.page = "winner"
                    st.rerun()
                else:
                    st.session_state.page = "elimination"
                    st.rerun()
        else:
            # No tie, eliminate the farthest player normally
            eliminated_index = farthest_indices[0]
            st.session_state.eliminated = [st.session_state.active_players[eliminated_index]]
            st.session_state.eliminated_players.extend(st.session_state.eliminated)
            
            # Remove from active players
            st.session_state.active_players = [name for i, name in enumerate(st.session_state.active_players) 
                                             if i != eliminated_index]
            
            # Update selections
            st.session_state.selections = [sel for i, sel in enumerate(st.session_state.selections) 
                                         if i != eliminated_index]
            
            # If only one player remains, they win
            if len(st.session_state.active_players) == 1:
                st.session_state.winner = st.session_state.active_players[0]
                st.session_state.page = "winner"
                st.rerun()
            else:
                show_loading_screen("Calculating elimination...")
                st.session_state.page = "elimination"
                st.rerun()

# 🔥 Tie Breaker Explanation Page (updated)
if st.session_state.page == "tie_breaker_explanation":
    tied_players = st.session_state.tied_players
    tied_indices = st.session_state.tied_indices
    selections = st.session_state.selections
    avg = sum(selections) / len(selections) if len(selections) > 0 else 0

    # Calculate original distances for context
    original_distances = []
    for i in tied_indices:
        if i < len(selections):
            dist = abs(selections[i] - avg)
            original_distances.append(dist)
        else:
            original_distances.append(0)

    if st.session_state.tie_breaker_mode == "two_player":
        rule_used = "Rule: Two players are tied at the bottom. They will play a tie-breaker round."
        tie_desc = "The two tied players will play a special round. The loser will be eliminated; the winner will continue in the game."
    else:
        rule_used = "Rule: Multiple players tied at the bottom after immediate eliminations."
        tie_desc = "These players will play a tie-breaker round to decide who gets eliminated."

    st.markdown(
        f"""
        <div style='text-align:center; padding:40px;'>
            <h1 style='color:#F73718;'>Tie Breaker!</h1>
            <p style='font-size:20px;'><b>{rule_used}</b></p>
            <p style='font-size:18px;'>{tie_desc}</p>
            <p style='font-size:18px;'>Players in the tie-breaker:</p>
            <ul style='list-style:none; font-size:18px;'>
        """,
        unsafe_allow_html=True
    )

    for player, dist in zip(tied_players, original_distances):
        st.markdown(
            f"<li><b>{player}</b> — Original Distance: <span style='color:#F73718;'>{dist:.2f}</span></li>",
            unsafe_allow_html=True,
        )

    st.markdown("</ul></div>", unsafe_allow_html=True)

    if st.button("Start Tie-Breaker"):
        # Save the current game state (non-tied players)
        st.session_state.main_game_names = [name for name in st.session_state.active_players 
                                          if name not in tied_players]
        st.session_state.main_game_selections = [sel for i, sel in enumerate(st.session_state.selections) 
                                              if i not in tied_indices]
        
        # Set up tie-breaker round with only tied players
        st.session_state.active_players = tied_players
        st.session_state.selections = []
        st.session_state.current_player = 0
        st.session_state.page = "player_turn"
        st.session_state.in_tie_breaker = True
        st.rerun()

# 💥 Elimination Page (updated)
if st.session_state.page == "elimination":
    eliminated = st.session_state.eliminated
    st.session_state.eliminated_players.extend(eliminated)
    
    # Show elimination message
    st.markdown(
        f"""
        <div style='text-align:center; padding:40px;'>
            <h1 style='font-size:64px; color:#F73718;'>💥 Elimination! 💥</h1>
            <p style='font-size:24px;'>The following players are eliminated:</p>
            <ul style='list-style:none; font-size:24px;'>
        """, 
        unsafe_allow_html=True
    )
    
    for player in eliminated:
        st.markdown(f"<li>❌ {player}</li>", unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

    # Prepare for next round
    if st.button("Next Round"):
        show_loading_screen("Starting next round...")
        st.session_state.page = "player_turn"
        st.session_state.selections = []
        st.session_state.selected_button = None
        st.session_state.current_player = 0
        st.rerun()

# 🏆 Winner Page
if st.session_state.page == "winner":
    st.balloons()
    st.markdown(
        f"<h1 style='text-align:center; font-size:48px; color:#F73718;'>🎉 {st.session_state.winner} WINS! 🎉</h1>",
        unsafe_allow_html=True
    )
    if st.button("Play Again"):
        show_loading_screen("Restarting game...")
        st.session_state.page = "home"
        st.session_state.names = []
        st.session_state.selections = []
        st.session_state.current_player = 0
        st.session_state.selected_button = None
        st.session_state.eliminated_players = []
        st.session_state.active_players = []
        st.rerun()

# 💀 All Eliminated Page (rule 5)
if st.session_state.page == "all_eliminated":
    st.markdown(
        f"""
        <div style='text-align:center; padding:40px;'>
            <h1 style='font-size:64px; color:#F73718;'>💀 All Players Eliminated! 💀</h1>
            <p style='font-size:24px;'>All remaining players chose the same number!</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if st.button("Play Again"):
        show_loading_screen("Restarting game...")
        st.session_state.page = "home"
        st.session_state.names = []
        st.session_state.selections = []
        st.session_state.current_player = 0
        st.session_state.selected_button = None
        st.session_state.eliminated_players = []
        st.session_state.active_players = []
        st.rerun()

# 3️⃣ Three Player Elimination (rule 4)
if st.session_state.page == "three_player_elimination":
    st.markdown(
        f"""
        <div style='text-align:center; padding:40px;'>
            <h1 style='font-size:64px; color:#F73718;'>Three Player Rule Activated!</h1>
            <p style='font-size:24px;'>Two players chose the same number:</p>
            <ul style='list-style:none; font-size:24px;'>
        """, 
        unsafe_allow_html=True
    )
    
    for player in st.session_state.eliminated:
        st.markdown(f"<li>❌ {player}</li>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
            </ul>
            <p style='font-size:32px;'>🎉 {st.session_state.winner} WINS! 🎉</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if st.button("Play Again"):
        show_loading_screen("Restarting game...")
        st.session_state.page = "home"
        st.session_state.names = []
        st.session_state.selections = []
        st.session_state.current_player = 0
        st.session_state.selected_button = None
        st.session_state.eliminated_players = []
        st.session_state.active_players = []
        st.rerun()

        
# 🌐 Remote Mode
if st.session_state.page == "remote_mode":
    st.subheader("Remote Game Setup")
    
    # Add under construction message
    st.warning("🚧 The remote device feature is currently under construction! 🚧")
    st.info("We're working hard to bring you multiplayer functionality soon!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛠️ Generate Room"):
            show_loading_screen("Generating room...")
            room_code = str(uuid.uuid4())[:6].upper()
            st.session_state.room_code = room_code
            st.session_state.page = "player_count"
            st.rerun()

    with col2:
        if st.button("🔗 Join Room"):
            show_loading_screen("Redirecting to join screen...")
            st.session_state.page = "join_room"
            st.rerun()
    
    # Add a back button
    if st.button("← Back to Home"):
        show_loading_screen("Returning home...")
        st.session_state.page = "home"
        st.rerun()

# 🔗 Join Room
elif st.session_state.page == "join_room":
    st.subheader("Join Room")
    room_code_input = st.text_input("Enter Room Code")
    if st.button("Join Room"):
        if room_code_input.strip() == "":
            st.warning("Please enter a valid room code.")
        else:
            show_loading_screen("Joining room...")
            st.session_state.room_code = room_code_input.upper()
            st.session_state.page = "waiting_room"
            st.rerun()

# 🕒 Waiting Room
elif st.session_state.page == "waiting_room":
    st.subheader("🕒 Waiting Room")
    st.write(f"Room Code: `{st.session_state.room_code}`")
    st.info("Waiting for host to start the game...")