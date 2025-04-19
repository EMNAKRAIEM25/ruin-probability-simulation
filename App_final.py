import streamlit as st

# configuration du non de la page 
st.set_page_config(page_title='Simulateur')
import altair as alt
import pandas as pd
import form1
import form2

#DB management 
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(Username TEXT, Password TEXT)')


def add_userdata(Username, Password):
    c.execute('INSERT INTO userstable(Username, Password) VALUES (?,?)',(Username,Password))
    conn.commit()


def login_user(Username, Password):
    c.execute('SELECT * FROM userstable WHERE Username =? AND Password = ?', (Username,Password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data 



def main():



    st.sidebar.title("Menu")
    menu = ["Se connecter", "S'inscrire", "Accueil"]
    choice = st.sidebar.selectbox("", menu)

    
    if choice == "Se connecter":
        st.subheader("Interface d'authentification")
     
        

        username = st.sidebar.text_input("Nom d'utilisateur")
        password = st.sidebar.text_input("mot de passe", type='password')
        if st.sidebar.button("Se connecter"):
            
            create_usertable()
            result = login_user(username,password)
            if result :
                st.success("Bienvenu {}". format(username))

                
            else:
                st.warning("Incorrect Username/Password")
#verfier si le new user existe dans la base ou non 
    elif choice == "S'inscrire":
        st.subheader("Crée un nouveau compte")
        
        # configuration du non de la page 
        
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button ("S'inscrire"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("Vous avez créé avec succès un compte valide")
            st.info("Allez dans le menu de connexion pour vous connecter")

    elif choice == "Accueil":
        st.subheader("Accueil")

        PAGES = {
            
            "Simulateur avec la loi paréto": form1,
            "Simulateur avec la loi weibull": form2
        }
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("", list(PAGES.keys()))
        page = PAGES[selection]
        page.app()
       



if __name__ == '__main__':
    main()