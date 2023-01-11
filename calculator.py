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
    fig = plt.figure(figsize=(20, 10))
    plt.plot(x, f, color='#DAF7A6', linewidth=3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid('on')
    st.pyplot(fig)

#--------------------------------------------------------------------------------------------------CALCULATOR
st.title('Calculator')

col1, col2, col3, col4, col5, col6 = st.columns([1, 8, 1, 2, 1, 2], gap="small")
col01, col02, col03, col04, col05, col06, col07, col08, col09, col010 = st.columns([6, 1, 1, 1, 1, 1, 1, 1, 1, 1], gap="small")

#--------------------------------------------------------------------------COMMANDS
with col2:
    st.markdown(read_expression('expression.txt'))

with col3:
    if st.button('='):
        expression = read_expression('expression.txt')
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

with col4:
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

with col5:
    if st.button('C'):
        clear_expression('expression.txt')
        st.experimental_rerun()

with col6:
    if st.button('REC', key = 1):
        client.publish("AAIB-TL", payload="cstart")
        time.sleep(22)
        st.experimental_rerun()

#--------------------------------------------------------------------------OPERATIONS
with col02:
    if st.button('×'):
        append_expression('expression.txt', '*')
        st.experimental_rerun()

with col03:
    if st.button('÷'):
        append_expression('expression.txt', '/')
        st.experimental_rerun()

with col04:
    if st.button('\+'):
        append_expression('expression.txt', '˖')
        st.experimental_rerun()

with col05:
    if st.button('−'):
        append_expression('expression.txt', '-')
        st.experimental_rerun()

with col06:
    if st.button('^'):
        append_expression('expression.txt', '^')
        st.experimental_rerun()

with col07:
    if st.button('√'):
        append_expression('expression.txt', 'sqrt')
        st.experimental_rerun()

with col08:
    if st.button('('):
        append_expression('expression.txt', '(')
        st.experimental_rerun()

with col09:
    if st.button(')'):
        append_expression('expression.txt', ')')
        st.experimental_rerun()

with col010:
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
                <td style="width: 20px; background-color: #EEEEEE">&#215 </td>
                <td style="width: 20px; background-color: #EEEEEE">&#247 </td>
            </tr>
            <tr>
                <td>4 </td>
                <td>5 </td>
                <td>6 </td>
                <td style="width: 20px; background-color: #EEEEEE">&#43 </td>
                <td style="width: 20px; background-color: #EEEEEE">&#8722 </td>
            </tr>
            <tr>
                <td>1 </td>
                <td>2 </td>
                <td>3 </td>
                <td style="width: 20px; background-color: #EEEEEE">^ </td>
                <td style="width: 20px; background-color: #EEEEEE">&#8730 </td>
            </tr>
            <tr>
                <td style="background-color: #FFFFFF"></td>
                <td>0 </td>
                <td style="background-color: #FFFFFF"></td>
                <td style="width: 20px; background-color: #EEEEEE">&#61 </td>
                <td style="width: 20px; font-size: 16px; padding: 10px 20px; background-color: #EEEEEE">(a+b)&#8319 </td>
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
        st.text(prev_calc[-1])
    except IndexError:
        pass
    try:
        st.text(prev_calc[-2])
    except IndexError:
        pass
    try:
        st.text(prev_calc[-2])
    except IndexError:
        pass

#--------------------------------------------------------------------------------------------------PLOT
st.title('Plot')

p1, p2, p3, p4, p5, p6 = st.columns([1, 2, 12, 2, 2, 1], gap="small")
p01, p02, p03, p04, p05, p06, p07, p08, p09, p010, p011 = st.columns([5, 1, 1, 1, 1, 1, 1, 1, 1, 1.5, 1], gap="small")

#--------------------------------------------------------------------------COMMANDS
with p2:
    st.markdown('f(𝑥) =')

with p3:
    st.markdown(read_expression('plot.txt'))

with p4:
    if st.button('REC', key = 'plt_rec'):
        client.publish("AAIB-TL", payload="start")
        time.sleep(22)
        st.experimental_rerun()

with p5:
    plt_button = st.button('Plot', key = 'plt')

with p6:
    if st.button('C', key = 'plt_clear'):
        clear_expression('plot.txt')
        st.experimental_rerun()

#--------------------------------------------------------------------------OPERATIONS
with p02:
    if st.button('×', key = 'plt_t'):
        append_expression('plot.txt', '*')
        st.experimental_rerun()

with p03:
    if st.button('÷', key = 'plt_d'):
        append_expression('plot.txt', '/')
        st.experimental_rerun()

with p04:
    if st.button('\+', key = 'plt_p'):
        append_expression('plot.txt', '˖')
        st.experimental_rerun()

with p05:
    if st.button('−', key = 'plt_m'):
        append_expression('plot.txt', '-')
        st.experimental_rerun()


with p06:
    if st.button('^', key = 'plt_pwr'):
        append_expression('plot.txt', '^')
        st.experimental_rerun()

with p07:
    if st.button('√', key = 'plt_s'):
        append_expression('plot.txt', 'sqrt')
        st.experimental_rerun()

with p08:
    if st.button('(', key = 'plt_o'):
        append_expression('plot.txt', '(')
        st.experimental_rerun()

with p09:
    if st.button(')', key = 'plt_c'):
        append_expression('plot.txt', ')')
        st.experimental_rerun()

with p010:
    if st.button('exp', key = 'plt_e'):
        append_expression('plot.txt', 'exp')
        st.experimental_rerun()

with p011:
    if st.button('𝑥', key = 'plt_x'):
        append_expression('plot.txt', 'x')
        st.experimental_rerun()

if plt_button == True:
    expr = read_expression('plot.txt')
    func = str_to_func(expr)
    x = np.arange(-100,100,0.1)
    plot_graph(func(x))
    #st.experimental_rerun()