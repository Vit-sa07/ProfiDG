import pandas as pd
import numpy as np

# Коэффициенты
l = [0.874, 0.974, 0.996, 1, 1.01]
c = [1.15, 1.13, 1.14, 1.1, 1.15]


# Функция для вычисления значений
def calculate_values(data):
    Rasch_Tsr = np.zeros((5,))
    Rasch_Tmax = np.zeros((5,))
    Rasch_TmaxM = np.zeros((5,))

    for r in range(5):
        Rasch_Tsr[r] = data.iloc[r, :].mean()  # Средняя температура по высоте
        Rasch_Tmax[r] = data.iloc[r, :].max()  # Максимальная температура по высоте

    # Расчет Tp
    Tp = np.round((Rasch_Tsr[1] + 2 * Rasch_Tsr[2] + Rasch_Tsr[3]) / 4)

    # Применение коэффициентов и расчет значений с учетом коэффициентов
    for r in range(5):
        Rasch_TmaxM[r] = Rasch_Tmax[r] + (875 - Tp) * c[r]

    return Rasch_TmaxM, Tp


# Функция для проверки данных и предоставления рекомендаций
def check_data(data, Rasch_TmaxM):
    suggestions = []
    num_columns = data.shape[1]

    for index, row in data.iterrows():
        for col in range(num_columns):
            value = row.iloc[col]
            if value > Rasch_TmaxM[index]:
                left_therm = (col - 1) % num_columns
                right_therm = (col + 1) % num_columns
                suggestions.append(
                    f"Высота {index + 1}, Термопара {col + 1}, Значение: {value}. Превышает допустимое значение {Rasch_TmaxM[index]}. "
                    f"Рекомендуется замена форсунки с меньшим расходом топлива. Соседние термопары: {left_therm + 1} ({row.iloc[left_therm]}), {right_therm + 1} ({row.iloc[right_therm]}).")

    if not suggestions:
        suggestions.append("Температурное поле соответствует ТУ.")

    return suggestions


# Основная функция для обработки Excel файла
def main():
    # Чтение Excel файла
    file_path = 'engine_data.xlsx'
    data = pd.read_excel(file_path, header=None)

    # Извлечение данных эксперимента
    experiment_data = data.iloc[1:6, 1:17].reset_index(drop=True)  # Сбрасываем индексы для корректной обработки

    # Вычисление необходимых значений
    Rasch_TmaxM, Tp = calculate_values(experiment_data)

    # Проверка данных и получение рекомендаций
    suggestions = check_data(experiment_data, Rasch_TmaxM)

    # Вывод рекомендаций
    for suggestion in suggestions:
        print(suggestion)


if __name__ == "__main__":
    main()
