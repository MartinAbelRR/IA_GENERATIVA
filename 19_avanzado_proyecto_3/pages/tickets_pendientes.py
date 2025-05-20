import streamlit as st

st.title('Departamentos de Tickets Pendientes')

# Crear pestañas.
tab1, tab2, tab3 = st.tabs(['HR', 'IT', 'Transporte'])

# Agregar contenido a las pestañas.
with tab1:
    st.header('Tickets Pendientes de HR')
    if 'tickets_hr' in st.session_state:
        for ticket in st.session_state['tickets_hr']:
            st.write(str(st.session_state['tickets_hr'].index(ticket) + 1) + '. ' + ticket)
    else:
        st.write('No hay tickets pendientes de HR.')

with tab2:
    st.header('Tickets Pendientes de IT')
    if 'tickets_it' in st.session_state:
        for ticket in st.session_state['tickets_it']:
            st.write(str(st.session_state['tickets_it'].index(ticket) + 1) + '. ' + ticket)
    else:
        st.write('No hay tickets pendientes de IT.')

with tab3:
    st.header('Tickets Pendientes de Transporte')
    if 'tickets_transporte' in st.session_state:
        for ticket in st.session_state['tickets_transporte']:
            st.write(str(st.session_state['tickets_transporte'].index(ticket) + 1) + '. ' + ticket)
    else:
        st.write('No hay tickets pendientes de Transporte.')