import streamlit as st

def main():
    st.title('Enchanted Equities')
    st.subheader('Benvenuto, Scegli quale versione del sito desideri visitare:')
    
    st.write("Seleziona una delle due opzioni qui sotto per essere reindirizzato al sito corrispondente.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('Equities v2', help='Clicca per visitare la versione v2 del sito'):
            st.success('Clicca e sarai reindirizzato a Equities v2.')
            st.markdown('### [Visita Enchanted Equities v2](https://enchanted-equities-v2.streamlit.app)', unsafe_allow_html=True)
    
    with col2:
        if st.button('Test Analyze Pro', help='Clicca per visitare la versione Test Analyze Pro del sito'):
            st.success('Clicca e sarai reindirizzato a Test Analyze Pro.')
            st.markdown('### [Visita Enchanted Equities Test Analyze Pro](https://enchanted-equities-test-analyze-pro.streamlit.app)', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
