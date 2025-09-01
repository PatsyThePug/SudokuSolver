import streamlit as st
import numpy as np
import time

# Initialize session state
if 'grid' not in st.session_state:
    st.session_state.grid = np.zeros((9, 9), dtype=int)
if 'original_grid' not in st.session_state:
    st.session_state.original_grid = np.zeros((9, 9), dtype=int)
if 'solving' not in st.session_state:
    st.session_state.solving = False
if 'solve_speed' not in st.session_state:
    st.session_state.solve_speed = 0.1

# Predefined Sudoku puzzles
SAMPLE_PUZZLES = {
    "Fácil 1": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "Fácil 2": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],
    "Fácil 3": [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 0, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 0, 0, 6, 8, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ],
    "Medio 1": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ],
    "Medio 2": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ],
    "Medio 3": [
        [0, 0, 5, 3, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 7, 0, 0, 1, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 5, 3, 0, 0],
        [0, 1, 0, 0, 7, 0, 0, 0, 6],
        [0, 0, 3, 2, 0, 0, 0, 8, 0],
        [0, 6, 0, 5, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 9, 7, 0, 0]
    ],
    "Difícil 1": [
        [0, 0, 0, 0, 0, 0, 6, 8, 0],
        [0, 0, 0, 0, 4, 6, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 6, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0, 0]
    ],
    "Difícil 2": [
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 5, 9, 0, 0, 0, 0, 0, 8],
        [2, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 4, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 3, 0, 5, 4],
        [0, 0, 0, 3, 2, 5, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "Difícil 3": [
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 2],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 5],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0]
    ],
    "Experto 1": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3]
    ],
    "Experto 2": [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ],
    "Extremo": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
}

def is_valid(grid, row, col, num):
    """Check if placing num at (row, col) is valid according to Sudoku rules"""
    # Check row
    for j in range(9):
        if grid[row][j] == num:
            return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    
    return True

def find_empty_location(grid):
    """Find an empty location (cell with value 0) in the grid"""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None

def solve_sudoku(grid, visualize=False, speed=0.1):
    """Solve Sudoku using backtracking algorithm"""
    empty_location = find_empty_location(grid)
    
    # If no empty location found, puzzle is solved
    if not empty_location:
        return True
    
    row, col = empty_location
    
    # Try numbers 1 through 9
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            # Make tentative assignment
            grid[row][col] = num
            
            # Add visualization delay if requested
            if visualize:
                st.session_state.grid = grid.copy()
                time.sleep(speed)
                st.rerun()
            
            # Recursively try to solve the rest
            if solve_sudoku(grid, visualize, speed):
                return True
            
            # If it doesn't work, backtrack
            grid[row][col] = 0
            
            if visualize:
                st.session_state.grid = grid.copy()
                time.sleep(speed)
                st.rerun()
    
    return False

def is_valid_puzzle(grid):
    """Check if the current puzzle state is valid"""
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                temp = grid[row][col]
                grid[row][col] = 0
                if not is_valid(grid, row, col, temp):
                    grid[row][col] = temp
                    return False
                grid[row][col] = temp
    return True

def has_unique_solution(grid):
    """Check if puzzle has a unique solution by counting solutions"""
    solutions = [0]
    
    def count_solutions(g):
        if solutions[0] > 1:
            return
        
        empty_location = find_empty_location(g)
        if not empty_location:
            solutions[0] += 1
            return
        
        row, col = empty_location
        for num in range(1, 10):
            if is_valid(g, row, col, num):
                g[row][col] = num
                count_solutions(g)
                g[row][col] = 0
    
    temp_grid = grid.copy()
    count_solutions(temp_grid)
    return solutions[0] == 1

