import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка страницы.
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("HR Analytics Dashboard")
st.markdown("Анализ факторов, влияющих на увольнение сотрудников")

# 1. ЗАГРУЗКА ДАННЫХ.
@st.cache_data
def load_data():
    df = pd.read_csv('HR_comma_sep.csv')
    return df

df = load_data()

# Преобразование типов.
df['Department'] = df['Department'].astype(str)
df['salary'] = df['salary'].astype(str)
df['left'] = df['left'].astype(int)

st.success(f"Данные загружены! Всего сотрудников: {len(df)}")

# 2. БОКОВАЯ ПАНЕЛЬ С ФИЛЬТРАМИ.
st.sidebar.header("Фильтры")

# Фильтр по отделам.
departments = ['Все'] + sorted(df['Department'].unique())
selected_dept = st.sidebar.selectbox("Департамент", departments)

# Фильтр по уровню зарплаты.
salary_levels = ['Все'] + sorted(df['salary'].unique())
selected_salary = st.sidebar.selectbox("Уровень зарплаты", salary_levels)

# Фильтр по статусу увольнения.
left_status = st.sidebar.radio(
    "Статус сотрудника",
    ['Все', 'Уволившиеся', 'Работающие']
)

# Фильтр по стажу.
min_tenure = int(df['time_spend_company'].min())
max_tenure = int(df['time_spend_company'].max())
tenure_range = st.sidebar.slider(
    "Стаж в компании (лет)",
    min_tenure, max_tenure,
    (min_tenure, max_tenure)
)

# Фильтр по количеству проектов.
min_projects = int(df['number_project'].min())
max_projects = int(df['number_project'].max())
project_range = st.sidebar.slider(
    "Количество проектов",
    min_projects, max_projects,
    (min_projects, max_projects)
)

# 3. ПРИМЕНЕНИЕ ФИЛЬТРОВ.
filtered_df = df.copy()

if selected_dept != 'Все':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]

if selected_salary != 'Все':
    filtered_df = filtered_df[filtered_df['salary'] == selected_salary]

if left_status == 'Уволившиеся':
    filtered_df = filtered_df[filtered_df['left'] == 1]
elif left_status == 'Работающие':
    filtered_df = filtered_df[filtered_df['left'] == 0]

filtered_df = filtered_df[
    (filtered_df['time_spend_company'] >= tenure_range[0]) &
    (filtered_df['time_spend_company'] <= tenure_range[1])
]

filtered_df = filtered_df[
    (filtered_df['number_project'] >= project_range[0]) &
    (filtered_df['number_project'] <= project_range[1])
]

st.sidebar.metric("Отфильтровано записей", len(filtered_df))

# 4. ОСНОВНАЯ ПАНЕЛЬ С ГРАФИКАМИ.
st.header("Визуализация данных")

# График 1: Распределение уровня удовлетворенности по статусу увольнения.
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Удовлетворенность vs Увольнение")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    
    left_0 = filtered_df[filtered_df['left'] == 0]['satisfaction_level']
    left_1 = filtered_df[filtered_df['left'] == 1]['satisfaction_level']
    
    ax1.hist(left_0, bins=20, alpha=0.5, label='Работающие', color='green', edgecolor='black')
    ax1.hist(left_1, bins=20, alpha=0.5, label='Уволившиеся', color='red', edgecolor='black')
    ax1.set_xlabel('Уровень удовлетворенности')
    ax1.set_ylabel('Количество сотрудников')
    ax1.set_title('Распределение уровня удовлетворенности')
    ax1.legend()
    st.pyplot(fig1)
    
    st.caption(f"Средняя удовлетворенность работающих: {left_0.mean():.2f}")
    st.caption(f"Средняя удовлетворенность уволившихся: {left_1.mean():.2f}")

# График 2: Оптимальное количество проектов.
with col2:
    st.subheader("2. Проекты vs Оценка эффективности")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    project_stats = filtered_df.groupby('number_project')['last_evaluation'].agg(['mean', 'std']).reset_index()
    
    ax2.bar(project_stats['number_project'], project_stats['mean'], 
            yerr=project_stats['std'], capsize=5, color='steelblue', edgecolor='black')
    ax2.set_xlabel('Количество проектов')
    ax2.set_ylabel('Средняя оценка эффективности')
    ax2.set_title('Оценка эффективности vs Количество проектов')
    ax2.axhline(y=filtered_df['last_evaluation'].mean(), color='red', linestyle='--', label='Среднее значение')
    ax2.legend()
    st.pyplot(fig2)
    
    optimal = project_stats.loc[project_stats['mean'].idxmax(), 'number_project']
    st.caption(f"Оптимальное количество проектов: {optimal}")

