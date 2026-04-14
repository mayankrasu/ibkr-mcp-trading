import streamlit as st
from ibkr_mcp.llm.parser import parse_natural_language
from ibkr_mcp.mcp.server import MCPServer
from ibkr_mcp.ibkr.service import IBService


# -------------------------
# INIT
# -------------------------
if "ib" not in st.session_state:
    ib = IBService()
    ib.connect()
    mcp = MCPServer(ib)

    st.session_state.ib = ib
    st.session_state.mcp = mcp
else:
    ib = st.session_state.ib
    mcp = st.session_state.mcp


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="IBKR AI Assistant", layout="wide")

st.title("🤖 IBKR Trading Assistant")
st.caption("Natural language trading via IBKR")


# -------------------------
# SIDEBAR (connection + controls)
# -------------------------
if ib.client.isConnected():
    st.sidebar.success("🟢 IBKR Connected")
else:
    st.sidebar.error("🔴 IBKR Disconnected")


if st.sidebar.button("Disconnect IBKR"):
    try:
        ib.disconnect()
    except:
        pass

    st.session_state.pop("ib", None)
    st.session_state.pop("mcp", None)
    st.sidebar.warning("Disconnected. Refresh to reconnect.")


# -------------------------
# SESSION STATE (chat)
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            st.dataframe(msg["content"], use_container_width=True)

        elif isinstance(msg["content"], dict):
            st.table([msg["content"]])

        else:
            st.markdown(str(msg["content"]))


# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Type your instruction...")

if user_input:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------
    # PROCESS
    # -------------------------
    try:
        tool_call = parse_natural_language(user_input)

        result = mcp.call_tool(
            tool_call["tool"],
            tool_call["arguments"]
        )

    except Exception as e:
        result = f"❌ Error: {str(e)}"

    # -------------------------
    # STORE RESPONSE
    # -------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    # -------------------------
    # DISPLAY RESPONSE
    # -------------------------
    with st.chat_message("assistant"):
        if isinstance(result, list) and len(result) > 0:
            st.dataframe(result, use_container_width=True)

        elif isinstance(result, dict):
            st.table([result])

        else:
            st.markdown(str(result))