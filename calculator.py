import streamlit as st
import streamlit.components.v1 as components
import paho.mqtt.client as mqtt
import time
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import numpy as np
from math import comb
from expand import expand

st.set_page_config(page_title='Voice Calculator', page_icon='🎙')

st.title('Calculator')

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

col1, col2, col3, col4, col5, col6 = st.columns([1, 8, 1, 2, 1, 2], gap="small")

with col2:
    st.markdown(read_expression('expression.txt'))
with col3:
    if st.button('='):
        expression = read_expression('expression.txt')
        result = eval(expression.replace('^','**'))
        total = expression + ' = ' +str(result)
        with open('previous_calculations.txt', 'a') as f:
            f.write(total+'\n')
            f.close()
        with open('expression.txt', 'a') as f:
            f.write('\n')
            f.write(str(result))
            f.close()
        st.experimental_rerun()
with col4:
    if st.button('(a+b)ⁿ'):
        expression = read_expression('expression.txt')
        result = expand(expression)
        total = expression + ' = ' +str(result)
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
        with open('expression.txt', 'w') as f:
            f.write('Record mathematical expression to compute.')
            st.experimental_rerun()
with col6:
    if st.button('REC', key = 1):
        client.publish("AAIB-TL", payload="start")
        #with st.spinner('Wait for it...'):
        #    time.sleep(15)
        #    st.success('Done!')
            
        st.experimental_rerun()

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

st.title('Plot')

def plot_graph(f):    
    fig = plt.figure(figsize=(20, 10))
    plt.plot(x, f, color='#DAF7A6', linewidth=2)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid('on')
    st.pyplot(fig)

def line(x, m, b):
    return x*m+b

def square(x, m, b):
    return m*(x**2)+b

def exp(x, m, b):
    return m*(np.exp(x))+b

def sin(x, m, b):
    return m*(np.sin(x + b))

plot = st.radio(
    "Select a function to plot:",
    ('f(x)=mx+b', 'f(x)=mx^2+b', 'f(x)=m*e^x+b', 'f(x)=m*sin(x+b)'))

st.markdown('Record constants m and b:')
col7, col8, col9, col10, col11, col12, col13 = st.columns([1, 1, 2, 1, 1, 2, 6], gap="small")

with col7:
    st.markdown('m:')
with col8:
    st.markdown(read_expression('m.txt'))
with col9:
    if st.button('REC', key=2):
        client.publish("AAIB-TL", payload="start")
        f = open('expression.txt', 'r')
        lines = f.readlines()
        f.close()
        try:
            number = lines[-1]
            with open('m.txt', 'w') as f:
                f.write(number)
        except IndexError:
            pass
        st.experimental_rerun()
with col10:
    st.markdown('b:')
with col11:
    st.markdown(read_expression('b.txt'))
with col12:
    if st.button('REC', key=3):
        client.publish("AAIB-TL", payload="start")
        f = open('expression.txt', 'r')
        lines = f.readlines()
        f.close()
        try:
            number = lines[-1]
            with open('b.txt', 'w') as f:
                f.write(number)
        except IndexError:
            pass
        st.experimental_rerun()
if plot == 'f(x)=mx+b':
    try:
        m = int(read_expression('m.txt'))
    except:
        m = 0
    try:
        b = int(read_expression('b.txt'))
    except:
        b = 0
    x = np.arange(-100,100,0.1)
    plot_graph(line(x,m,b))
else:
    if plot == 'f(x)=mx^2+b':
        try:
            m = int(read_expression('m.txt'))
        except:
            m = 0
        try:
            b = int(read_expression('b.txt'))
        except:
            b = 0
        x = np.arange(-100,100,0.1)
        plot_graph(square(x,m,b))
    else:
        if plot == 'f(x)=m*e^x+b':
            try:
                m = int(read_expression('m.txt'))
            except:
                m = 0
            try:
                b = int(read_expression('b.txt'))
            except:
                b = 0
            x = np.arange(-100,100,0.1)
            plot_graph(exp(x,m,b))
        else:
            if plot == 'f(x)=m*sin(x+b)':
                try:
                    m = int(read_expression('m.txt'))
                except:
                    m = 0
                try:
                    b = int(read_expression('b.txt'))
                except:
                    b = 0
                x = np.arange(-100,100,0.1)
                plot_graph(sin(x,m,b))