# График 3: Часы работы по отделам.
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Часы работы по отделам")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    dept_hours = filtered_df.groupby('Department')['average_montly_hours'].mean().sort_values(ascending=False)
    colors = plt.cm.viridis(np.linspace(0, 1, len(dept_hours)))
    ax3.barh(dept_hours.index, dept_hours.values, color=colors, edgecolor='black')
    ax3.set_xlabel('Среднемесячные часы работы')
    ax3.set_title('Средние часы работы по отделам')
    ax3.invert_yaxis()
    st.pyplot(fig3)

# График 4: Уровень зарплаты и увольнения.
with col4:
    st.subheader("4. Зарплата vs Увольнение")
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    
    salary_left = filtered_df.groupby(['salary', 'left']).size().unstack(fill_value=0)
    salary_left.columns = ['Работающие', 'Уволившиеся']
    
    salary_left.plot(kind='bar', ax=ax4, color=['green', 'red'], edgecolor='black')
    ax4.set_xlabel('Уровень зарплаты')
    ax4.set_ylabel('Количество сотрудников')
    ax4.set_title('Распределение увольнений по уровням зарплаты')
    ax4.legend()
    ax4.tick_params(axis='x', rotation=0)
    st.pyplot(fig4)
    
    for salary in salary_left.index:
        total = salary_left.loc[salary].sum()
        left_pct = salary_left.loc[salary]['Уволившиеся'] / total * 100
        st.caption(f" {salary}: уволилось {left_pct:.1f}%")

# График 5: Оценка эффективности vs Стаж.
col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Оценка vs Стаж")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    
    tenure_data = [filtered_df[filtered_df['time_spend_company'] == t]['last_evaluation'].dropna() 
                   for t in sorted(filtered_df['time_spend_company'].unique())]
    
    bp = ax5.boxplot(tenure_data, labels=sorted(filtered_df['time_spend_company'].unique()), 
                     patch_artist=True, showmeans=True)
    
    for box in bp['boxes']:
        box.set_facecolor('lightblue')
    
    ax5.set_xlabel('Стаж в компании (лет)')
    ax5.set_ylabel('Оценка эффективности')
    ax5.set_title('Распределение оценок по стажу')
    st.pyplot(fig5)

# График 6: Несчастные случаи и увольнения.
with col6:
    st.subheader("6. Несчастные случаи vs Увольнения")
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    
    accident_left = filtered_df.groupby(['Work_accident', 'left']).size().unstack(fill_value=0)
    accident_left.columns = ['Работающие', 'Уволившиеся']
    accident_left.index = ['Нет', 'Да']
    
    accident_left.plot(kind='bar', ax=ax6, color=['green', 'red'], edgecolor='black')
    ax6.set_xlabel('Несчастный случай на работе')
    ax6.set_ylabel('Количество сотрудников')
    ax6.set_title('Влияние несчастных случаев на увольнение')
    ax6.legend()
    ax6.tick_params(axis='x', rotation=0)
    st.pyplot(fig6)
    
    if 'Да' in accident_left.index:
        with_accident = accident_left.loc['Да']['Уволившиеся'] / accident_left.loc['Да'].sum() * 100
        st.caption(f" При наличии несчастного случая увольняется {with_accident:.1f}%")

# График 7: Повышение за 5 лет и увольнения.
col7, col8 = st.columns(2)

with col7:
    st.subheader("7. Повышение vs Увольнение")
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    
    promo_left = filtered_df.groupby(['promotion_last_5years', 'left']).size().unstack(fill_value=0)
    promo_left.columns = ['Работающие', 'Уволившиеся']
    promo_left.index = ['Нет повышения', 'Было повышение']
    
    # Столбчатая диаграмма вместо круговой.
    promo_left.plot(kind='bar', ax=ax7, color=['green', 'red'], edgecolor='black')
    ax7.set_xlabel('Статус повышения')
    ax7.set_ylabel('Количество сотрудников')
    ax7.set_title('Увольнения в зависимости от повышения за 5 лет')
    ax7.legend()
    ax7.tick_params(axis='x', rotation=0)
    
    # Добавляем значения на столбцы.
    for container in ax7.containers:
        ax7.bar_label(container, fmt='%d', fontsize=10)
    
    st.pyplot(fig7)
    
    # Статистика.
    for status in promo_left.index:
        total = promo_left.loc[status].sum()
        if total > 0:
            left_pct = promo_left.loc[status]['Уволившиеся'] / total * 100
            st.caption(f"📊 {status}: уволилось {left_pct:.1f}%")

