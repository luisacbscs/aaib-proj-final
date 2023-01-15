import streamlit as st
import streamlit.components.v1 as components
import paho.mqtt.client as mqtt
import time
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import numpy as np
from expand import expand
from math import sqrt
from str_to_func import str_to_func

st.set_page_config(page_title='Speech Calc', page_icon='🎙')

client = mqtt.Client("calc_aaib")
client.connect("mqtt.eclipseprojects.io", 1883, 60)

def read_expression(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    try:
        last = lines[-1]
    except IndexError:
        last = ''
    return last

def append_expression(filename, string):
    with open(filename, 'a') as f:
            f.write(string)
            f.close()

def clear_expression(filename):
    if filename == 'expression.txt':
        with open(filename, 'w') as f:
                f.write('Record mathematical expression to compute.\n')
                f.close()
    else:
        with open(filename, 'w') as f:
                f.write('Record function to plot.\n')
                f.close()

def plot_graph(f):    
    fig = plt.figure(figsize=(18, 10))
    plt.plot(f, color='#DAF7A6', linewidth=3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid('on')
    st.pyplot(fig)

replacements = {
        'sin' : 'np.sin',
        'cos' : 'np.cos',
        'tan' : 'np.tan',
        'π' : 'np.pi',
        'exp': 'np.exp',
        'sqrt': 'np.sqrt',
        '^': '**',
    }

allowed_words = [
        'x',
        'sin',
        'cos',
        'tan',
        'pi',
        'sqrt',
        'exp',
    ]

#--------------------------------------------------------------------------------------------------CALCULATOR
st.title('Calculator')

#--------------------------------------------------------------------------COMMANDS
col0, col1, col2 = st.columns([1, 10,2], gap = "small")
with col1:
    display = st.empty()
    display.markdown(read_expression('expression.txt'))
    plot = st.empty()

with col2:
    if st.button('='):
        expression = read_expression('expression.txt')

        for old, new in replacements.items():
            expression = expression.replace(old, new)

        try:
            result = eval(expression.replace('^','**'))
            total = expression + ' = ' +str(result)
        except SyntaxError:
            total = 'Syntax Error'
            result = 'Syntax Error'
        
        with open('previous_calculations.txt', 'a') as f:
            f.write(total+'\n')
            f.close()
        with open('expression.txt', 'a') as f:
            f.write('\n')
            f.write(str(result))
            f.close()
        st.experimental_rerun()
    
    plt_button = st.button('Plot', key = 'plt')
    
    if st.button('(a𝑥+b)ⁿ'):
        expression = read_expression('expression.txt')
        try:
            result = expand(expression)
            total = expression + ' = ' +str(result)
        except SyntaxError:
            total = 'Syntax Error'
            result = 'Syntax Error'
        with open('previous_calculations.txt', 'a') as f:
            f.write(total+'\n')
            f.close()
        with open('expression.txt', 'a') as f:
            f.write('\n')
            f.write(str(result))
            f.close()
        st.experimental_rerun()
    
    if st.button('C'):
        clear_expression('expression.txt')
        plot.empty()
        st.experimental_rerun()
    
    if st.button('REC', key = 1):
        client.publish("AAIB-TL", payload="start")
        time.sleep(10)
        st.experimental_rerun()

if plt_button == True:
    expr = read_expression('expression.txt')
    try:
        func = str_to_func(expr)
        x = np.arange(-100,100,0.1)
        with plot.container():
            plot_graph(func(x))
    except:
        print('Error')
        total = 'Syntax Error'
        result = 'Syntax Error'
        with open('expression.txt', 'a') as f:
            f.write('\n')
            f.write(str(result))
            f.close()
        with open('previous_calculations.txt', 'a') as f:
            f.write(total+'\n')
            f.close()
    with col0:
            st.markdown('f(𝑥) =')
 
    #st.experimental_rerun()

#c01, c02, c03, c04, c05, c06 = st.columns([4, 1, 1, 2, 1, 1], gap="small")
c11, c12, c13, c14, c15, c16, c17, c18, c19, c110 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], gap="small")
c21, c22, c23, c24, c25, c26, c27, c28 = st.columns([2, 1, 1, 1, 1, 1, 1, 2], gap="small")


#--------------------------------------------------------------------------OPERATIONS
with c12:
    if st.button('×'):
        append_expression('expression.txt', '*')
        st.experimental_rerun()

with c13:
    if st.button('÷'):
        append_expression('expression.txt', '/')
        st.experimental_rerun()

with c14:
    if st.button('\+'):
        append_expression('expression.txt', '+')
        st.experimental_rerun()

with c15:
    if st.button('−'):
        append_expression('expression.txt', '-')
        st.experimental_rerun()

with c16:
    if st.button('^'):
        append_expression('expression.txt', '^')
        st.experimental_rerun()

with c17:
    if st.button('√'):
        append_expression('expression.txt', 'sqrt')
        st.experimental_rerun()

with c18:
    if st.button('('):
        append_expression('expression.txt', '(')
        st.experimental_rerun()

with c19:
    if st.button(')'):
        append_expression('expression.txt', ')')
        st.experimental_rerun()

with c22:
    if st.button('exp', key = 'exp'):
        append_expression('expression.txt', 'exp(')
        st.experimental_rerun()

with c23:
    if st.button('sin', key = 'sin'):
        append_expression('expression.txt', 'sin(')
        st.experimental_rerun()

with c24:
    if st.button('cos', key = 'cos'):
        append_expression('expression.txt', 'cos(')
        st.experimental_rerun()

with c25:
    if st.button('tan', key = 'tan'):
        append_expression('expression.txt', 'tan(')
        st.experimental_rerun()

with c26:
    if st.button('π', key = 'pi'):
        append_expression('expression.txt', 'π')
        st.experimental_rerun()

with c27:
    if st.button('𝑥'):
        append_expression('expression.txt', 'x')
        st.experimental_rerun()
       
#--------------------------------------------------------------------------HTML CALCULATOR
components.html(
    """  
    <head>
        <style>
            table {
                border: 1px;
                margin-left: auto;
                margin-right: auto;
                border-radius: 5px;
            }
    
            td {
                width: 110px;
                padding: 20px 40px;
                text-align: center;
                background-color: #DAF7A6;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                font-family: sans-serif;
            }

        </style>
    </head>

    <body>
        <table id="calcu">
            <tr>
                <td>7 </td>
                <td>8 </td>
                <td>9 </td>
            
            </tr>
            <tr>
                <td>4 </td>
                <td>5 </td>
                <td>6 </td>
                
            </tr>
            <tr>
                <td>1 </td>
                <td>2 </td>
                <td>3 </td>
                
            </tr>
            <tr>
                <td style="background-color: #FFFFFF"></td>
                <td>0 </td>
                <td style="background-color: #FFFFFF"></td>
                
            </tr>
        </table>
    </body> 
    """,
    height=320,
)

#--------------------------------------------------------------------------PREVIOUS CALCULATIONS
with st.container():
    f = open('previous_calculations.txt', 'r')
    prev_calc = f.readlines()
    f.close()
    try:
        st.markdown('Previous calculations:')
        st.text(prev_calc[-1].replace('np.', '').replace('pi', 'π'))
    except IndexError:
        pass
    
    try:
        st.text(prev_calc[-2].replace('np.', '').replace('pi', 'π'))
    except IndexError:
        pass
    
    try:
        st.text(prev_calc[-3].replace('np.', '').replace('pi', 'π'))
    except IndexError:
        pass
