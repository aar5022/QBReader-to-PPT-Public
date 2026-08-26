from typing import Any

import tkinter as tk
from tkinter import messagebox

from qbreader import Difficulty

from qbtppt.models import AppSettings, PacketSelection, SelectionOptions
from qbtppt.trivia.categories import category_value, selectable_categories
from qbtppt.trivia.distributions import DISTRIBUTIONS, NO_DISTRIBUTION, RANDOM_SOURCE_MODE, SOURCE_MODES, get_distribution_buckets


def select_source_mode(default_value: str) -> str:
    root = tk.Tk()
    root.title("Select Question Source")
    root.geometry("400x190")
    ok_pressed = tk.BooleanVar(value=False)
    selected_source = tk.StringVar(value=default_value if default_value in SOURCE_MODES else RANDOM_SOURCE_MODE)

    tk.Label(root, text="Choose how to build the deck").pack(anchor="center", pady=(22, 10))
    for option in SOURCE_MODES:
        tk.Radiobutton(root, text=option, variable=selected_source, value=option).pack(anchor="center", pady=5)

    def on_ok() -> None:
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=16)
    root.wait_variable(ok_pressed)

    return selected_source.get()


def infer_year_from_set_name(set_name: str) -> str:
    for token in set_name.replace("-", " ").split():
        if token.isdigit() and len(token) == 4:
            return token
    return ""


def select_set_from_list(set_names: tuple[str, ...]) -> str:
    root = tk.Tk()
    root.title("Select Set")
    root.geometry("850x520")
    ok_pressed = tk.BooleanVar(value=False)
    search_text = tk.StringVar(value="")
    selected_set = tk.StringVar(value="")

    tk.Label(root, text="Search sets").pack(anchor="w", padx=12, pady=(12, 4))
    search_entry = tk.Entry(root, textvariable=search_text)
    search_entry.pack(fill="x", padx=12)

    tk.Label(root, text="Year    Set").pack(anchor="w", padx=12, pady=(8, 0))
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=12, pady=8)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Consolas", 10), exportselection=False)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    filtered_sets: list[str] = []

    def row_for_set(set_name: str) -> str:
        year = infer_year_from_set_name(set_name) or "----"
        return f"{year:<6}  {set_name}"

    def refresh_list(*_args) -> None:
        search = search_text.get().lower().strip()
        filtered_sets.clear()
        filtered_sets.extend([set_name for set_name in set_names if search in set_name.lower()])
        listbox.delete(0, tk.END)
        for set_name in filtered_sets:
            listbox.insert(tk.END, row_for_set(set_name))

    def on_select(_event=None) -> None:
        selection = listbox.curselection()
        if selection:
            selected_set.set(filtered_sets[selection[0]])

    def on_ok() -> None:
        if not selected_set.get():
            messagebox.showerror("No Set Selected", "Choose a set before continuing.")
            return
        ok_pressed.set(True)
        root.destroy()

    search_text.trace_add("write", refresh_list)
    listbox.bind("<<ListboxSelect>>", on_select)
    listbox.bind("<Double-Button-1>", lambda _event: on_ok())

    tk.Button(root, text="OK", command=on_ok).pack(pady=(0, 12))
    refresh_list()
    search_entry.focus_set()
    root.wait_variable(ok_pressed)

    return selected_set.get()


def select_packet_number(set_name: str, packet_count: int) -> int:
    root = tk.Tk()
    root.title("Select Packet")
    root.geometry("500x210")
    ok_pressed = tk.BooleanVar(value=False)
    packet_number_var = tk.IntVar(value=1)
    selected_packet_number = [1]

    tk.Label(root, text=set_name, wraplength=460, justify="center").pack(anchor="center", pady=(20, 8))
    tk.Label(root, text=f"Packet number (1-{packet_count})").pack(anchor="center", pady=(0, 4))
    tk.Spinbox(root, from_=1, to=packet_count, textvariable=packet_number_var, width=8).pack(anchor="center")

    def on_ok() -> None:
        packet_number = packet_number_var.get()
        if packet_number < 1 or packet_number > packet_count:
            messagebox.showerror("Invalid Packet", f"Packet number must be between 1 and {packet_count}.")
            return
        selected_packet_number[0] = packet_number
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=18)
    root.wait_variable(ok_pressed)

    return selected_packet_number[0]


def select_existing_packet(set_names: tuple[str, ...], packet_count_loader) -> PacketSelection:
    set_name = select_set_from_list(set_names)
    packet_count = packet_count_loader(set_name)
    packet_number = select_packet_number(set_name, packet_count)
    return PacketSelection(set_name=set_name, packet_number=packet_number)


