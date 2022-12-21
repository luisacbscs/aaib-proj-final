import streamlit as st
import streamlit.components.v1 as components
import paho.mqtt.client as mqtt
import time
from streamlit_autorefresh import st_autorefresh

client = mqtt.Client("calc_aaib")
client.connect("mqtt.eclipseprojects.io", 1883, 60)

def read_expression():
    f = open('expression.txt', 'r')
    lines = f.readlines()
    f.close()
    return lines[-1]

col1, col2, col3, col4 = st.columns([1, 10, 1, 2],gap="small")

with col2:
    st.markdown(read_expression())
with col3:
    if st.button('C'):
        with open('expression.txt', 'w') as f:
            f.write('Record mathematical expression to compute.')
            st.experimental_rerun()
with col4:
    if st.button('REC'):
        #client.publish("AAIB-TL", payload="start")
        #with st.spinner('Wait for it...'):
        #    time.sleep(8)
        #    st.success('Done!')
        last = read_expression()
        print(last[-1])
        if last[-1] != '=':
            result = last
        else:
            result = eval(last[:-1])
            
        with open('expression.txt', 'a') as f:
            f.write('\n')
            f.write(str(result))
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
                <td style="width: 10px; background-color: #EEEEEE">&#215 </td>
                <td style="width: 10px; background-color: #EEEEEE">&#247 </td>
            </tr>
            <tr>
                <td>4 </td>
                <td>5 </td>
                <td>6 </td>
                <td style="width: 10px; background-color: #EEEEEE">&#43 </td>
                <td style="width: 10px; background-color: #EEEEEE">&#8722 </td>
            </tr>
            <tr>
                <td>1 </td>
                <td>2 </td>
                <td>3 </td>
                <td style="width: 10px; background-color: #EEEEEE">^ </td>
                <td style="width: 10px; background-color: #EEEEEE">&#8730 </td>
            </tr>
            <tr>
                <td style="background-color: #FFFFFF"></td>
                <td>0 </td>
                <td style="background-color: #FFFFFF"></td>
                <td style="width: 10px; background-color: #FFFFFF"></td>
                <td style="width: 10px; background-color: #FFFFFF"></td>
            </tr>
        </table>
    </body> 
    """,
    height=400,
)