# Streamlit UI
st.title("🧩 Sudoku Solver")
st.markdown("*Solve Sudoku puzzles using backtracking algorithm with visual step-by-step animation*")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    
    # Load sample puzzle
    st.subheader("Load Sample Puzzle")
    puzzle_difficulty = st.selectbox("Choose difficulty:", list(SAMPLE_PUZZLES.keys()))
    
    if st.button("Load Puzzle", type="primary"):
        st.session_state.grid = np.array(SAMPLE_PUZZLES[puzzle_difficulty])
        st.session_state.original_grid = st.session_state.grid.copy()
        st.rerun()
    
    st.divider()
    
    # Solving controls
    st.subheader("Solving Options")
    
    visualize = st.checkbox("Show solving animation", value=True)
    
    if visualize:
        st.session_state.solve_speed = st.slider(
            "Animation speed (seconds between steps):",
            min_value=0.01,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
    
    # Solve button
    if st.button("🚀 Solve Puzzle", type="primary", disabled=st.session_state.solving):
        if not is_valid_puzzle(st.session_state.grid):
            st.error("❌ Invalid puzzle! Please check your inputs.")
        else:
            with st.spinner("Solving puzzle..."):
                st.session_state.solving = True
                grid_copy = st.session_state.grid.copy()
                
                if solve_sudoku(grid_copy, visualize, st.session_state.solve_speed):
                    st.session_state.grid = grid_copy
                    st.success("✅ Puzzle solved successfully!")
                else:
                    st.error("❌ No solution exists for this puzzle!")
                
                st.session_state.solving = False
                st.rerun()
    
    st.divider()
    
    # Reset controls
    st.subheader("Reset Options")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset to Original"):
            st.session_state.grid = st.session_state.original_grid.copy()
            st.rerun()
    
    with col2:
        if st.button("🧹 Clear All"):
            st.session_state.grid = np.zeros((9, 9), dtype=int)
            st.session_state.original_grid = np.zeros((9, 9), dtype=int)
            st.rerun()

# Main grid display
st.subheader("Sudoku Grid")

# Create 9x9 grid using Streamlit columns
for big_row in range(3):
    for big_col in range(3):
        st.markdown(f"**Block {big_row * 3 + big_col + 1}**")
        
        # Create 3x3 sub-grid
        for sub_row in range(3):
            cols = st.columns(3)
            for sub_col in range(3):
                row = big_row * 3 + sub_row
                col = big_col * 3 + sub_col
                
                with cols[sub_col]:
                    # Determine if this is an original number
                    is_original = st.session_state.original_grid[row][col] != 0
                    
                    # Create input field
                    current_value = st.session_state.grid[row][col]
                    display_value = int(current_value) if current_value != 0 else None
                    
                    # Use different styling for original vs user/solved numbers
                    help_text = "Original number" if is_original else "Enter 1-9 or leave empty"
                    
                    new_value = st.number_input(
                        f"R{row+1}C{col+1}",
                        min_value=0,
                        max_value=9,
                        value=display_value,
                        step=1,
                        key=f"cell_{row}_{col}",
                        help=help_text,
                        disabled=is_original or st.session_state.solving,
                        label_visibility="collapsed"
                    )
                    
                    # Update grid if value changed
                    if not is_original and not st.session_state.solving:
                        new_value = new_value if new_value is not None else 0
                        if st.session_state.grid[row][col] != new_value:
                            st.session_state.grid[row][col] = new_value
        
        st.markdown("---")

# Grid validation feedback
if not is_valid_puzzle(st.session_state.grid):
    st.warning("⚠️ Current puzzle state contains conflicts. Please review your inputs.")

# Display puzzle statistics
empty_cells = np.count_nonzero(st.session_state.grid == 0)
filled_cells = 81 - empty_cells

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Filled Cells", filled_cells, f"{filled_cells}/81")
with col2:
    st.metric("Empty Cells", empty_cells)
with col3:
    st.metric("Completion", f"{(filled_cells/81)*100:.1f}%")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    **Getting Started:**
    1. Load a sample puzzle from the sidebar, or manually enter numbers in the grid
    2. Use the solving options to customize the animation
    3. Click "Solve Puzzle" to see the backtracking algorithm in action
    
    **Features:**
    - **Interactive Grid**: Click on any cell to enter numbers (1-9)
    - **Visual Solving**: Watch the algorithm work step-by-step
    - **Validation**: Real-time feedback on puzzle validity
    - **Sample Puzzles**: Three difficulty levels to choose from
    - **Animation Control**: Adjust solving speed or disable animation
    
    **Backtracking Algorithm:**
    The solver uses a recursive backtracking approach:
    1. Find an empty cell
    2. Try numbers 1-9 in that cell
    3. Check if the number is valid (follows Sudoku rules)
    4. If valid, recursively solve the rest of the puzzle
    5. If no valid number works, backtrack and try a different approach
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "Built with Streamlit • Backtracking Algorithm Implementation"
    "</div>", 
    unsafe_allow_html=True
)
