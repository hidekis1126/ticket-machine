import os
import sys
import openpyxl
from tkinter import messagebox
from fare_calculator import calculate_fare

def get_resource_path(filename):
    """リソースファイルのパスを取得"""
    if getattr(sys, 'frozen', False):  # PyInstallerで実行時
        base_path = sys._MEIPASS  # type: ignore　# PyInstallerの一時フォルダ
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)

def load_data(filename, sheetname):
    """Excelファイルからデータを読み込み、駅間の距離と運賃の辞書を作成"""
    # ファイルパスを修正
    file_path = get_resource_path(filename)

    distances = {}
    fares = {}

    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook[sheetname]
    except FileNotFoundError:
        messagebox.showerror("エラー", f"{file_path} が見つかりません。")
        return distances, fares
    except KeyError:
        messagebox.showerror("エラー", f"シート {sheetname} が存在しません。")
        return distances, fares
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました: {e}")
        return distances, fares

    try:
        header = [cell.value for cell in worksheet[1][1:]]

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            start_station = row[0]
            if not start_station:
                continue

            for end_station, distance in zip(header, row[1:]):
                if end_station and distance is not None:
                    distances[(start_station, end_station)] = distance
                    fares[(start_station, end_station)] = calculate_fare(distance)

    except Exception as e:
        messagebox.showerror("エラー", f"データ読み込み中にエラーが発生しました: {e}")

    return distances, fares

