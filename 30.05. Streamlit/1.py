import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Анализ чаевых в ресторане")

sex_translation = {'Male': 'Мужчина', 'Female': 'Женщина'}
day_translation = {'Thur': 'Четверг', 'Fri': 'Пятница', 'Sat': 'Суббота', 'Sun': 'Воскресенье'}
smoker_translation = {'Yes': 'Курящий', 'No': 'Некурящий'}
time_translation = {'Lunch': 'Обед', 'Dinner': 'Ужин'}

# Порядок дней для сортировки.
day_order = ['Четверг', 'Пятница', 'Суббота', 'Воскресенье']

@st.cache_data
def load_data():
    df = sns.load_dataset('tips')
    df['sex'] = df['sex'].map(sex_translation)
    df['day'] = df['day'].map(day_translation)
    df['smoker'] = df['smoker'].map(smoker_translation)
    df['time'] = df['time'].map(time_translation)
    # size числовой
    return df

df = load_data()

# Боковая панель с фильтрами.
with st.sidebar:
    st.header("Фильтры данных")
    
    total_bill_min = float(df['total_bill'].min())
    total_bill_max = float(df['total_bill'].max())
    bill_range = st.slider(
        "Диапазон суммы счета ($):",
        total_bill_min, total_bill_max,
        (total_bill_min, total_bill_max)
    )
    
    # Дни недели.
    days = sorted(df['day'].unique(), key=lambda x: day_order.index(x))
    selected_days = st.multiselect("Дни недели:", options=days, default=days)
    
    # Пол.
    sexes = sorted(df['sex'].unique())
    selected_sexes = st.multiselect("Пол клиента:", options=sexes, default=sexes)
    
    # Размер компании.
    size_options = sorted(df['size'].unique())
    selected_sizes = st.multiselect(
        "Количество человек за столом:",
        options=size_options, default=size_options
    )

# Применение фильтров.
try:
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['total_bill'] >= bill_range[0]) &
        (filtered_df['total_bill'] <= bill_range[1])
    ]
    if selected_days:
        filtered_df = filtered_df[filtered_df['day'].isin(selected_days)]
    if selected_sexes:
        filtered_df = filtered_df[filtered_df['sex'].isin(selected_sexes)]
    if selected_sizes:
        filtered_df = filtered_df[filtered_df['size'].isin(selected_sizes)]
except Exception as e:
    st.error(f"Ошибка фильтрации: {e}")
    filtered_df = df.copy()

# 8 ГРАФИКОВ.
st.subheader("1. Какие суммы счетов встречаются чаще всего?")
fig1 = px.histogram(filtered_df, x='total_bill', nbins=40,
                    title="Распределение сумм счетов",
                    labels={'total_bill': 'Сумма счета ($)', 'count': 'Количество заказов'})
st.plotly_chart(fig1, width='stretch')

col1, col2 = st.columns(2)

with col1:
    st.subheader("2. Растёт ли размер чаевых с увеличением счета?")
    fig2 = px.scatter(filtered_df, x='total_bill', y='tip', color='sex',
                      title="Чаевые vs Сумма счета",
                      labels={'total_bill': 'Сумма счета ($)', 'tip': 'Чаевые ($)', 'sex': 'Пол'})
    st.plotly_chart(fig2, width='stretch')
    
    st.subheader("3. В какой день недели клиенты оставляют самые щедрые чаевые?")
    tips_by_day = filtered_df.groupby('day', as_index=False)['tip'].mean()
    tips_by_day['day'] = pd.Categorical(tips_by_day['day'], categories=day_order, ordered=True)
    tips_by_day = tips_by_day.sort_values('day')
    fig3 = px.bar(tips_by_day, x='day', y='tip', color='day',
                  title="Средние чаевые по дням",
                  labels={'day': 'День недели', 'tip': 'Средние чаевые ($)'})
    st.plotly_chart(fig3, width='stretch')
    
    st.subheader("4. Сравнение чаевых по полу")
    tips_by_sex = filtered_df.groupby('sex', as_index=False)['tip'].mean()
    fig4 = px.bar(tips_by_sex, x='sex', y='tip', color='sex',
                  title="Средние чаевые: мужчины vs женщины",
                  labels={'sex': 'Пол', 'tip': 'Средние чаевые ($)'})
    st.plotly_chart(fig4, width='stretch')

with col2:
    st.subheader("5. Количество заказов по времени дня")
    orders_by_time = filtered_df['time'].value_counts().reset_index()
    orders_by_time.columns = ['time', 'count']
    fig5 = px.pie(orders_by_time, values='count', names='time',
                  title="Соотношение заказов: обед vs ужин")
    st.plotly_chart(fig5, width='stretch')
    
    st.subheader("6. Доля курящих и некурящих клиентов")
    smoker_ratio = filtered_df['smoker'].value_counts().reset_index()
    smoker_ratio.columns = ['smoker', 'count']
    fig6 = px.pie(smoker_ratio, values='count', names='smoker',
                  title="Курящие vs Некурящие")
    st.plotly_chart(fig6, width='stretch')
    
    st.subheader("7. Распределение размера компании")
    fig7 = px.histogram(filtered_df, x='size', nbins=len(filtered_df['size'].unique()),
                        title="Количество человек за столом",
                        labels={'size': 'Число персон', 'count': 'Частота'})
    st.plotly_chart(fig7, width='stretch')

st.subheader("8. Различия в средних чаевых по дням и полу")
tips_by_day_sex = filtered_df.groupby(['day', 'sex'], as_index=False)['tip'].mean()
tips_by_day_sex['day'] = pd.Categorical(tips_by_day_sex['day'], categories=day_order, ordered=True)
tips_by_day_sex = tips_by_day_sex.sort_values('day')
fig8 = px.bar(tips_by_day_sex, x='day', y='tip', color='sex', barmode='group',
              title="Средние чаевые: день недели × пол",
              labels={'day': 'День недели', 'tip': 'Средние чаевые ($)', 'sex': 'Пол'})
st.plotly_chart(fig8, width='stretch')

# Сырые данные и скачивание.
with st.expander("Показать отфильтрованные данные (сырая таблица)"):
    st.dataframe(filtered_df)

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Скачать отфильтрованные данные в CSV",
    data=csv_data,
    file_name="filtered_tips.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown(f"**Показано записей:** {len(filtered_df)} из {len(df)} после применения фильтров")