def select_difficulties() -> list[int]:
    diff_names = [diff.name for diff in Difficulty]
    difficulties = range(11)
    chosen_difficulties = []

    root = tk.Tk()
    root.title("Select Difficulties")
    root.geometry("400x400")
    ok_pressed = tk.BooleanVar(value=False)

    def update_difficulties(index: int, var: tk.IntVar) -> None:
        difficulty = difficulties[index]
        if var.get() == 1:
            if difficulty not in chosen_difficulties:
                chosen_difficulties.append(difficulty)
        elif difficulty in chosen_difficulties:
            chosen_difficulties.remove(difficulty)

    for i in range(11):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(
            root,
            text=f"{diff_names[i]}",
            variable=var,
            command=lambda i=i, var=var: update_difficulties(i, var),
        )
        checkbox.pack(anchor="center")

    def on_ok() -> None:
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=20)
    root.wait_variable(ok_pressed)

    return chosen_difficulties


def select_categories() -> list[Any]:
    cat_names = selectable_categories()
    chosen_categories = []

    root = tk.Tk()
    root.title("Select Categories")
    root.geometry("400x400")
    ok_pressed = tk.BooleanVar(value=False)

    def update_categories(cat_name: Any, var: tk.IntVar) -> None:
        if var.get() == 1:
            if cat_name not in chosen_categories:
                chosen_categories.append(cat_name)
        elif cat_name in chosen_categories:
            chosen_categories.remove(cat_name)

    for cat_name in cat_names:
        var = tk.IntVar(value=1)
        chosen_categories.append(cat_name)
        checkbox = tk.Checkbutton(
            root,
            text=category_value(cat_name),
            variable=var,
            command=lambda cat_name=cat_name, var=var: update_categories(cat_name, var),
        )
        checkbox.pack(anchor="center")

    def on_ok() -> None:
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=20)
    root.wait_variable(ok_pressed)

    return chosen_categories


def select_distribution() -> str:
    root = tk.Tk()
    root.title("Select Category Distribution")
    root.geometry("400x220")
    ok_pressed = tk.BooleanVar(value=False)
    selected_distribution = tk.StringVar(value=NO_DISTRIBUTION)

    for option in DISTRIBUTIONS:
        radio = tk.Radiobutton(
            root,
            text=option,
            variable=selected_distribution,
            value=option,
        )
        radio.pack(anchor="center", pady=8)

    def on_ok() -> None:
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=20)
    root.wait_variable(ok_pressed)

    return selected_distribution.get()


def select_year_range(min_default: int, max_default: int) -> tuple[int, int]:
    root = tk.Tk()
    root.title("Select Year Range")
    root.geometry("400x240")
    ok_pressed = tk.BooleanVar(value=False)
    min_year_var = tk.IntVar(value=min_default)
    max_year_var = tk.IntVar(value=max_default)
    selected_year_range = [min_default, max_default]

    tk.Label(root, text="Minimum year").pack(anchor="center", pady=(20, 4))
    tk.Spinbox(root, from_=min_default, to=max_default, textvariable=min_year_var, width=8).pack(anchor="center")

    tk.Label(root, text="Maximum year").pack(anchor="center", pady=(16, 4))
    tk.Spinbox(root, from_=min_default, to=max_default, textvariable=max_year_var, width=8).pack(anchor="center")

    def on_ok() -> None:
        min_year = min_year_var.get()
        max_year = max_year_var.get()
        if min_year > max_year:
            messagebox.showerror("Invalid Year Range", "Minimum year cannot be greater than maximum year.")
            return
        selected_year_range[0] = min_year
        selected_year_range[1] = max_year
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=20)
    root.wait_variable(ok_pressed)

    return tuple(selected_year_range)


def select_include_bonuses(default_value: bool) -> bool:
    root = tk.Tk()
    root.title("Include Bonuses")
    root.geometry("400x180")
    ok_pressed = tk.BooleanVar(value=False)
    include_bonuses = tk.BooleanVar(value=default_value)
    selected_include_bonuses = [default_value]

    tk.Label(root, text="Include bonuses after the tossups?").pack(anchor="center", pady=(24, 10))

    tk.Radiobutton(root, text="Yes", variable=include_bonuses, value=True).pack(anchor="center", pady=4)
    tk.Radiobutton(root, text="No", variable=include_bonuses, value=False).pack(anchor="center", pady=4)

    def on_ok() -> None:
        selected_include_bonuses[0] = include_bonuses.get()
        ok_pressed.set(True)
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=16)
    root.wait_variable(ok_pressed)

    return selected_include_bonuses[0]


def collect_selection_options(settings: AppSettings) -> SelectionOptions:
    difficulties = select_difficulties()
    difficulties.sort()
    min_year, max_year = select_year_range(settings.min_year, settings.max_year)
    distribution = select_distribution()
    tossup_count, distribution_buckets = get_distribution_buckets(distribution, settings.manual_tossup_count)
    categories = [] if distribution_buckets else select_categories()
    include_bonuses = select_include_bonuses(settings.include_bonuses_default)
    bonus_count, _ = get_distribution_buckets(distribution, settings.manual_bonus_count)

    return SelectionOptions(
        source_mode=RANDOM_SOURCE_MODE,
        difficulties=difficulties,
        min_year=min_year,
        max_year=max_year,
        distribution=distribution,
        categories=categories,
        tossup_count=tossup_count,
        include_bonuses=include_bonuses,
        bonus_count=bonus_count,
    )
