import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt

# Lista dostępnych funkcji
def predefined_function(x, choice):
    if choice == 1:
        return np.sin(x) + x**2
    elif choice == 2:
        return np.exp(-x**2)
    elif choice == 3:
        return np.log(x + 10)  # Zakładamy, że x + 10 > 0
    elif choice == 4:
        return x**3 - 2 * x
    else:
        raise ValueError("Niepoprawny wybór funkcji!")

# Funkcja obliczająca całkę dla danego przedziału
def trapezoidal_rule(args):
    a, b, n, choice = args
    h = (b - a) / n
    result = 0.5 * (predefined_function(a, choice) + predefined_function(b, choice))
    for i in range(1, n):
        x = a + i * h
        result += predefined_function(x, choice)
    return result * h

# Funkcja do równoległego obliczania całki
def parallel_integration(a, b, n, num_processes, choice):
    sub_ranges = []
    step = (b - a) / num_processes
    for i in range(num_processes):
        sub_a = a + i * step
        sub_b = sub_a + step
        sub_ranges.append((sub_a, sub_b, n // num_processes, choice))

    with Pool(processes=num_processes) as pool:
        results = pool.map(trapezoidal_rule, sub_ranges)
    return sum(results)

# Funkcja do rysowania wykresu i zapisywania go jako plik obrazu
def plot_function(a, b, choice):
    x = np.linspace(a, b, 1000)
    y = predefined_function(x, choice)
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f"Funkcja (wybór: {choice})")
    plt.fill_between(x, y, alpha=0.3, color="orange", label="Obszar całkowania")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Wykres funkcji i zakres całkowania")
    plt.legend()
    plt.grid()

    # Zapis wykresu jako plik PNG
    plt.savefig("wykres.png")
    print("Wykres został zapisany jako 'wykres.png'.")

# Główna funkcja programu
def main():
    print("Wybierz funkcję:")
    print("1. f(x) = sin(x) + x^2")
    print("2. f(x) = exp(-x^2)")
    print("3. f(x) = log(x + 10)")
    print("4. f(x) = x^3 - 2 * x")
    try:
        choice = int(input("Wybór funkcji (1-4): "))
        if choice not in [1, 2, 3, 4]:
            raise ValueError("Niepoprawny wybór funkcji!")

        a = float(input("Podaj początek zakresu całkowania (a): "))
        b = float(input("Podaj koniec zakresu całkowania (b): "))
        if b <= a:
            raise ValueError("Koniec zakresu (b) musi być większy niż początek zakresu (a)!")

        n = int(input("Podaj liczbę podprzedziałów (n): "))
        if n <= 0:
            raise ValueError("Liczba podprzedziałów musi być większa niż 0!")

        num_processes = int(input("Podaj liczbę procesorów: "))
        if num_processes <= 0:
            raise ValueError("Liczba procesorów musi być większa niż 0!")

        # Obliczenie całki
        result = parallel_integration(a, b, n, num_processes, choice)

        # Wyświetlenie wyników
        print("\n--- Wyniki ---")
        print(f"Wybrana funkcja: {choice}")
        print(f"Zakres całkowania: [{a}, {b}]")
        print(f"Liczba podprzedziałów: {n}")
        print(f"Liczba procesorów: {num_processes}")
        print(f"Wynik całki: {result:.6f}")

        # Rysowanie wykresu funkcji i zapisywanie go do pliku
        plot_function(a, b, choice)

    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    main()
