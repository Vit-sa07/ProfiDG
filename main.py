import pandas as pd
import numpy as np

# Коэффициенты
l = [0.874, 0.974, 0.996, 1, 1.01]
c = [1.15, 1.13, 1.14, 1.1, 1.15]


# Функция для вычисления значений
def calculate_values(data):
    Rasch_Tsr = np.zeros((5,))
    Rasch_Tmax = np.zeros((5,))
    Rasch_TsrM = np.zeros((5,))
    Rasch_TmaxM = np.zeros((5,))

    for r in range(5):
        Rasch_Tsr[r] = data.iloc[r, :].mean()  # Средняя температура по высоте
        Rasch_Tmax[r] = data.iloc[r, :].max()  # Максимальная температура по высоте

    # Расчет Tp
    Tp = np.round((Rasch_Tsr[0] + Rasch_Tsr[1] + 2 * Rasch_Tsr[3]) / 4)

    # Применение коэффициентов и расчет значений с учетом коэффициентов
    for r in range(5):
        Rasch_TsrM[r] = Rasch_Tsr[r] + 870 - Tp - l[r]
        Rasch_TmaxM[r] = Rasch_Tmax[r] + 875 - Tp - c[r]

    return Rasch_TsrM, Rasch_TmaxM, Tp


# Функция для проверки данных и предоставления рекомендаций
def check_data(data, Rasch_TsrM, Rasch_TmaxM):
    suggestions = []
    num_columns = data.shape[1]

    for index, row in data.iterrows():
        for col in range(num_columns):
            value = row.iloc[col]
            if value > Rasch_TmaxM[index]:
                left_therm = (col - 1) % num_columns + 1
                right_therm = (col + 1) % num_columns + 1
                suggestions.append(
                    f"Высота {index + 1}, Термопара {col + 1}: Значение {value} превышает максимальный предел {Rasch_TmaxM[index]}. "
                    f"Рекомендуется замена ближайшей форсунки с большим распылением. Соседние термопары: {left_therm}, {right_therm}.")
            elif value < Rasch_TsrM[index]:
                left_therm = (col - 1) % num_columns + 1
                right_therm = (col + 1) % num_columns + 1
                suggestions.append(
                    f"Высота {index + 1}, Термопара {col + 1}: Значение {value} ниже минимального предела {Rasch_TsrM[index]}. "
                    f"Рекомендуется замена ближайшей форсунки с меньшим распылением. Соседние термопары: {left_therm}, {right_therm}.")

    return suggestions


# Основная функция для обработки Excel файла
def main():
    # Чтение Excel файла
    file_path = 'engine_data.xlsx'
    data = pd.read_excel(file_path, header=None)

    # Извлечение данных эксперимента
    experiment_data = data.iloc[1:6, 1:17].reset_index(drop=True)  # Сбрасываем индексы 

    # Вычисление необходимых значений
    Rasch_TsrM, Rasch_TmaxM, Tp = calculate_values(experiment_data)

    # Проверка данных и получение рекомендаций
    suggestions = check_data(experiment_data, Rasch_TsrM, Rasch_TmaxM)

    # Вывод рекомендаций
    for suggestion in suggestions:
        print(suggestion)


if __name__ == "__main__":
    main()
