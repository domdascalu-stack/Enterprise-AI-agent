import streamlit as st
import boto3
import uuid
import os

AGENT_ID = "GANVN4QYRT"
AGENT_ALIAS_ID = "WFETGDPWE6"
REGION = "us-east-1"

os.environ["AWS_ACCESS_KEY_ID"] = st.secrets["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = st.secrets["AWS_SECRET_ACCESS_KEY"]

client = boto3.client("bedrock-agent-runtime", region_name=REGION)

st.title("🤖 My Bedrock Agent")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.invoke_agent(
                    agentId=AGENT_ID,
                    agentAliasId=AGENT_ALIAS_ID,
                    sessionId=st.session_state.session_id,
                    inputText=prompt,
                )
                output = ""
                for event in response["completion"]:
                    if "chunk" in event:
                        output += event["chunk"]["bytes"].decode("utf-8")
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            except Exception as e:
                st.error(f"Error: {e}")
