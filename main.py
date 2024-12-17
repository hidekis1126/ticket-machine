import tkinter as tk
from tkinter import ttk, messagebox
from data_loader import load_data
from station_move import StationMove

STATION_NUMBERS = {
    "北千里": "HK95", "山田": "HK94", "南千里": "HK93",
    "千里山": "HK92", "関大前": "HK91", "豊津": "HK90",
    "吹田": "HK89", "下新庄": "HK88", "淡路": "HK63"
}

class TicketMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("券売機")
        self.geometry("300x300")
        self.resizable(False, False)

        self.current_station = "北千里"
        self.inserted_amount = 0
        self.ticket_fare = None
        self.distances, self.fares = load_data('calc.xlsx', 'range')

        self.end_station_var = tk.StringVar()
        self.initialize_purchase_ui()

    def sort_stations_by_number(self, station_list):
        return sorted(station_list, key=lambda s: STATION_NUMBERS.get(s, ""), reverse=True)

    def initialize_purchase_ui(self):
        self.clear_ui()
        tk.Label(self, text=f"出発駅: {self.current_station}").grid(row=0, column=0)
        filtered_stations = [
            station for station in self.sort_stations_by_number(STATION_NUMBERS.keys())
            if station != self.current_station
        ]
        self.end_station_var.set("")
        end_station_combo = ttk.Combobox(self, textvariable=self.end_station_var, values=filtered_stations)
        end_station_combo.grid(row=1, column=0)

        tk.Button(self, text="運賃を計算", command=self.calculate_fare_display).grid(row=2, column=0)
        self.fare_label = tk.Label(self, text="")
        self.fare_label.grid(row=3, column=0)

        self.amount_label = tk.Label(self, text=f"投入金額: {self.inserted_amount}円")
        self.amount_label.grid(row=4, column=0)

        self.entry_amount = tk.Entry(self)
        self.entry_amount.grid(row=5, column=0)
        tk.Button(self, text="入金", command=self.add_money).grid(row=5, column=1)

        tk.Button(self, text="切符購入", command=self.buy_ticket).grid(row=6, column=0)

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def calculate_fare_display(self):
        end = self.end_station_var.get()
        fare = self.fares.get((self.current_station, end), "運賃不明")
        display_text = f"{fare}円" if isinstance(fare, int) else "運賃が不明です"
        self.fare_label.config(text=f"{self.current_station}→{end}: {display_text}")

    def add_money(self):
        try:
            amount = int(self.entry_amount.get())
            self.inserted_amount += amount
            self.amount_label.config(text=f"投入金額: {self.inserted_amount}円")
        except ValueError:
            messagebox.showerror("エラー", "正しい金額を入力してください")

    def buy_ticket(self):
        end = self.end_station_var.get()
        fare = self.fares.get((self.current_station, end), "運賃不明")
        if fare == "運賃不明" or self.inserted_amount < fare:
            messagebox.showerror("エラー", "金額が足りないか運賃が不明です")
            return
        self.ticket_fare = fare
        self.switch_to_station_move()

    def switch_to_station_move(self):
        self.clear_ui()
        station_move_frame = StationMove(
            self, current_station=self.current_station,
            stations=list(STATION_NUMBERS.keys()),
            ticket_fare=self.ticket_fare, fares=self.fares,
            switch_to_purchase=self.switch_to_purchase
        )
        station_move_frame.grid(row=0, column=0)

    def switch_to_purchase(self, new_station):
        self.current_station = new_station
        self.initialize_purchase_ui()

if __name__ == "__main__":
    app = TicketMachineApp()
    app.mainloop()

