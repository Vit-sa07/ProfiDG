import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Коэффициенты
l = [0.874, 0.974, 0.996, 1, 1.01]
c = [1.15, 1.13, 1.14, 1.1, 1.15]

# Статические ограничения
TmaxM_limits = [1025, 1025, 1025, 1040, 1055]


# Функция для вычисления значений
def calculate_values(data):
    Rasch_Tsr = np.zeros((5,))
    Rasch_Tmax = np.zeros((5,))
    Rasch_TmaxM = np.zeros((5,))
    Rasch_TsrM = np.zeros((5,))

    for r in range(5):
        Rasch_Tsr[r] = data.iloc[r, :].mean()  # Средняя температура по высоте
        Rasch_Tmax[r] = data.iloc[r, :].max()  # Максимальная температура по высоте

    # Расчет Tp
    Tp = np.round((Rasch_Tsr[1] + 2 * Rasch_Tsr[2] + Rasch_Tsr[3]) / 4)

    # Применение коэффициентов и расчет значений с учетом коэффициентов
    for r in range(5):
        Rasch_TmaxM[r] = Rasch_Tmax[r] + (875 - Tp) * c[r]
        Rasch_TsrM[r] = Rasch_Tsr[r] + (870 - Tp) * l[r]

    return Rasch_TsrM, Rasch_TmaxM, Tp


# Функция для проверки данных и предоставления рекомендаций
def check_data(data, Rasch_TmaxM):
    suggestions = []
    num_columns = data.shape[1]
    thermopar_numbers = data.columns[1:].astype(int).tolist()

    for index, row in data.iterrows():
        for col in range(num_columns):
            value = row.iloc[col]
            if value > TmaxM_limits[index]:
                left_therm = (col - 1) % num_columns
                right_therm = (col + 1) % num_columns
                suggestions.append(
                    f"Высота {index + 1}, Термопара {thermopar_numbers[col]}, Значение: {value}. Превышает допустимое значение {TmaxM_limits[index]}. "
                    f"Рекомендуется замена форсунки с меньшим расходом топлива. Соседние термопары: {thermopar_numbers[left_therm]} ({row.iloc[left_therm]}), {thermopar_numbers[right_therm]} ({row.iloc[right_therm]}).")

    if not suggestions:
        suggestions.append("Температурное поле соответствует ТУ.")

    return suggestions


def draw_layout(thermopar_numbers):
    num_thermocouples = len(thermopar_numbers)
    angles = np.linspace(0, 2 * np.pi, num_thermocouples, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Радиус для термопар и форсунок
    radius = 1.0
    for angle, label in zip(angles, thermopar_numbers):
        ax.text(angle, radius, f'TP{label}', horizontalalignment='center', verticalalignment='center')

    ax.set_ylim(0, 1.1)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title('Расположение термопар и форсунок', va='bottom')
    plt.show()


# Основная функция для обработки Excel файла
def main():
    # Чтение Excel файла
    file_path = 'engine_data.xlsx'
    data = pd.read_excel(file_path, header=None)

    # Извлечение номеров термопар и данных эксперимента
    thermopar_numbers = data.iloc[0, 1:].astype(int).tolist()
    experiment_data = data.iloc[1:6, 1:17].reset_index(drop=True)  # Сбрасываем индексы для корректной обработки

    # Вычисление необходимых значений
    Rasch_TsrM, Rasch_TmaxM, Tp = calculate_values(experiment_data)

    # Проверка данных и получение рекомендаций
    suggestions = check_data(experiment_data, Rasch_TmaxM)

    # Вывод рекомендаций
    for suggestion in suggestions:
        print(suggestion)

    if "Температурное поле соответствует ТУ." not in suggestions:
        # Отрисовка схемы расположения термопар и форсунок
        draw_layout(thermopar_numbers)


if __name__ == "__main__":
    main()
