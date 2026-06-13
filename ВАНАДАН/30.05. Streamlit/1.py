import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Анализ чаевых в ресторане")

# ------------------------------------------------------------
# 1. Единая тема оформления для всех графиков Plotly
# ------------------------------------------------------------
PLOTLY_THEME = "plotly_white"       # чистый светлый фон
COLOR_PALETTE = px.colors.qualitative.Pastel   # пастельные цвета для категорий
# (можно заменить на Set1, Vivid, Bold и др.)

sex_translation = {'Male': 'Мужчина', 'Female': 'Женщина'}
day_translation = {'Thur': 'Четверг', 'Fri': 'Пятница', 'Sat': 'Суббота', 'Sun': 'Воскресенье'}
smoker_translation = {'Yes': 'Курящий', 'No': 'Некурящий'}
time_translation = {'Lunch': 'Обед', 'Dinner': 'Ужин'}

day_order = ['Четверг', 'Пятница', 'Суббота', 'Воскресенье']

@st.cache_data
def load_data():
    df = sns.load_dataset('tips')
    df['sex'] = df['sex'].map(sex_translation)
    df['day'] = df['day'].map(day_translation)
    df['smoker'] = df['smoker'].map(smoker_translation)
    df['time'] = df['time'].map(time_translation)
    return df

df = load_data()

# Боковая панель с фильтрами
with st.sidebar:
    st.header("Фильтры данных")
    
    total_bill_min = float(df['total_bill'].min())
    total_bill_max = float(df['total_bill'].max())
    bill_range = st.slider(
        "Диапазон суммы счета ($):",
        total_bill_min, total_bill_max,
        (total_bill_min, total_bill_max)
    )
    
    days = sorted(df['day'].unique(), key=lambda x: day_order.index(x))
    selected_days = st.multiselect("Дни недели:", options=days, default=days)
    
    sexes = sorted(df['sex'].unique())
    selected_sexes = st.multiselect("Пол клиента:", options=sexes, default=sexes)
    
    size_options = sorted(df['size'].unique())
    selected_sizes = st.multiselect(
        "Количество человек за столом:",
        options=size_options, default=size_options
    )

# Применение фильтров
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

