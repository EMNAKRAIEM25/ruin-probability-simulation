import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def app():
    form3 = st.form(key='form3')
    form3.subheader("Simulateur avec la loi paréto")
    n_clients = int(form3.number_input("Nombre des clients"))
    p_sinistre = form3.number_input("Probabilité des sinistres")
    n_annees = int(form3.number_input("Nombre des années"))
    capital_initial = form3.number_input("Capital initial") 
    prime_annuelle = form3.number_input("Prime anuelle") 

    alpha = form3.number_input("Paramètre alpha de la loi paréto")
    theta = form3.number_input("Paramètre theta de la loi paréto")

    M = int(form3.number_input("Nombre de simulation"))

    submit = form3.form_submit_button("Simuler") 
    
    A = np.zeros(M)
    n_sinistres_all = np.zeros((n_annees, M)) # Stocker le nombre de réclamations pour chaque simulation
    couts_total_all = np.zeros((n_annees, M)) # Stocker le coût total des réclamations pour chaque simulation
    capital_all = np.zeros((n_annees+1, M)) # Stocker le capital à la fin de chaque année pour chaque simulation

    for j in range(M):
    
    # Simulation des sinistres et des coûts associés
        n_sinistres = np.random.binomial(n_clients, p_sinistre, n_annees)
        n_sinistres_all[:, j] = n_sinistres # Stocker le nombre de réclamations pour cette simulation
        couts_sinistres = np.random.pareto(alpha, sum(n_sinistres)) * theta
        couts_total = np.zeros(n_annees)
        for i in range(n_annees):
            debut = np.sum(n_sinistres[:i])
            fin = np.sum(n_sinistres[:i+1])
            couts_total[i] = np.sum(couts_sinistres[debut:fin])
        couts_total_all[:, j] = couts_total # Stocker le coût total des sinistres pour cette simulation
    
    # Simulation du capital restant
        capital = np.zeros((n_annees+1, 1))
        capital[0] = capital_initial
        for i in range(n_annees):
            capital[i+1] = capital[i] + prime_annuelle - couts_total[i]
        capital_all[:, j] = capital[:, 0] # Stocker le capital à la fin de chaque année pour cette simulation
    
    # Calcul de la probabilité de ruine pour cette simulation
        a = np.where(capital[:, 0] < 0)[0]
        if len(a) == 0:
            A[j] = 0
        else:
            A[j] = 1
        
    prob_ruine = np.mean(A)
    st.write("La probabilité de ruine de l'assurance est de ",prob_ruine)

