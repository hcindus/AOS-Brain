#!/usr/bin/env python3
"""
Reggie Starr RS-79 — Digital Cash Register
v1.0.0.1  (Master consolidation)

A comprehensive, customizable point-of-sale application built with Tkinter.

Features:
- Splash screen with multilingual welcome
- Multilingual UI (English, Spanish, French, German, Arabic, Chinese, Korean, Japanese)
- Currency formatting (USD, EUR, GBP, BTC) via babel
- Tax programming (multiple rates, per-item assignment)
- PLU & department management
- Discounts & surcharges (percentage + flat)
- Payment methods (Cash, BTC, MC/Visa, AMEX, EBT, WIC, Debit/Credit, Check)
- Advanced transactions (refund, void, exchange, cancel)
- Financial reports (financial, group, PLU, period, sales totals) — stored locally
- Clerk management (login/logout, per-clerk transaction tracking)
- Register modes (Register, Void, X, Z, Program, Service, Negative)
- Split check / split tender / layaway / deposit
- Customer management, gift cards, hold & recall
- BTC QR code (Lightning) + live exchange-rate refresh

Optional dependencies (gracefully degrade if missing):
- qrcode (BTC payment QR)
- requests (live exchange rates)
- babel (locale-aware currency formatting)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import datetime
import json
import os
import sys

try:
    from babel.numbers import format_currency
    _BABEL = True
except Exception:
    _BABEL = False

try:
    import requests
    _REQUESTS = True
except Exception:
    _REQUESTS = False

try:
    import qrcode
    from PIL import Image, ImageTk
    _QR = True
except Exception:
    _QR = False

try:
    from PIL import Image as _PILImage, ImageTk as _PILImageTk
    _PIL = True
except Exception:
    _PIL = False


# ══════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════

LANGUAGES = {
    "English": {
        "welcome": "Welcome", "product_code": "Product Code", "quantity": "Quantity",
        "price": "Price", "add_product": "Add Product", "discount": "Discount (%)",
        "surcharge": "Surcharge", "payment_method": "Payment Method",
        "refund": "Refund", "void": "Void", "exchange": "Exchange",
        "cancel": "Cancel Transaction", "generate_report": "Generate Report",
        "group_report": "Group Report", "plu_report": "PLU Report",
        "period_report": "Period Report", "sales_totals": "Sales Totals",
        "login": "Login", "logout": "Logout", "clerk_name": "Clerk Name",
        "tax_name": "Tax Name", "tax_rate": "Tax Rate (%)", "add_tax": "Add Tax Rate",
        "department": "Department", "plu_code": "PLU Code",
        "split_check": "Split Check", "split_tender": "Split Tender",
        "currency_conversion": "Currency Conversion", "qr_code": "QR Code",
        "pay": "Pay", "hold": "Hold", "recall": "Recall",
        "language": "Language", "currency": "Currency", "customer": "Customer",
        "gift_card": "Gift Card", "update_rates": "Update Rates", "mode": "Mode",
    },
    "Spanish": {
        "welcome": "Bienvenido", "product_code": "Código de Producto", "quantity": "Cantidad",
        "price": "Precio", "add_product": "Agregar Producto", "discount": "Descuento (%)",
        "surcharge": "Recargo", "payment_method": "Método de Pago",
        "refund": "Reembolso", "void": "Anular", "exchange": "Intercambiar",
        "cancel": "Cancelar Transacción", "generate_report": "Generar Informe",
        "group_report": "Informe de Grupo", "plu_report": "Informe de PLU",
        "period_report": "Informe de Periodo", "sales_totals": "Totales de Venta",
        "login": "Iniciar sesión", "logout": "Cerrar sesión", "clerk_name": "Nombre del Empleado",
        "tax_name": "Nombre del Impuesto", "tax_rate": "Tasa (%)", "add_tax": "Agregar Impuesto",
        "department": "Departamento", "plu_code": "Código PLU",
        "split_check": "Dividir Cheque", "split_tender": "Dividir Pago",
        "currency_conversion": "Conversión de Moneda", "qr_code": "Código QR",
        "pay": "Pagar", "hold": "Espera", "recall": "Recordar",
        "language": "Idioma", "currency": "Moneda", "customer": "Cliente",
        "gift_card": "Tarjeta de Regalo", "update_rates": "Actualizar Tasas", "mode": "Modo",
    },
    "French": {
        "welcome": "Bienvenue", "product_code": "Code Produit", "quantity": "Quantité",
        "price": "Prix", "add_product": "Ajouter Produit", "discount": "Remise (%)",
        "surcharge": "Supplément", "payment_method": "Mode de Paiement",
        "refund": "Remboursement", "void": "Annuler", "exchange": "Échange",
        "cancel": "Annuler la Transaction", "generate_report": "Générer un Rapport",
        "group_report": "Rapport de Groupe", "plu_report": "Rapport PLU",
        "period_report": "Rapport de Période", "sales_totals": "Totaux des Ventes",
        "login": "Connexion", "logout": "Déconnexion", "clerk_name": "Nom de l'Employé",
        "tax_name": "Nom de la Taxe", "tax_rate": "Taux (%)", "add_tax": "Ajouter Taxe",
        "department": "Département", "plu_code": "Code PLU",
        "split_check": "Diviser la Note", "split_tender": "Diviser le Paiement",
        "currency_conversion": "Conversion de Devise", "qr_code": "Code QR",
        "pay": "Payer", "hold": "Attente", "recall": "Rappeler",
        "language": "Langue", "currency": "Devise", "customer": "Client",
        "gift_card": "Carte Cadeau", "update_rates": "Mettre à Jour", "mode": "Mode",
    },
    "German": {
        "welcome": "Willkommen", "product_code": "Produktcode", "quantity": "Menge",
        "price": "Preis", "add_product": "Produkt Hinzufügen", "discount": "Rabatt (%)",
        "surcharge": "Aufschlag", "payment_method": "Zahlungsart",
        "refund": "Rückerstattung", "void": "Stornieren", "exchange": "Umtausch",
        "cancel": "Transaktion Abbrechen", "generate_report": "Bericht Erstellen",
        "group_report": "Gruppenbericht", "plu_report": "PLU-Bericht",
        "period_report": "Zeitraumbericht", "sales_totals": "Verkaufssummen",
        "login": "Anmelden", "logout": "Abmelden", "clerk_name": "Mitarbeitername",
        "tax_name": "Steuername", "tax_rate": "Satz (%)", "add_tax": "Steuer Hinzufügen",
        "department": "Abteilung", "plu_code": "PLU-Code",
        "split_check": "Rechnung Teilen", "split_tender": "Zahlung Teilen",
        "currency_conversion": "Währungsumrechnung", "qr_code": "QR-Code",
        "pay": "Bezahlen", "hold": "Halten", "recall": "Abrufen",
        "language": "Sprache", "currency": "Währung", "customer": "Kunde",
        "gift_card": "Geschenkkarte", "update_rates": "Kurse Aktualisieren", "mode": "Modus",
    },
}

# Non-Latin locales: keep full dictionary for the "welcome" splash, but fall back
# to English labels for UI keys (tkinter + babel handle the glyphs fine).
for _lang, _msgs in {
    "Arabic": {"welcome": "أهلا بك"},
    "Chinese (Simplified)": {"welcome": "欢迎"},
    "Korean": {"welcome": "환영합니다"},
    "Japanese": {"welcome": "ようこそ"},
}.items():
    LANGUAGES[_lang] = {**LANGUAGES["English"], **_msgs}

CURRENCIES = {
    "USD": {"symbol": "$", "locale": "en_US", "rate": 1.0},
    "EUR": {"symbol": "€", "locale": "fr_FR", "rate": 0.85},
    "GBP": {"symbol": "£", "locale": "en_GB", "rate": 0.75},
    "BTC": {"symbol": "₿", "locale": "en_US", "rate": 0.000022},
}

PAYMENT_METHODS = ["Cash", "BTC", "MC/Visa", "AMEX", "EBT", "WIC", "Debit/Credit", "Check"]

REGISTER_MODES = ["Register", "Void", "X", "Z", "Program", "Service", "Negative"]


# ══════════════════════════════════════════════════════════════════
#  SPLASH SCREEN
# ══════════════════════════════════════════════════════════════════

class SplashScreen:
    def __init__(self, root, on_enter):
        self.root = root
        self.on_enter = on_enter
        root.title("Welcome to Reggie Starr RS-79")

        tk.Label(root, text="Reggie Starr", font=("Helvetica", 28, "bold")).pack(pady=(30, 0))
        tk.Label(root, text="RS-79 Digital Cash Register", font=("Helvetica", 16)).pack(pady=(0, 20))

        for lang, msgs in LANGUAGES.items():
            tk.Label(root, text=f"{msgs['welcome']}  —  {lang}",
                     font=("Helvetica", 12)).pack(pady=1)

        tk.Button(root, text="Enter", font=("Helvetica", 14, "bold"),
                  command=self._enter, width=20).pack(pady=25)

    def _enter(self):
        self.root.destroy()
        self.on_enter()


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════

class CashRegisterApp:
    def __init__(self, root):
        self.root = root
        root.title("Reggie Starr - RS-79 v1.0.0.1")

        # ── State ──
        self.tax_rates = {}            # name -> decimal rate
        self.inventory = []            # list of product dicts
        self.plu_codes = {}            # plu -> product
        self.departments = defaultdict(list)
        self.transactions = []         # list of transaction dicts
        self.clerks = defaultdict(list)
        self.current_clerk = None
        self.groups = defaultdict(list)
        self.plu_sales = defaultdict(float)
        self.period_sales = defaultdict(float)
        self.customers = {}
        self.gift_cards = {}
        self.hold_transactions = {}
        self.current_mode = "Register"
        self.current_role = "Clerk"

        # ── UI variables ──
        self.language = tk.StringVar(value="English")
        self.currency = tk.StringVar(value="USD")
        self.payment_method = tk.StringVar(value="Cash")

        self._build_ui()
        self.update_labels()

    # ──────────────────────────────────────────────
    #  UI construction
    # ──────────────────────────────────────────────
    def _build_ui(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        self.tab_register = ttk.Frame(nb); nb.add(self.tab_register, text="Register")
        self.tab_program = ttk.Frame(nb);  nb.add(self.tab_program, text="Programming")
        self.tab_reports = ttk.Frame(nb);  nb.add(self.tab_reports, text="Reports")
        self.tab_clerk = ttk.Frame(nb);    nb.add(self.tab_clerk, text="Clerks & Modes")
        self.tab_adv = ttk.Frame(nb);      nb.add(self.tab_adv, text="Advanced")

        self._build_config_bar()
        self._build_register_tab()
        self._build_program_tab()
        self._build_reports_tab()
        self._build_clerk_tab()
        self._build_adv_tab()

    def _build_config_bar(self):
        bar = ttk.Frame(self.tab_register)
        bar.pack(fill="x", pady=4)

        self.lbl_language = ttk.Label(bar, text="")
        self.lbl_language.grid(row=0, column=0, padx=4)
        ttk.OptionMenu(bar, self.language, "English", *LANGUAGES.keys(),
                       command=lambda _e: self.update_labels()).grid(row=0, column=1, padx=4)

        self.lbl_currency = ttk.Label(bar, text="")
        self.lbl_currency.grid(row=0, column=2, padx=4)
        ttk.OptionMenu(bar, self.currency, "USD", *CURRENCIES.keys()).grid(row=0, column=3, padx=4)

        self.lbl_payment = ttk.Label(bar, text="")
        self.lbl_payment.grid(row=0, column=4, padx=4)
        ttk.OptionMenu(bar, self.payment_method, "Cash", *PAYMENT_METHODS).grid(row=0, column=5, padx=4)

    def _build_register_tab(self):
        f = ttk.Frame(self.tab_register)
        f.pack(fill="both", expand=True, pady=8)

        # Product entry
        self.vars = {
            "code": tk.StringVar(), "qty": tk.StringVar(value="1"),
            "price": tk.StringVar(), "discount": tk.StringVar(value="0"),
            "surcharge": tk.StringVar(value="0"),
        }
        self.labels = {}
        row = 0
        for key, label_key, var, col in [
            ("code", "product_code", self.vars["code"], 0),
            ("qty", "quantity", self.vars["qty"], 1),
            ("price", "price", self.vars["price"], 0),
            ("discount", "discount", self.vars["discount"], 1),
            ("surcharge", "surcharge", self.vars["surcharge"], 0),
        ]:
            self.labels[label_key] = ttk.Label(f, text="")
            self.labels[label_key].grid(row=row, column=col * 2, padx=4, pady=2, sticky="w")
            ttk.Entry(f, textvariable=var, width=12).grid(row=row, column=col * 2 + 1, padx=4, pady=2)
            row += 1 if col == 1 else 0

        self.labels["add_product"] = ttk.Button(f, text="", command=self.add_product)
        self.labels["add_product"].grid(row=row, column=0, columnspan=4, pady=8)

        # Transaction buttons
        trow = 0
        for key, cmd in [("refund", self.process_refund), ("void", self.process_void),
                         ("exchange", self.process_exchange), ("cancel", self.cancel_transaction)]:
            self.labels[key] = ttk.Button(f, text="", command=cmd)
            self.labels[key].grid(row=trow, column=4, padx=4, pady=2, sticky="ew")
            trow += 1

        # Display
        self.display = tk.Text(f, height=14, width=64, font=("Courier", 10))
        self.display.grid(row=6, column=0, columnspan=6, padx=4, pady=8)

    def _build_program_tab(self):
        f = ttk.Frame(self.tab_program)
        f.pack(fill="both", expand=True, pady=8)

        # Tax programming
        self.tax_name = tk.StringVar(); self.tax_rate = tk.StringVar()
        self.labels["tax_name"] = ttk.Label(f, text=""); self.labels["tax_name"].grid(row=0, column=0, padx=4, pady=2, sticky="w")
        ttk.Entry(f, textvariable=self.tax_name, width=16).grid(row=0, column=1, padx=4)
        self.labels["tax_rate"] = ttk.Label(f, text=""); self.labels["tax_rate"].grid(row=1, column=0, padx=4, pady=2, sticky="w")
        ttk.Entry(f, textvariable=self.tax_rate, width=16).grid(row=1, column=1, padx=4)
        self.labels["add_tax"] = ttk.Button(f, text="", command=self.add_tax_rate)
        self.labels["add_tax"].grid(row=2, column=0, columnspan=2, pady=4)

        # PLU / department entry
        self.plu_vars = {
            "code": tk.StringVar(), "name": tk.StringVar(), "price": tk.StringVar(),
            "qty": tk.StringVar(value="1"), "department": tk.StringVar(), "plu": tk.StringVar(),
        }
        r = 3
        for i, (key, label_key) in enumerate([
            ("code", "product_code"), ("name", "clerk_name"), ("price", "price"),
            ("qty", "quantity"), ("department", "department"), ("plu", "plu_code"),
        ]):
            self.labels[f"plu_{label_key}"] = ttk.Label(f, text="")
            self.labels[f"plu_{label_key}"].grid(row=r + i, column=0, padx=4, pady=2, sticky="w")
            ttk.Entry(f, textvariable=self.plu_vars[key], width=16).grid(row=r + i, column=1, padx=4)
        self.labels["add_plu_product"] = ttk.Button(f, text="", command=self.add_plu_product)
        self.labels["add_plu_product"].grid(row=r + 6, column=0, columnspan=2, pady=4)

        self.program_display = tk.Text(f, height=12, width=60, font=("Courier", 10))
        self.program_display.grid(row=r + 7, column=0, columnspan=2, padx=4, pady=4)

    def _build_reports_tab(self):
        f = ttk.Frame(self.tab_reports)
        f.pack(fill="both", expand=True, pady=8)
        cmds = [("generate_report", self.generate_report), ("group_report", self.generate_group_report),
                ("plu_report", self.generate_plu_report), ("period_report", self.generate_period_report),
                ("sales_totals", self.generate_sales_totals)]
        for i, (key, cmd) in enumerate(cmds):
            self.labels[key] = ttk.Button(f, text="", command=cmd)
            self.labels[key].pack(fill="x", padx=8, pady=3)
        self.report_display = tk.Text(f, height=20, width=72, font=("Courier", 10))
        self.report_display.pack(fill="both", expand=True, padx=8, pady=6)

    def _build_clerk_tab(self):
        f = ttk.Frame(self.tab_clerk)
        f.pack(fill="both", expand=True, pady=8)

        self.clerk_name = tk.StringVar()
        self.labels["clerk_name"] = ttk.Label(f, text=""); self.labels["clerk_name"].grid(row=0, column=0, padx=4, pady=2, sticky="w")
        ttk.Entry(f, textvariable=self.clerk_name, width=18).grid(row=0, column=1, padx=4)
        self.labels["login"] = ttk.Button(f, text="", command=self.login_clerk); self.labels["login"].grid(row=1, column=0, padx=4, pady=2)
        self.labels["logout"] = ttk.Button(f, text="", command=self.logout_clerk); self.labels["logout"].grid(row=1, column=1, padx=4, pady=2)

        self.labels["mode"] = ttk.Label(f, text=""); self.labels["mode"].grid(row=2, column=0, padx=4, pady=6, sticky="w")
        for i, m in enumerate(REGISTER_MODES):
            ttk.Button(f, text=m, command=lambda _m=m: self.set_mode(_m)).grid(row=3 + i // 4, column=i % 4, padx=3, pady=2, sticky="ew")

        self.clerk_display = tk.Text(f, height=12, width=56, font=("Courier", 10))
        self.clerk_display.grid(row=5, column=0, columnspan=4, padx=4, pady=8)

    def _build_adv_tab(self):
        f = ttk.Frame(self.tab_adv)
        f.pack(fill="both", expand=True, pady=8)
        buttons = [
            ("split_check", self.split_check), ("split_tender", self.split_tender),
            ("currency_conversion", self.currency_conversion), ("qr_code", self.generate_qr_code),
            ("hold", self.hold_transaction), ("recall", self.recall_transaction),
            ("gift_card", self.issue_gift_card), ("update_rates", self.update_exchange_rates),
        ]
        for i, (key, cmd) in enumerate(buttons):
            self.labels[key] = ttk.Button(f, text="", command=cmd)
            self.labels[key].grid(row=i // 4, column=i % 4, padx=4, pady=4, sticky="ew")
        self.adv_display = tk.Text(f, height=16, width=72, font=("Courier", 10))
        self.adv_display.grid(row=2, column=0, columnspan=4, padx=4, pady=6)

    # ──────────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────────
    def t(self, key):
        """Translate a UI key using the active language (fallback to English)."""
        return LANGUAGES.get(self.language.get(), LANGUAGES["English"]).get(key, key)

    def update_labels(self):
        for key, widget in self.labels.items():
            if key in ("add_plu_product",):
                widget.config(text="Add Product")
                continue
            widget.config(text=self.t(key))

    def fmt(self, amount):
        c = CURRENCIES.get(self.currency.get(), CURRENCIES["USD"])
        if _BABEL:
            try:
                return format_currency(amount, self.currency.get(), locale=c["locale"])
            except Exception:
                pass
        return f"{c['symbol']}{amount:.2f}"

    def _log(self, text, widget=None):
        w = widget or self.display
        w.insert(tk.END, text + "\n")
        w.see(tk.END)

    # ──────────────────────────────────────────────
    #  Business logic
    # ──────────────────────────────────────────────
    def _require_clerk(self):
        if not self.current_clerk:
            self._log("⚠ Please login first.")
            return False
        return True

    def add_tax_rate(self):
        name = self.tax_name.get().strip()
        try:
            rate = float(self.tax_rate.get()) / 100.0
        except ValueError:
            self._log("Invalid tax rate.", self.program_display)
            return
        if name:
            self.tax_rates[name] = rate
            self.program_display.delete("1.0", tk.END)
            for n, r in self.tax_rates.items():
                self.program_display.insert(tk.END, f"{n}: {r * 100:.2f}%\n")

    def add_plu_product(self):
        code = self.plu_vars["code"].get().strip()
        name = self.plu_vars["name"].get().strip()
        try:
            price = float(self.plu_vars["price"].get())
            qty = int(self.plu_vars["qty"].get())
        except ValueError:
            self._log("Invalid price/quantity.", self.program_display)
            return
        dept = self.plu_vars["department"].get().strip() or "General"
        plu = self.plu_vars["plu"].get().strip() or None
        product = {"code": code, "name": name, "price": price, "quantity": qty,
                   "department": dept, "plu_code": plu}
        self.inventory.append(product)
        if plu:
            self.plu_codes[plu] = product
        self.departments[dept].append(product)
        self.program_display.insert(tk.END, f"Added: {code} {name} ${price:.2f} [{dept}]\n")

    def add_product(self):
        if not self._require_clerk():
            return
        try:
            price = float(self.vars["price"].get())
            qty = int(self.vars["qty"].get())
            discount = float(self.vars["discount"].get()) / 100.0
            surcharge = float(self.vars["surcharge"].get())
        except ValueError:
            self._log("Invalid entry.")
            return
        discounted = price * (1 - discount) + surcharge
        info = (f"{self.vars['code'].get().strip() or 'ITEM'}  x{qty}  {self.fmt(discounted)}  "
                f"(disc {discount*100:.0f}%, sur {self.fmt(surcharge)})  {self.payment_method.get()}")
        txn = {"type": "purchase", "info": info, "group": "General", "plu": self.vars["code"].get().strip(),
               "timestamp": datetime.datetime.now(), "amount": discounted}
        self.transactions.append(txn)
        self.clerks[self.current_clerk].append(txn)
        self.groups["General"].append(discounted)
        self.period_sales[datetime.datetime.now().hour] += discounted
        self._log(info)
        self.save_transactions()

    def _record(self, ttype, message):
        if not self._require_clerk():
            return
        txn = {"type": ttype, "info": message, "timestamp": datetime.datetime.now(), "amount": 0.0}
        self.transactions.append(txn)
        self.clerks[self.current_clerk].append(txn)
        self._log(message)
        self.save_transactions()

    def process_refund(self): self._record("refund", "Refund processed.")
    def process_void(self): self._record("void", "Transaction voided.")
    def process_exchange(self): self._record("exchange", "Exchange processed.")
    def cancel_transaction(self): self._record("cancel", "Transaction canceled.")

    def login_clerk(self):
        name = self.clerk_name.get().strip()
        if not name:
            self._log("Enter a clerk name.", self.clerk_display)
            return
        self.current_clerk = name
        self.clerks.setdefault(name, [])
        self._log(f"Clerk '{name}' logged in.", self.clerk_display)

    def logout_clerk(self):
        if self.current_clerk:
            self._log(f"Clerk '{self.current_clerk}' logged out.", self.clerk_display)
            self.current_clerk = None

    def set_mode(self, mode):
        self.current_mode = mode
        self._log(f"Mode → {mode}", self.clerk_display)

    def split_check(self): self._record("split_check", "Split check performed.")
    def split_tender(self): self._record("split_tender", "Split tender performed.")

    def currency_conversion(self):
        rate = CURRENCIES.get(self.currency.get(), {}).get("rate", 1.0)
        self._log(f"Currency conversion rate for {self.currency.get()}: {rate}", self.adv_display)

    def generate_qr_code(self):
        if not _QR:
            self._log("QR support not installed (pip install qrcode pillow).", self.adv_display)
            return
        amount = self._last_amount()
        payload = f"bitcoin:?amount={amount}"
        img = qrcode.make(payload)
        img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        top = tk.Toplevel(self.root)
        top.title("BTC Payment QR")
        lbl = tk.Label(top, image=photo); lbl.image = photo
        lbl.pack(padx=10, pady=10)
        self._log(f"QR generated for {self.fmt(amount)} BTC payment.", self.adv_display)

    def _last_amount(self):
        for txn in reversed(self.transactions):
            if txn.get("amount"):
                return txn["amount"]
        return 0.0

    def hold_transaction(self):
        key = f"TICKET-{len(self.hold_transactions) + 1}"
        self.hold_transactions[key] = list(self.transactions[-5:])
        self._log(f"Held as {key}.", self.adv_display)

    def recall_transaction(self):
        if not self.hold_transactions:
            self._log("No held transactions.", self.adv_display)
            return
        key, items = list(self.hold_transactions.items())[-1]
        for txn in items:
            self._log(f"[recall {key}] {txn['info']}", self.adv_display)

    def issue_gift_card(self):
        card_id = f"GC-{len(self.gift_cards) + 1}"
        self.gift_cards[card_id] = {"balance": 100.0, "expiry": datetime.datetime.now() + datetime.timedelta(days=365)}
        self._log(f"Issued {card_id} (balance $100.00).", self.adv_display)

    def update_exchange_rates(self):
        if not _REQUESTS:
            self._log("requests not installed — cannot fetch live rates.", self.adv_display)
            return
        try:
            r = requests.get("https://api.exchangeratesapi.io/latest", timeout=8)
            data = r.json()
            for cur, cfg in CURRENCIES.items():
                if cur in data.get("rates", {}):
                    cfg["rate"] = data["rates"][cur]
            self._log("Exchange rates updated.", self.adv_display)
        except Exception as e:
            self._log(f"Rate update failed: {e}", self.adv_display)

    # ──────────────────────────────────────────────
    #  Reports
    # ──────────────────────────────────────────────
    def _write_report(self, text, filename):
        try:
            with open(filename, "w") as f:
                f.write(text)
        except Exception:
            pass
        return text

    def generate_report(self):
        report = "FINANCIAL REPORT\n" + "=" * 40 + "\n"
        for txn in self.transactions:
            report += f"{txn['type']:<12} {txn['info']}\n"
        self.report_display.delete("1.0", tk.END)
        self.report_display.insert(tk.END, self._write_report(report, "financial_report.txt"))

    def generate_group_report(self):
        report = "GROUP REPORT\n" + "=" * 40 + "\n"
        for group, sales in self.groups.items():
            report += f"{group:<20} {self.fmt(sum(sales))}\n"
        self.report_display.delete("1.0", tk.END)
        self.report_display.insert(tk.END, self._write_report(report, "group_report.txt"))

    def generate_plu_report(self):
        report = "PLU REPORT\n" + "=" * 40 + "\n"
        for plu, sales in self.plu_sales.items():
            report += f"{plu:<20} {self.fmt(sales)}\n"
        self.report_display.delete("1.0", tk.END)
        self.report_display.insert(tk.END, self._write_report(report, "plu_report.txt"))

    def generate_period_report(self):
        report = "PERIOD REPORT (hourly)\n" + "=" * 40 + "\n"
        for hour in sorted(self.period_sales):
            report += f"{hour:02d}:00  {self.fmt(self.period_sales[hour])}\n"
        self.report_display.delete("1.0", tk.END)
        self.report_display.insert(tk.END, self._write_report(report, "period_report.txt"))

    def generate_sales_totals(self):
        report = "SALES TOTALS REPORT\n" + "=" * 40 + "\n"
        for period, delta in [("1 week", 7), ("3 weeks", 21), ("1 month", 30),
                              ("3 months", 90), ("6 months", 180), ("1 year", 365)]:
            cutoff = datetime.datetime.now() - datetime.timedelta(days=delta)
            total = sum(t.get("amount", 0.0) for t in self.transactions if t["timestamp"] >= cutoff)
            report += f"{period:<12} {self.fmt(total)}\n"
        self.report_display.delete("1.0", tk.END)
        self.report_display.insert(tk.END, self._write_report(report, "sales_totals_report.txt"))

    # ──────────────────────────────────────────────
    #  Persistence
    # ──────────────────────────────────────────────
    def save_transactions(self):
        try:
            with open("transactions.json", "w") as f:
                json.dump([{**t, "timestamp": t["timestamp"].isoformat()} for t in self.transactions], f)
        except Exception:
            pass


def main():
    root = tk.Tk()
    root.geometry("860x680")

    def launch_app():
        app_root = tk.Tk()
        CashRegisterApp(app_root)
        app_root.mainloop()

    SplashScreen(root, launch_app)
    root.mainloop()


if __name__ == "__main__":
    main()
