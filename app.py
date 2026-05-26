import streamlit as st
import math

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
    
)

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Reset padding for the main container to ensure alignment */
.block-container {
    padding-top: 4rem;
    max-width: 550px !important;
}

/* ---------------- APP BACKGROUND ---------------- */
.stApp {
    background-color: #dbe4f0 !important;
    color: #0f172a !important;
}

/* ---------------- DISPLAY BOX ---------------- */
.display {
    background: linear-gradient(145deg, #1e293b, #334155);
    color: #ffffff;
    padding: 20px;
    border-radius: 14px;
    font-size: 34px;
    text-align: right;
    border: 1px solid #475569;
    margin-bottom: 20px; /* Space between display and buttons */
    min-height: 80px;
    word-wrap: break-word;
    box-shadow: 0 6px 18px rgba(0,0,0,0.20);
    font-family: monospace;
    line-height: 1.2;
}

/* ---------------- BUTTONS ---------------- */
div.stButton > button {
    width: 100%;
    height: 55px;
    font-size: 18px;
    border-radius: 10px;
    border: 1px solid #94a3b8;
    background: linear-gradient(145deg, #f1f5f9, #e2e8f0);
    color: #0f172a;
    font-weight: 600;
    margin-bottom: -10px; /* Tighten vertical gap between rows */
}

div.stButton > button:hover {
    background: linear-gradient(145deg, #e2e8f0, #cbd5e1);
    border-color: #64748b;
}

/* Special styling for Clear and Backspace to make them stand out */
button[key^="extra_C"] {
    background: #fee2e2 !important;
    color: #b91c1c !important;
}

/* Remove default Streamlit padding between columns */
[data-testid="column"] {
    padding: 0 5px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOGIC FUNCTIONS ----------------
def add(value):
    if st.session_state.expression == "Error":
        st.session_state.expression = ""
    st.session_state.expression += value

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    try:
        expr = st.session_state.expression
        if not expr or expr == "Error":
            return
        # Replace display power symbol with python power symbol
        result = eval(expr.replace('^', '**'))
        
        if isinstance(result, float):
            result = int(result) if result.is_integer() else round(result, 6)
            
        st.session_state.history.append(f"{expr} = {result}")
        st.session_state.expression = str(result)
    except:
        st.session_state.expression = "Error"

     

def scientific(func):
    try:
        if not st.session_state.expression or st.session_state.expression == "Error":
            return
        value = eval(st.session_state.expression)
        
        if func == "sin": result = math.sin(math.radians(value))
        elif func == "cos": result = math.cos(math.radians(value))
        elif func == "tan": result = math.tan(math.radians(value))
        elif func == "sqrt": result = math.sqrt(value)
        elif func == "log": result = math.log10(value)
        elif func == "ln": result = math.log(value)
        
        st.session_state.history.append(f"{func}({value}) = {result}")
        st.session_state.expression = str(round(result, 6))
    except:
        st.session_state.expression = "Error"

# ---------------- UI LAYOUT ----------------
st.title("🧮 Scientific Calculator")

# 1. Display
display_value = st.session_state.expression if st.session_state.expression else "0"
st.markdown(f'<div class="display">{display_value}</div>', unsafe_allow_html=True)

# 2. Top Row (Clear, Backspace, Brackets)
col_top = st.columns(4)
with col_top[0]: 
    if st.button("C", key="extra_C"): clear(); st.rerun()
with col_top[1]: 
    if st.button("⌫", key="extra_back"): backspace(); st.rerun()
with col_top[2]: 
    if st.button("(", key="extra_p1"): add("("); st.rerun()
with col_top[3]: 
    if st.button(")", key="extra_p2"): add(")"); st.rerun()

# 3. Number Pad & Operators
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        if cols[i].button(btn, key=f"btn_{btn}_{i}"):
            if btn == "=": calculate()
            else: add(btn)
            st.rerun()

         
# 4. Scientific Functions
st.write("---")
st.subheader("Scientific Functions") 
sci_rows = [["sin", "cos", "tan"], ["sqrt", "log", "ln"]]

for row in sci_rows:
    cols = st.columns(3)
    for i, func in enumerate(row):
        if cols[i].button(func, key=f"sci_{func}"):
            scientific(func)
            st.rerun()

# 5. History
st.write("")
with st.expander("📜 History"):
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.write(f"`{item}`")
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No calculations yet.")