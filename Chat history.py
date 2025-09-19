    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        with st.spinner("AI is typing..."):
            try:
                response = query_openrouter(st.session_state.messages, model_id)
            except Exception as e:
                st.error(f"Error: {e}")
                return
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.experimental_rerun()
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        st.experimental_rerun()
if __name__ == "__main__":
    main()