# ------------------------------------------------------------
# 2. Вспомогательная функция для единого стиля графиков
# ------------------------------------------------------------
def apply_common_layout(fig, title=None, x_title=None, y_title=None):
    """Применяет единую тему, цвета, сетку и размеры шрифтов."""
    fig.update_layout(
        template=PLOTLY_THEME,
        title=dict(text=title, font=dict(size=18), x=0.5),
        xaxis_title=dict(text=x_title, font=dict(size=12)),
        yaxis_title=dict(text=y_title, font=dict(size=12)),
        legend=dict(title_font=dict(size=12), font=dict(size=11)),
        plot_bgcolor='rgba(240, 248, 255, 0.6)',   # очень светлый голубой фон
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    # Настройка сетки (светлые линии)
    fig.update_xaxis(showgrid=True, gridwidth=0.5, gridcolor='LightGray')
    fig.update_yaxis(showgrid=True, gridwidth=0.5, gridcolor='LightGray')
    return fig

# ------------------------------------------------------------
# 3. Рисуем графики с новым дизайном
# ------------------------------------------------------------
st.subheader("1. Какие суммы счетов встречаются чаще всего?")
fig1 = px.histogram(filtered_df, x='total_bill', nbins=40,
                    color_discrete_sequence=[COLOR_PALETTE[0]],
                    title="Распределение сумм счетов")
fig1 = apply_common_layout(fig1, x_title="Сумма счета ($)", y_title="Количество заказов")
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("2. Растёт ли размер чаевых с увеличением счета?")
    fig2 = px.scatter(filtered_df, x='total_bill', y='tip', color='sex',
                      color_discrete_sequence=COLOR_PALETTE[1:3],
                      title="Чаевые vs Сумма счета")
    fig2 = apply_common_layout(fig2, x_title="Сумма счета ($)", y_title="Чаевые ($)")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("3. В какой день недели клиенты оставляют самые щедрые чаевые?")
    tips_by_day = filtered_df.groupby('day', as_index=False)['tip'].mean()
    tips_by_day['day'] = pd.Categorical(tips_by_day['day'], categories=day_order, ordered=True)
    tips_by_day = tips_by_day.sort_values('day')
    fig3 = px.bar(tips_by_day, x='day', y='tip', color='day',
                  color_discrete_sequence=COLOR_PALETTE,
                  title="Средние чаевые по дням")
    fig3 = apply_common_layout(fig3, x_title="День недели", y_title="Средние чаевые ($)")
    fig3.update_traces(showlegend=False)  # убираем легенду, т.к. дни подписаны
    st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("4. Сравнение чаевых по полу")
    tips_by_sex = filtered_df.groupby('sex', as_index=False)['tip'].mean()
    fig4 = px.bar(tips_by_sex, x='sex', y='tip', color='sex',
                  color_discrete_sequence=COLOR_PALETTE[1:3],
                  title="Средние чаевые: мужчины vs женщины")
    fig4 = apply_common_layout(fig4, x_title="Пол", y_title="Средние чаевые ($)")
    fig4.update_traces(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("5. Количество заказов по времени дня")
    orders_by_time = filtered_df['time'].value_counts().reset_index()
    orders_by_time.columns = ['time', 'count']
    fig5 = px.pie(orders_by_time, values='count', names='time',
                  color_discrete_sequence=COLOR_PALETTE,
                  title="Соотношение заказов: обед vs ужин")
    fig5.update_layout(template=PLOTLY_THEME, title_x=0.5, paper_bgcolor='white')
    st.plotly_chart(fig5, use_container_width=True)
    
    st.subheader("6. Доля курящих и некурящих клиентов")
    smoker_ratio = filtered_df['smoker'].value_counts().reset_index()
    smoker_ratio.columns = ['smoker', 'count']
    fig6 = px.pie(smoker_ratio, values='count', names='smoker',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  title="Курящие vs Некурящие")
    fig6.update_layout(template=PLOTLY_THEME, title_x=0.5, paper_bgcolor='white')
    st.plotly_chart(fig6, use_container_width=True)
    
    st.subheader("7. Распределение размера компании")
    fig7 = px.histogram(filtered_df, x='size', nbins=len(filtered_df['size'].unique()),
                        color_discrete_sequence=[COLOR_PALETTE[4]],
                        title="Количество человек за столом")
    fig7 = apply_common_layout(fig7, x_title="Число персон", y_title="Частота")
    st.plotly_chart(fig7, use_container_width=True)

st.subheader("8. Различия в средних чаевых по дням и полу")
tips_by_day_sex = filtered_df.groupby(['day', 'sex'], as_index=False)['tip'].mean()
tips_by_day_sex['day'] = pd.Categorical(tips_by_day_sex['day'], categories=day_order, ordered=True)
tips_by_day_sex = tips_by_day_sex.sort_values('day')
fig8 = px.bar(tips_by_day_sex, x='day', y='tip', color='sex', barmode='group',
              color_discrete_sequence=COLOR_PALETTE[1:3],
              title="Средние чаевые: день недели × пол")
fig8 = apply_common_layout(fig8, x_title="День недели", y_title="Средние чаевые ($)")
st.plotly_chart(fig8, use_container_width=True)

# Сырые данные и скачивание
with st.expander("Показать отфильтрованные данные (сырая таблица)"):
    st.dataframe(filtered_df)

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Скачать отфильтрованные данные в CSV",
    data=csv_data,
    file_name="filtered_tips.csv",
    mime="text/csv"
)

st.markdown(f"**Показано записей:** {len(filtered_df)} из {len(df)} после применения фильтров")