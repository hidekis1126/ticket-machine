import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional

class StationMove(tk.Frame):
    def __init__(
        self,
        master,
        current_station="北千里",
        stations=None,
        ticket_fare=None,
        fares=None,
        switch_to_purchase: Optional[Callable[[str], None]] = None,  # 型ヒント追加
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.master = master
        self.current_station = current_station
        self.selected_station = current_station
        self.stations = stations or []
        self.ticket_fare = ticket_fare
        self.fares = fares or {}

        # switch_to_purchaseがNoneでないことを確認
        if switch_to_purchase is None:
            raise ValueError("switch_to_purchase が None です。正しい関数を渡してください。")
        self.switch_to_purchase = switch_to_purchase

        if not self.stations:
            messagebox.showerror("エラー", "駅リストが指定されていません。")
            return

        if not self.fares:
            raise ValueError("運賃データが指定されていません。")

        self.create_widgets()

    def create_widgets(self):
        self.label_current_station = tk.Label(self, text=f"現在地: {self.selected_station}")
        self.label_current_station.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        fare_text = f"{self.ticket_fare}円" if self.ticket_fare is not None else "運賃が設定されていません"
        self.label_ticket_fare = tk.Label(self, text=f"購入した切符の運賃: {fare_text}")
        self.label_ticket_fare.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.button_prev_station = tk.Button(self, text="前の駅", command=self.move_to_prev_station)
        self.button_prev_station.grid(row=2, column=0, padx=10, pady=10)

        self.button_next_station = tk.Button(self, text="次の駅", command=self.move_to_next_station)
        self.button_next_station.grid(row=2, column=1, padx=10, pady=10)

        self.button_exit_station = tk.Button(self, text="降車", command=self.exit_station)
        self.button_exit_station.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def move_to_next_station(self):
        current_index = self.stations.index(self.selected_station)
        if current_index < len(self.stations) - 1:
            self.selected_station = self.stations[current_index + 1]
            self.label_current_station.config(text=f"現在地: {self.selected_station}")

    def move_to_prev_station(self):
        current_index = self.stations.index(self.selected_station)
        if current_index > 0:
            self.selected_station = self.stations[current_index - 1]
            self.label_current_station.config(text=f"現在地: {self.selected_station}")

    def exit_station(self):
        if self.selected_station == self.current_station:
            messagebox.showerror("エラー", "現在地と同じ駅では降車できません。")
            return

        fare = self.fares.get((self.current_station, self.selected_station), "運賃不明")
        if fare == "運賃不明":
            messagebox.showerror("エラー", "指定された駅間の運賃が不明です。")
            return

        if self.ticket_fare >= fare:
            messagebox.showinfo("降車", f"{self.selected_station}で降車しました。\nご利用ありがとうございました。")
            self.switch_to_purchase(self.selected_station)
        else:
            shortage = fare - self.ticket_fare
            messagebox.showerror("エラー", f"運賃が不足しています。あと{shortage}円必要です。")
