import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import ctypes
import xml.etree.ElementTree as ET
import glob
import time
import wmi

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def get_adapter_names():
    adapter_map = {}
    try:
        c = wmi.WMI()
        for adapter in c.Win32_NetworkAdapter():
            guid = adapter.GUID
            name = adapter.Name
            if guid and name:
                clean_guid = guid.upper().replace("{", "").replace("}", "")
                adapter_map[clean_guid] = name
    except Exception as e:
        print("Erro com WMI:", e)
    return adapter_map

def get_ascii_key(profile):
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"], text=True, encoding="utf-8", errors="ignore")
        for line in output.splitlines():
            if "Conteúdo da Chave" in line or "Key Content" in line:
                return line.split(":")[1].strip()
    except:
        return ""
    return ""

def extract_profiles():
    results = []
    xml_paths = glob.glob(r"C:\ProgramData\Microsoft\Wlansvc\Profiles\Interfaces\*\*.xml")
    adapter_names = get_adapter_names()

    for path in xml_paths:
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            ns = {"ms": "http://www.microsoft.com/networking/WLAN/profile/v1"}

            ssid = root.find(".//ms:name", ns).text
            key_material = root.find(".//ms:keyMaterial", ns)
            key_ascii = get_ascii_key(ssid)
            key_hex = key_material.text.encode("utf-8").hex() if key_material is not None else ""

            auth = root.find(".//ms:authentication", ns)
            encrypt = root.find(".//ms:encryption", ns)
            conn_type = root.find(".//ms:connectionType", ns)

            raw_guid = path.split("\\")[-2]
            adapter_guid = raw_guid.upper().replace("{", "").replace("}", "")
            adapter_name = adapter_names.get(adapter_guid, "Desconhecido")

            info = {
                "SSID": ssid,
                "Senha (ASCII)": key_ascii,
                "Senha (HEX)": key_hex,
                "Adaptador": adapter_name,
                "GUID Adaptador": raw_guid,
                "Autenticação": auth.text if auth is not None else "",
                "Criptografia": encrypt.text if encrypt is not None else "",
                "Tipo de Conexão": conn_type.text if conn_type is not None else "",
                "Modificado em": time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(path))),
                "Caminho do Perfil": path
            }

            results.append(info)
        except Exception as e:
            print("Erro ao processar XML:", e)
    return results

def show_profiles():
    tree.delete(*tree.get_children())
    global profile_data
    profile_data = extract_profiles()
    for profile in profile_data:
        values = [profile[col] for col in tree["columns"]]
        tree.insert("", "end", values=values)

def reset_ui():
    tree.delete(*tree.get_children())

def copy_cell(event):
    item_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if not item_id or not column:
        return
    col_index = int(column[1:]) - 1
    value = tree.item(item_id, "values")[col_index]

    top = tk.Toplevel(root)
    top.title("Copiar Informação")
    top.configure(bg="#111111")
    top.geometry("500x120")
    top.resizable(False, False)

    label = tk.Label(top, text="Clique para copiar:", font=("Segoe UI", 10), bg="#111111", fg="white")
    label.pack(pady=(10, 0))

    entry = tk.Entry(top, font=("Segoe UI", 11), fg="black", bg="white", relief="flat", justify="left")
    entry.insert(0, value)
    entry.configure(state="readonly")
    entry.pack(padx=20, pady=10, fill="x")

    def copiar():
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()
        top.destroy()

    btn = tk.Button(top, text="📋 Copiar", command=copiar,
                    font=("Segoe UI", 10, "bold"),
                    bg="white", fg="black", relief="flat", padx=10, pady=5, cursor="hand2")
    btn.pack(pady=(0, 10))

# ===================== GUI ===================== #

root = tk.Tk()
root.title("DarkFeather - Wireless Connection PRO")
root.geometry("1280x600")
root.configure(bg="#111111")

style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview", background="#111111", foreground="white", fieldbackground="#111111",
                rowheight=28, font=("Segoe UI", 10))
style.map("Treeview", background=[("selected", "#333333")])
style.configure("Treeview.Heading", background="#1a1a1a", foreground="white", font=("Segoe UI", 10, "bold"))

header = tk.Label(root, text="🦅 DarkFeather - Redes Wi-Fi Salvas", font=("Segoe UI", 16, "bold"),
                  fg="white", bg="#111111")
header.pack(pady=(15, 5))

btn_frame = tk.Frame(root, bg="#111111")
btn_frame.pack(pady=10)

btn_search = tk.Button(btn_frame, text="🔍 Buscar e Atualizar", command=show_profiles,
    bg="white", fg="black", font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
btn_search.pack(side="left", padx=10)

btn_reset = tk.Button(btn_frame, text="🧹 Resetar UI", command=reset_ui,
    bg="#ffffff", fg="#000000", font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
btn_reset.pack(side="left", padx=10)

columns = [
    "SSID", "Senha (ASCII)", "Senha (HEX)", "Adaptador", "GUID Adaptador",
    "Autenticação", "Criptografia", "Tipo de Conexão", "Modificado em", "Caminho do Perfil"
]

tree_frame = tk.Frame(root, bg="#111111")
tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=160, anchor="w")

scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)

tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
tree.grid(row=0, column=0, sticky="nsew")
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")

tree.bind("<Double-1>", copy_cell)

tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

profile_data = []
root.mainloop()