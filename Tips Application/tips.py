from multiprocessing import context
from turtle import color, title
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 
# [theme]
# base="light"
# primaryColor="#6073c5"
# secondaryBackgroundColor="#f7d79d"


st.write("""
# Чаевые в ресторане
"""
)

def load_data():
    tips_df = pd.read_csv("tips.csv")
    tips = tips_df.set_index('Unnamed: 0')
    return tips

tips = load_data()

def main():
    sns.plotting_context("notebook")
    sns.set(style='whitegrid')
    sns.axes_style("ticks")
    col2, col3, col4 = st.columns([3, 1, 6])
    new_tab = tips.head(10)
    col4.dataframe(data=new_tab)
    col2.subheader('Исследуемые данные :sunrise:')
    col2.markdown('<div style="text-align: justify;">Здесь представлена таблица данных чаевых в ресторане.\nТакже таблица содержит данные о поле человека, его общем счете, времени дня, дне недели и размере заказа.</div>', unsafe_allow_html=True)
    # col2.markdown('<div style="text-align: justify;">'Здесь представлена таблица данных чаевых в ресторане.\nТакже таблица содержит данные о поле человека, его общем счете, времени дня, дня недели и размера заказа' </div>)
    st.markdown('Внизу приведены различные исследования в виде графиков. Для того, чтобы поменять график, нажмите кнопку слева и выберите график из представленных :arrow_upper_left:')
    st.sidebar.markdown('<div style="text-align: justify;">Здесь можно выбрать зависимости (графики), которые будут построены по исследуемым данным.</div>', unsafe_allow_html=True)
    page = st.sidebar.selectbox('Выберите график', ['Гистограмма общего счета', 'Общий счет и чаевые', 'Графики по чаевым', 'Исследования по дням недели'],)

    if page == 'Гистограмма общего счета':
        st.header('Histogram Total Bill :small_orange_diamond:')
        st.markdown('Гистограмма, показывающая количество размеров счета.')
        hist_total_bill()
    
    elif page == 'Общий счет и чаевые':
        st.header('Total bill vs Tips :small_orange_diamond:')
        st.write("""
        ##### График зависимости размера чаевых от общего счета
        **Точечный график**. График показывает, как зависит размер чаевых от общего счета заказа.\n
        Внизу можно выбрать разбиение графика :arrow_double_down:
        """)
        total_bill_vs_tip()
    
    elif page == 'Графики по чаевым':
        st.header('Tip Charts :small_orange_diamond:')
        st.markdown('**Гистограмма по чаевым.** График показывает количество чаевых определенной суммы.')
        charts_tip()
    
    elif page == 'Исследования по дням недели':
        daily_charts()


def daily_charts():
    fig = plt.figure(figsize=(6, 6))
    st.header('Daily Research')
    st.markdown('Ниже приведены графики чаевых и и размера счета по дням недели.')
    # plot = st.selectbox('Выберете график:',['Чаевые по дням недели', 'Размер счета по дням недели'])
    # if plot == 'Чаевые по дням недели':
    st.header('Daily Research by Tip :small_orange_diamond:')
    st.markdown('**Точечный график.** График показывает количество чаевых определенной суммы по дням недели. Также есть разбиение по полу человека.')
    tips = sns.load_dataset("tips")
    f = sns.relplot(data=tips, x='tip', y='day', kind='scatter', hue='sex')
    f.set(xlabel = 'Чаевые', ylabel='Дни недели')
    f._legend.set_title('Пол')
    st.pyplot(f)
    # elif plot == 'Размер счета по дням недели':
    st.header('Daily Research by Total Bill :small_orange_diamond:')
    st.markdown('**Точечный график.** График показывает количество размеров общего счета определенной суммы по дням недели.')
    fg = sns.relplot(data=tips, x='day', y='total_bill', color='orange')
    fg.set(xlabel = 'Дни недели', ylabel='Размер счёта')
    st.pyplot(fg)


def charts_tip():
    fig = plt.figure(figsize=(6, 6))
    chek = st.checkbox('Разбить по времени')
    if chek:
        fig = sns.displot(data=tips, x='tip', kind='hist', col='time', color='orange')
        fig.set(xlabel = 'Чаевые', ylabel='Число таких значений')
        st.pyplot(fig)
    else:
        fig = sns.displot(data=tips, x='tip', kind='hist', color='orange')
        fig.set(xlabel = 'Чаевые', ylabel='Число таких значений')
        st.pyplot(fig)


def hist_total_bill():
    fig = plt.figure(figsize=(8, 6))
    plt.title('Гистограмма общего счета')
    fg = sns.histplot(
            data=tips,
            x='total_bill',
            color='orange',
            bins=20,
            kde=True
            )
    fg.set(xlabel = 'Общий счет', ylabel='Число таких значений')
    st.pyplot(fig)   


def total_bill_vs_tip():
    plot = st.selectbox('Выберите разбиение графика:',['Нет разбиения', 'По полу', 'По размеру'])
    fig = plt.figure(figsize=(8, 6))

    col1, col2 = st.columns([1, 3])

    if plot == 'Нет разбиения':
        fig = sns.relplot(data=tips, x='total_bill', y='tip', color='orange')
        fig.set(xlabel = 'Общий счет', ylabel='Чаевые')
        st.pyplot(fig)
    
    elif plot == 'По полу':
        # sns.scatterplot(data=tips, x="total_bill", y="tip", col="smoker", hue="sex")
        sex = col1.radio('Выберите пол:', ('Мужской', 'Женский'))  
        if sex == 'Мужской':
            male_tips = tips[tips['sex'] == 'Male']
            # fg = sns.scatterplot(data=male_tips, x="total_bill", y="tip", hue="smoker")
            fg = sns.relplot(data=male_tips, x='total_bill', y='tip', hue='smoker')
            fg.set(xlabel = 'Общий счет', ylabel='Чаевые')
            fg._legend.set_title('Курит?')
            col2.pyplot(fg)
        elif sex == 'Женский':
            female_tips = tips[tips['sex'] == 'Female']
            fg = sns.relplot(data=female_tips, x='total_bill', y='tip', hue='smoker')
            fg.set(xlabel = 'Общий счет', ylabel='Чаевые')
            fg._legend.set_title('Курит?')
            col2.pyplot(fg)

    elif plot == 'По размеру':
        fig = sns.relplot(data=tips, x='total_bill', y='tip', hue='size', palette=['#ffeecc', '#ffe6b3', '#ffdd99', '#ffd480', '#ffcc66', '#ffc34d'])
        fig._legend.set_title('Размер')
        fig.set(xlabel = 'Общий счет', ylabel='Чаевые')
        st.pyplot(fig)

    

if __name__ == "__main__":
    main()
