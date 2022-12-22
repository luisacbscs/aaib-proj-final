import streamlit as st
import streamlit.components.v1 as components
import paho.mqtt.client as mqtt
import time
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

st.set_page_config(page_title='Voice Calculator', page_icon='🎙')

st.title('Calculator')

client = mqtt.Client("calc_aaib")
client.connect("mqtt.eclipseprojects.io", 1883, 60)

def read_expression():
    f = open('expression.txt', 'r')
    lines = f.readlines()
    f.close()
    return lines[-1]

col1, col2, col3, col4, col5, col6 = st.columns([1, 8, 1, 2, 1, 2], gap="small")

with col2:
    st.markdown(read_expression())
with col3:
    if st.button('='):
        f = open('expression.txt', 'r')
        lines = f.readlines()
        f.close()
        expression = lines[-1]
        result = eval(expression)
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
        result = 'Binomial Expansion'
with col5:
    if st.button('C'):
        with open('expression.txt', 'w') as f:
            f.write('Record mathematical expression to compute.')
            st.experimental_rerun()
with col6:
    if st.button('REC'):
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
    x = np.arange(-100,100,0.1)
    fig = plt.figure(figsize=(20, 10))
    plt.plot(x, f, color='#DAF7A6')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid('on')
    st.pyplot(fig3)

plot_graph()