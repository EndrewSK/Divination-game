import os
import msvcrt
import random
import time
import ctypes

LEVELS = {
    "Fácil": (10, 5),
    "Médio": (100, 7),
    "Difícil": (1000, 10),
    "Impossível": (10000, 10),
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def exit_game():
    clear()
    print("\n" * 5 + "\t\t\tAté mais! 👋", "\n" * 5)
    time.sleep(1)
    exit()

def pause():
    print("\n\t\tPressione qualquer tecla para continuar...")
    msvcrt.getch()

def configure_console():
    # This part will only work if cmd is opened as administrator
    # It is used to change the cmd screen size
    os.system('mode con: cols=80 lines=30')

    screen_width, screen_height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    cmd_width, cmd_height = 80 * 8, 30 * 16

    x, y = (screen_width - cmd_width) // 2, (screen_height - cmd_height) // 2
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    if hwnd:
        ctypes.windll.user32.MoveWindow(hwnd, x, y, cmd_width, cmd_height, True)

def print_centered(text):
    print(f"\t\t{text}")

def welcome():
    clear()
    print("\n" * 5)
    print_centered("=======================================")
    print_centered("        🎯 JOGO DE ADIVINHAÇÃO 🎯")
    print_centered("=======================================\n")
    print_centered("      Desenvolvimento de Sistemas")
    print_centered(" Colégio Técnico de Campinas - Unicamp")
    print_centered("          By Endrew Oliveira")
    print_centered("=======================================\n")
    
    pause()
    choose_level()

def choose_level():
    options = list(LEVELS.keys()) + ["Sair"]
    current_index = 0

    while True:
        clear()
        print("\n" * 4)
        print_centered("=====================================")
        print_centered("   Escolha um nível de dificuldade")
        print_centered("=====================================\n")
        print_centered("   Use ↑ e ↓ para navegar e Enter para selecionar.\n")

        for index, option in enumerate(options):
            prefix = "-> " if index == current_index else "   "
            print(f"\t\t{prefix}{option}")

        key = msvcrt.getch()
        if key == b'\xe0':
            arrow_key = msvcrt.getch()
            if arrow_key == b'H':
                current_index = (current_index - 1) % len(options)
            elif arrow_key == b'P':
                current_index = (current_index + 1) % len(options)
        elif key == b'\r':
            if options[current_index] == "Sair":
                exit_game()
            game(options[current_index])
            return

def game(mode):
    clear()
    print("\n" * 5)
    print_centered("=====================================")
    print_centered(f"    🎮 Modo escolhido: {mode}")
    print_centered("=====================================\n")
    print("\t\tPressione qualquer tecla para iniciar ou X para voltar.")

    key = msvcrt.getch().decode('utf-8').lower()
    if key == "x":
        choose_level()
    else:
        instructions(mode)

def instructions(mode):
    clear()
    max_num, attempts = LEVELS[mode]

    print("\n" * 4)
    print_centered("===================================")
    print_centered("           📜 REGRAS 📜")
    print_centered("===================================\n")
    print_centered(f"• Um número de 0 a {max_num} será escolhido.")
    print_centered(f"• Você tem {attempts} tentativas para acertar.\n")

    if mode != "Impossível":
        print_centered("• Se errar, receberá uma dica (maior ou menor).\n")

    print_centered("• Cada erro reduz suas tentativas.")
    print_centered("• Se acabar suas tentativas, é GAME OVER! ☠️")
    print_centered("• Se acertar o número, você vence! 🏆\n")

    pause()
    play_game(mode, max_num, attempts)

def play_game(mode, max_num, attempts):
    drawn = random.randint(0, max_num)

    while attempts > 0:
        clear()
        print("\n" * 4)
        print_centered("=======================================")
        print_centered("         🎯 Adivinhe o número! ")
        print_centered("=======================================\n")
        print_centered(f"Tentativas restantes: {attempts}")

        try:
            guess = int(input(f"\t\tDigite um número entre 0 e {max_num}: "))
        except ValueError:
            print("\n\t\t❌ Entrada inválida! Digite um número válido.")
            pause()
            continue

        if guess == drawn:
            print("\n\t\t🎉 Parabéns! Você acertou! 🎉")
            pause()
            return welcome()
        
        attempts -= 1
        if attempts == 0:
            print("\n\t\t💀 GAME OVER! O número era:", drawn)
        elif mode != "Impossível":
            hint = "maior" if guess < drawn else "menor"
            print(f"\n\t\t❌ Errado! O número é {hint}.")

        pause()

    welcome()

if __name__ == "__main__":
    configure_console()
    welcome()