# График 8: Лучшие сотрудники по отделам.
with col8:
    st.subheader("8. Лучшие сотрудники по отделам")
    fig8, ax8 = plt.subplots(figsize=(12, 6))
    
    high_performers = filtered_df[filtered_df['last_evaluation'] > 0.8]
    
    if len(high_performers) > 0:
        dept_left = high_performers.groupby(['Department', 'left']).size().unstack(fill_value=0)
        dept_left.columns = ['Работающие', 'Уволившиеся']
        
        dept_left.plot(kind='bar', ax=ax8, color=['green', 'red'], edgecolor='black')
        ax8.set_xlabel('Департамент')
        ax8.set_ylabel('Количество лучших сотрудников')
        ax8.set_title('Увольнение лучших сотрудников (оценка > 0.8)')
        ax8.legend()
        ax8.tick_params(axis='x', rotation=45)
        st.pyplot(fig8)
        
        if 'Уволившиеся' in dept_left.columns and not dept_left['Уволившиеся'].empty:
            max_loss_dept = dept_left['Уволившиеся'].idxmax()
            max_loss_count = dept_left.loc[max_loss_dept, 'Уволившиеся']
            st.caption(f"Отдел с наибольшей потерей: {max_loss_dept} ({max_loss_count} чел.)")
    else:
        st.info("Нет лучших сотрудников (оценка > 0.8) в отфильтрованном наборе")
        fig8, ax8 = plt.subplots()
        ax8.text(0.5, 0.5, 'Нет данных для отображения', ha='center', va='center', fontsize=14)
        ax8.set_xlim(0, 1)
        ax8.set_ylim(0, 1)
        ax8.axis('off')
        st.pyplot(fig8)

# 5. ДОПОЛНИТЕЛЬНЫЕ ГРАФИКИ.
st.header("Дополнительный анализ")

col9, col10 = st.columns(2)

with col9:
    st.subheader("Корреляционная матрица")
    fig9, ax9 = plt.subplots(figsize=(10, 8))
    
    numeric_cols = ['satisfaction_level', 'last_evaluation', 'number_project', 
                    'average_montly_hours', 'time_spend_company', 'Work_accident', 
                    'left', 'promotion_last_5years']
    
    corr_matrix = filtered_df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, square=True, linewidths=0.5, ax=ax9)
    ax9.set_title('Корреляция между признаками')
    st.pyplot(fig9)

with col10:
    st.subheader("Общая динамика увольнений")
    fig10, ax10 = plt.subplots(figsize=(8, 8))
    
    left_counts = filtered_df['left'].value_counts()
    labels = ['Работающие', 'Уволившиеся']
    colors = ['lightgreen', 'lightcoral']
    explode = (0, 0.05)
    
    ax10.pie(left_counts, labels=labels, autopct='%1.1f%%', colors=colors,
             explode=explode, shadow=True, startangle=90)
    ax10.set_title(f'Всего сотрудников: {len(filtered_df)}')
    st.pyplot(fig10)

# 6. СЫРЫЕ ДАННЫЕ.
with st.expander("Показать сырые данные"):
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Скачать отфильтрованные данные (CSV)",
        data=csv,
        file_name="hr_filtered_data.csv",
        mime="text/csv",
    )

# 7. ВЫВОДЫ.
st.header("Ключевые выводы")

col11, col12 = st.columns(2)

with col11:
    st.info("""
    **Основные факторы увольнения:**
    - Низкая удовлетворенность (< 0.3): высокий риск увольнения
    - Оптимальное количество проектов: 3-5
    - Переработка (> 250 часов/мес): риск выгорания
    - Отсутствие повышения за 5 лет: высокий риск увольнения
    """)

with col12:
    st.success("""
    **Рекомендации:**
    1. Провести опрос среди сотрудников с низкой удовлетворенностью
    2. Оптимизировать нагрузку по проектам
    3. Внедрить программу удержания для отделов с высокой текучкой
    4. Регулярно пересматривать политику повышений
    """)

st.caption("HR Analytics Dashboard | Данные о сотрудниках компании")