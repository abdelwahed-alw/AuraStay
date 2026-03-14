"""
╔══════════════════════════════════════════════════════════╗
║     MAISON D'HÔTE  –  Guest House Management App        ║
║     Python 3 · tkinter / ttk · SQLite3                  ║
║     🇫🇷 Français  /  🇬🇧 English  ·  Full CRUD           ║
╚══════════════════════════════════════════════════════════╝
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date

# ═══════════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════════
LANG = {
  "fr": dict(
    app_title="🏡 Maison d'Hôte",
    nav_dashboard="Tableau de bord", nav_reservations="Réservations",
    nav_rooms="Chambres", nav_clients="Clients", nav_new="Nouvelle résa.",
    nav_icons=["�","","🛏","👥","➕"],
    dashboard_title="Tableau de bord", kpi_clients="Total Clients",
    kpi_active="Réservations actives", kpi_rooms="Chambres disponibles",
    kpi_revenue="Revenus totaux", recent_title="Réservations récentes",
    rooms_title="Chambres", resa_title="Réservations",
    clients_title="Clients", new_title="Nouvelle réservation",
    col_client="Client", col_room="Chambre", col_start="Début",
    col_end="Fin", col_status="Statut", col_amount="Montant",
    col_lastname="Nom", col_firstname="Prénom", col_phone="Téléphone",
    col_actions="Actions",
    lbl_lastname="Nom du client", lbl_firstname="Prénom",
    lbl_phone="Téléphone", lbl_room="Chambre (disponible)",
    lbl_checkin="Date d'arrivée  (AAAA-MM-JJ)",
    lbl_checkout="Date de départ  (AAAA-MM-JJ)",
    btn_save="Enregistrer", btn_edit="Modifier", btn_delete="Supprimer",
    btn_cancel="Annuler",
    err_fill="Veuillez remplir tous les champs obligatoires.",
    err_date="Dates invalides. Format : AAAA-MM-JJ, fin > début.",
    ok_saved="Réservation enregistrée !  {n} nuit(s)  ·  {m} €",
    ok_updated="Modification enregistrée !", ok_deleted="Supprimé !",
    confirm_delete="Êtes-vous sûr(e) de vouloir supprimer cet élément ?",
    confirm_title="Confirmation",
    err_room_busy="Impossible : chambre liée à une réservation active.",
    err_client_busy="Impossible : client lié à une réservation.",
    available="Disponible", occupied="Occupée",
    status_active="En cours", status_done="Terminée", status_cancelled="Annulée",
    type_lbl="Type", capacity_lbl="Capacité", per_night="/nuit",
    lang_switch="🇬🇧  English", search_ph="Rechercher un nom…",
    edit_client="Modifier le client", edit_room="Modifier la chambre",
    edit_resa="Modifier la réservation",
    lbl_name="Nom", lbl_type="Type", lbl_capacity="Capacité",
    lbl_price="Prix / nuit (€)", lbl_status="Statut", pers="pers.",
  ),
  "en": dict(
    app_title="🏡 Guest House",
    nav_dashboard="Dashboard", nav_reservations="Reservations",
    nav_rooms="Rooms", nav_clients="Clients", nav_new="New Booking",
    nav_icons=["📊","📅","🛏","👥","➕"],
    dashboard_title="Dashboard", kpi_clients="Total Clients",
    kpi_active="Active Bookings", kpi_rooms="Available Rooms",
    kpi_revenue="Total Revenue", recent_title="Recent Bookings",
    rooms_title="Rooms", resa_title="Reservations",
    clients_title="Clients", new_title="New Booking",
    col_client="Client", col_room="Room", col_start="Check-in",
    col_end="Check-out", col_status="Status", col_amount="Amount",
    col_lastname="Last Name", col_firstname="First Name", col_phone="Phone",
    col_actions="Actions",
    lbl_lastname="Last Name", lbl_firstname="First Name",
    lbl_phone="Phone", lbl_room="Room (available)",
    lbl_checkin="Check-in  (YYYY-MM-DD)",
    lbl_checkout="Check-out  (YYYY-MM-DD)",
    btn_save="Save", btn_edit="Edit", btn_delete="Delete",
    btn_cancel="Cancel",
    err_fill="Please fill in all required fields.",
    err_date="Invalid dates. Format: YYYY-MM-DD, end > start.",
    ok_saved="Booking saved!  {n} night(s)  ·  {m} €",
    ok_updated="Changes saved!", ok_deleted="Deleted!",
    confirm_delete="Are you sure you want to delete this item?",
    confirm_title="Confirm",
    err_room_busy="Cannot delete: room linked to an active booking.",
    err_client_busy="Cannot delete: client has reservations.",
    available="Available", occupied="Occupied",
    status_active="En cours", status_done="Terminée", status_cancelled="Annulée",
    type_lbl="Type", capacity_lbl="Capacity", per_night="/night",
    lang_switch="🇫🇷  Français", search_ph="Search by name…",
    edit_client="Edit Client", edit_room="Edit Room",
    edit_resa="Edit Reservation",
    lbl_name="Name", lbl_type="Type", lbl_capacity="Capacity",
    lbl_price="Price / night (€)", lbl_status="Status", pers="pers.",
  ),
}

# ═══════════════════════════════════════════════════════════
# COLOUR PALETTE  (refined dark theme)
# ═══════════════════════════════════════════════════════════
C = dict(
    # backgrounds
    bg       = "#0F1923",
    sidebar  = "#141E2B",
    sidebar_h= "#1A2A3B",
    topbar   = "#182635",
    card     = "#182635",
    card2    = "#1D2F42",
    # accents
    accent   = "#FF4C6E",
    green    = "#34D399",
    orange   = "#FB923C",
    blue     = "#60A5FA",
    purple   = "#A78BFA",
    yellow   = "#FBBF24",
    cyan     = "#22D3EE",
    # text
    white    = "#F1F5F9",
    sub      = "#94A3B8",
    muted    = "#64748B",
    # borders
    border   = "#293B50",
    divider  = "#1E3044",
    # inputs
    entry_bg = "#0F1923",
    # buttons
    btn_edit = "#059669",
    btn_edit_h= "#047857",
    btn_del  = "#DC2626",
    btn_del_h= "#B91C1C",
    btn_save = "#2563EB",
    btn_save_h="#1D4ED8",
    hover    = "#E11D48",
    # table
    row_alt  = "#152231",
    row_sel  = "#1E3A5F",
)

PAD = 32       # main content padding
GAP = 12       # between cards
RAD = 10       # corner radius (conceptual)

# ═══════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════
DB = "maison_hote.db"
def cn():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init_db():
    with cn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS chambres (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL, type TEXT NOT NULL, capacite INTEGER NOT NULL,
                prix_nuit REAL NOT NULL, statut TEXT NOT NULL DEFAULT 'Disponible');
            CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL, prenom TEXT NOT NULL, telephone TEXT);
            CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL REFERENCES clients(id),
                chambre_id INTEGER NOT NULL REFERENCES chambres(id),
                date_debut TEXT NOT NULL, date_fin TEXT NOT NULL,
                statut TEXT NOT NULL DEFAULT 'En cours', montant REAL NOT NULL);
        """)
        if c.execute("SELECT COUNT(*) FROM chambres").fetchone()[0] == 0:
            c.executemany("INSERT INTO chambres (nom,type,capacite,prix_nuit,statut) VALUES (?,?,?,?,?)",
                [("Chambre Lavande","Simple",1,200.0,"Disponible"),
                 ("Chambre Rose","Double",2,350.0,"Disponible"),
                 ("Suite Jasmin","Suite",4,500.0,"Disponible"),
                 ("Chambre Olive","Simple",1,150.0,"Occupée"),
                 ("Chambre Myrte","Double",2,250.0,"Disponible")])
        if c.execute("SELECT COUNT(*) FROM clients").fetchone()[0] == 0:
            c.execute("INSERT INTO clients (nom,prenom,telephone) VALUES ('Benali','Yasmine','0555 12 34 56')")
            c.execute("INSERT INTO clients (nom,prenom,telephone) VALUES ('Amrani','Karim','0661 98 76 54')")
            c.execute("INSERT INTO reservations (client_id,chambre_id,date_debut,date_fin,statut,montant) VALUES (1,2,'2024-03-01','2024-03-05','Terminée',1400)")
            c.execute("INSERT INTO reservations (client_id,chambre_id,date_debut,date_fin,statut,montant) VALUES (2,4,'2024-03-10','2024-03-12','En cours',300)")


# ═══════════════════════════════════════════════════════════
# REUSABLE WIDGETS
# ═══════════════════════════════════════════════════════════

def make_entry(parent, var=None, placeholder="", width=None):
    """Styled entry with placeholder behaviour."""
    kw = {}
    if width: kw["width"] = width
    e = tk.Entry(parent, bg=C["entry_bg"], fg=C["white"],
                 insertbackground=C["white"], font=("Segoe UI", 11),
                 relief="flat", bd=0, highlightthickness=2,
                 highlightbackground=C["border"], highlightcolor=C["blue"],
                 textvariable=var, **kw)
    if placeholder and not (var and var.get()):
        e.insert(0, placeholder)
        e.config(fg=C["muted"])
        def _in(ev):
            if e.get() == placeholder:
                e.delete(0, "end"); e.config(fg=C["white"])
        def _out(ev):
            if not e.get().strip():
                e.insert(0, placeholder); e.config(fg=C["muted"])
        e.bind("<FocusIn>", _in); e.bind("<FocusOut>", _out)
    return e


def make_btn(parent, text, cmd, bg_c=None, fg_c="white", icon="", size=9, pad_x=12, pad_y=5):
    bg = bg_c or C["accent"]
    hover_map = {
        C["accent"]: C["hover"], C["btn_edit"]: C["btn_edit_h"],
        C["btn_del"]: C["btn_del_h"], C["btn_save"]: C["btn_save_h"],
        C["border"]: C["muted"],
    }
    hv = hover_map.get(bg, C["hover"])
    full = f"{icon}  {text}" if icon else text
    b = tk.Button(parent, text=full, command=cmd, bg=bg, fg=fg_c,
                  font=("Segoe UI", size, "bold"), bd=0, padx=pad_x, pady=pad_y,
                  cursor="hand2", relief="flat", activebackground=hv,
                  activeforeground="white")
    b.bind("<Enter>", lambda e, b=b, h=hv: b.config(bg=h))
    b.bind("<Leave>", lambda e, b=b, o=bg: b.config(bg=o))
    return b


# ═══════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "fr"; self.t = LANG["fr"]
        self.title(self.t["app_title"])
        self.geometry("1220x760"); self.minsize(1040, 660)
        self.configure(bg=C["bg"])
        self._page = "dashboard"
        init_db()
        self._ttk_styles()
        self._build()
        self.show_dashboard()

    # ── TTK STYLES ─────────────────────────────────
    def _ttk_styles(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("T.Treeview", background=C["card"], fieldbackground=C["card"],
                     foreground=C["white"], rowheight=38, font=("Segoe UI", 10), borderwidth=0)
        s.configure("T.Treeview.Heading", background=C["topbar"], foreground=C["blue"],
                     font=("Segoe UI", 10, "bold"), relief="flat", borderwidth=0, padding=6)
        s.map("T.Treeview", background=[("selected", C["row_sel"])],
              foreground=[("selected", C["white"])])
        s.configure("TCombobox", fieldbackground=C["entry_bg"], background=C["border"],
                     foreground=C["white"], borderwidth=1, arrowcolor=C["blue"],
                     padding=6)
        s.map("TCombobox", fieldbackground=[("readonly", C["entry_bg"])])
        s.configure("Vertical.TScrollbar", background=C["border"], troughcolor=C["bg"],
                     bordercolor=C["bg"], arrowcolor=C["sub"])

    # ── BUILD LAYOUT ───────────────────────────────
    def _build(self):
        # -------- SIDEBAR --------
        self.sidebar = tk.Frame(self, bg=C["sidebar"], width=240)
        self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Frame(self.sidebar, bg=C["sidebar"], pady=28)
        logo.pack(fill="x")
        self._logo = tk.Label(logo, text="🏡", bg=C["sidebar"], font=("Segoe UI Emoji", 28))
        self._logo.pack()
        self._logo2 = tk.Label(logo, text="Maison d'Hôte", bg=C["sidebar"],
                               fg=C["white"], font=("Segoe UI", 14, "bold"))
        self._logo2.pack(pady=(4, 0))
        self._logo3 = tk.Label(logo, text="━━━━━━━━━━━━━━━━", bg=C["sidebar"],
                               fg=C["border"], font=("Segoe UI", 8))
        self._logo3.pack(pady=(8, 0))

        # Nav
        nav_f = tk.Frame(self.sidebar, bg=C["sidebar"])
        nav_f.pack(fill="x", pady=(12, 0))

        keys  = ["nav_dashboard","nav_reservations","nav_rooms","nav_clients","nav_new"]
        cmds  = [self.show_dashboard, self.show_reservations, self.show_rooms,
                 self.show_clients, self.show_new_reservation]
        pages = ["dashboard","reservations","rooms","clients","new"]
        self._nav = []; self._nav_ind = []; self._nav_pg = pages
        self._nav_cmd = cmds; self._nav_key = keys

        for i, (k, cmd, pg) in enumerate(zip(keys, cmds, pages)):
            row = tk.Frame(nav_f, bg=C["sidebar"], pady=1)
            row.pack(fill="x")
            # left accent indicator
            ind = tk.Frame(row, bg=C["sidebar"], width=3)
            ind.pack(side="left", fill="y"); self._nav_ind.append(ind)
            # button
            ic = self.t["nav_icons"][i]
            b = tk.Label(row, text=f"   {ic}    {self.t[k]}",
                         bg=C["sidebar"], fg=C["sub"],
                         font=("Segoe UI", 11), anchor="w",
                         padx=12, pady=12, cursor="hand2")
            b.pack(fill="x", side="left", expand=True)
            b.bind("<Button-1>", lambda e, c=cmd: c())
            b.bind("<Enter>", lambda e, b=b: b.config(bg=C["sidebar_h"]))
            b.bind("<Leave>", lambda e, b=b, p=pg:
                   b.config(bg=C["sidebar_h"] if self._page == p else C["sidebar"]))
            self._nav.append(b)

        # Language toggle at bottom
        tk.Frame(self.sidebar, bg=C["sidebar"]).pack(fill="both", expand=True)
        tk.Frame(self.sidebar, bg=C["divider"], height=1).pack(fill="x", padx=20)
        self._lang_b = tk.Label(self.sidebar, text=self.t["lang_switch"],
                                bg=C["sidebar"], fg=C["muted"],
                                font=("Segoe UI", 10), cursor="hand2", pady=16)
        self._lang_b.pack(fill="x", side="bottom")
        self._lang_b.bind("<Button-1>", lambda e: self._toggle_lang())
        self._lang_b.bind("<Enter>", lambda e: self._lang_b.config(fg=C["white"]))
        self._lang_b.bind("<Leave>", lambda e: self._lang_b.config(fg=C["muted"]))

        # -------- MAIN AREA --------
        wrapper = tk.Frame(self, bg=C["bg"])
        wrapper.pack(side="left", fill="both", expand=True)

        self._canvas = tk.Canvas(wrapper, bg=C["bg"], bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=self._canvas.yview,
                            style="Vertical.TScrollbar")
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y"); self._canvas.pack(fill="both", expand=True)

        self.main = tk.Frame(self._canvas, bg=C["bg"])
        self._cw = self._canvas.create_window((0, 0), window=self.main, anchor="nw")
        self.main.bind("<Configure>",
                       lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
                          lambda e: self._canvas.itemconfig(self._cw, width=e.width))
        # scrolling
        self._canvas.bind_all("<Button-4>",  lambda e: self._canvas.yview_scroll(-3, "units"))
        self._canvas.bind_all("<Button-5>",  lambda e: self._canvas.yview_scroll(3, "units"))
        self._canvas.bind_all("<MouseWheel>",
                              lambda e: self._canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ── NAV HIGHLIGHT ──────────────────────────────
    def _set_page(self, pg):
        self._page = pg
        for i, p in enumerate(self._nav_pg):
            active = p == pg
            self._nav[i].config(bg=C["sidebar_h"] if active else C["sidebar"],
                                fg=C["white"] if active else C["sub"],
                                font=("Segoe UI", 11, "bold") if active else ("Segoe UI", 11))
            self._nav_ind[i].config(bg=C["accent"] if active else C["sidebar"])

    # ── LANGUAGE ───────────────────────────────────
    def _toggle_lang(self):
        self.lang = "en" if self.lang == "fr" else "fr"
        self.t = LANG[self.lang]; self.title(self.t["app_title"])
        name = "Maison d'Hôte" if self.lang == "fr" else "Guest House"
        self._logo2.config(text=name)
        self._lang_b.config(text=self.t["lang_switch"])
        for i, k in enumerate(self._nav_key):
            ic = self.t["nav_icons"][i]
            self._nav[i].config(text=f"   {ic}    {self.t[k]}")
        refresh = {"dashboard": self.show_dashboard, "reservations": self.show_reservations,
                   "rooms": self.show_rooms, "clients": self.show_clients,
                   "new": self.show_new_reservation}
        refresh.get(self._page, self.show_dashboard)()

    # ── HELPERS ────────────────────────────────────
    def _clear(self):
        for w in self.main.winfo_children(): w.destroy()
        self._canvas.yview_moveto(0)

    def _header(self, icon, title):
        bar = tk.Frame(self.main, bg=C["topbar"], pady=18)
        bar.pack(fill="x")
        tk.Label(bar, text=f"  {icon}   {title}", bg=C["topbar"], fg=C["white"],
                 font=("Segoe UI", 17, "bold")).pack(side="left", padx=PAD)

    def _card_frame(self, parent, **kw):
        f = tk.Frame(parent, bg=C["card"], highlightthickness=1,
                     highlightbackground=C["border"], **kw)
        return f

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, bg=C["bg"], fg=C["sub"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PAD, pady=(18, 8))

    # ── POPUP DIALOG ───────────────────────────────
    def _popup(self, title, fields, vals, on_save):
        top = tk.Toplevel(self); top.title(title)
        top.configure(bg=C["card"]); top.resizable(False, False)
        top.transient(self); top.grab_set()

        # center on parent
        w, h = 440, 80 + len(fields) * 68
        top.geometry(f"{w}x{h}+{self.winfo_x()+380}+{self.winfo_y()+120}")

        # title bar
        tk.Frame(top, bg=C["accent"], height=3).pack(fill="x")
        tk.Label(top, text=f"  {title}", bg=C["card"], fg=C["white"],
                 font=("Segoe UI", 13, "bold"), anchor="w", pady=12).pack(fill="x", padx=20)
        tk.Frame(top, bg=C["divider"], height=1).pack(fill="x", padx=20)

        inner = tk.Frame(top, bg=C["card"], padx=24, pady=8)
        inner.pack(fill="both", expand=True)

        widgets = {}
        for key, ftype, opts in fields:
            tk.Label(inner, text=self.t.get(key, key), bg=C["card"], fg=C["sub"],
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 3))
            if ftype == "entry":
                var = tk.StringVar(value=vals.get(key, ""))
                make_entry(inner, var).pack(fill="x", ipady=7)
                widgets[key] = var
            elif ftype == "combo":
                var = tk.StringVar(value=vals.get(key, ""))
                ttk.Combobox(inner, textvariable=var, values=opts, state="readonly",
                             font=("Segoe UI", 11)).pack(fill="x", ipady=4)
                widgets[key] = var

        msg = tk.Label(inner, text="", bg=C["card"], font=("Segoe UI", 10, "bold"))
        msg.pack(pady=(8, 0))

        bf = tk.Frame(inner, bg=C["card"]); bf.pack(fill="x", pady=(12, 8))
        def do_save():
            res = {k: v.get() for k, v in widgets.items()}
            err = on_save(res)
            if err:
                msg.config(text=f"⚠  {err}", fg=C["accent"])
            else:
                msg.config(text=f"✅  {self.t['ok_updated']}", fg=C["green"])
                top.after(500, top.destroy)
        make_btn(bf, self.t["btn_save"], do_save, C["btn_save"], icon="💾", size=10, pad_x=16, pad_y=7).pack(side="left", padx=(0, 8))
        make_btn(bf, self.t["btn_cancel"], top.destroy, C["border"], size=10, pad_x=16, pad_y=7).pack(side="left")

    # ══════════════════════════════════════════════════
    #  📊  DASHBOARD
    # ══════════════════════════════════════════════════
    def show_dashboard(self):
        self._clear(); self._set_page("dashboard")
        t = self.t; self._header("📊", t["dashboard_title"])

        with cn() as c:
            nc = c.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
            na = c.execute("SELECT COUNT(*) FROM reservations WHERE statut='En cours'").fetchone()[0]
            nr = c.execute("SELECT COUNT(*) FROM chambres WHERE statut='Disponible'").fetchone()[0]
            rv = c.execute("SELECT COALESCE(SUM(montant),0) FROM reservations").fetchone()[0]
            recent = c.execute("""SELECT c.nom||' '||c.prenom, ch.nom,
                r.date_debut, r.date_fin, r.statut, r.montant
                FROM reservations r JOIN clients c ON c.id=r.client_id
                JOIN chambres ch ON ch.id=r.chambre_id ORDER BY r.id DESC LIMIT 8""").fetchall()

        # KPI row
        kf = tk.Frame(self.main, bg=C["bg"]); kf.pack(fill="x", padx=PAD, pady=(20, 0))
        kpis = [
            (t["kpi_clients"], str(nc),        "👤", C["blue"],   C["blue"]),
            (t["kpi_active"],  str(na),         "📅", C["green"],  C["green"]),
            (t["kpi_rooms"],   str(nr),         "🔑", C["purple"], C["purple"]),
            (t["kpi_revenue"], f"{rv:,.0f} €",  "💰", C["orange"], C["orange"]),
        ]
        for col, (label, val, icon, clr, _) in enumerate(kpis):
            kf.columnconfigure(col, weight=1)
            card = self._card_frame(kf)
            card.grid(row=0, column=col, padx=GAP//2, sticky="nsew")
            # top accent line
            tk.Frame(card, bg=clr, height=3).pack(fill="x")
            body = tk.Frame(card, bg=C["card"], padx=20, pady=18); body.pack(fill="both")
            # icon + value row
            row = tk.Frame(body, bg=C["card"]); row.pack(fill="x")
            tk.Label(row, text=icon, bg=C["card"], font=("Segoe UI Emoji", 22)).pack(side="left")
            tk.Label(row, text=val, bg=C["card"], fg=clr,
                     font=("Segoe UI", 26, "bold")).pack(side="right")
            tk.Label(body, text=label, bg=C["card"], fg=C["sub"],
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 0))

        # Recent reservations
        self._section_label(self.main, f"📋  {t['recent_title']}")
        self._tree(self.main,
                   [t["col_client"], t["col_room"], t["col_start"],
                    t["col_end"], t["col_status"], t["col_amount"]],
                   [list(r) for r in recent])

    # ══════════════════════════════════════════════════
    #  🛏  ROOMS
    # ══════════════════════════════════════════════════
    def show_rooms(self):
        self._clear(); self._set_page("rooms"); self._header("🛏", self.t["rooms_title"])
        t = self.t
        with cn() as c: rooms = c.execute("SELECT * FROM chambres ORDER BY id").fetchall()

        grid = tk.Frame(self.main, bg=C["bg"]); grid.pack(fill="x", padx=PAD, pady=(16, 20))
        icons = {"Simple": "🛏", "Double": "🛏🛏", "Suite": "🏨"}
        for i in range(3): grid.columnconfigure(i, weight=1)

        for idx, r in enumerate(rooms):
            rw, cl = divmod(idx, 3)
            ok = r["statut"] == "Disponible"
            ac = C["green"] if ok else C["accent"]
            st = t["available"] if ok else t["occupied"]

            card = self._card_frame(grid)
            card.grid(row=rw, column=cl, padx=GAP//2, pady=GAP//2, sticky="nsew")
            tk.Frame(card, bg=ac, height=3).pack(fill="x")
            body = tk.Frame(card, bg=C["card"], padx=20, pady=16); body.pack(fill="both")

            # name
            tk.Label(body, text=f"{icons.get(r['type'],'🛏')}  {r['nom']}", bg=C["card"],
                     fg=C["white"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
            # type + capacity
            info = tk.Frame(body, bg=C["card"]); info.pack(fill="x", pady=(8, 2))
            tk.Label(info, text=f"{t['type_lbl']}: {r['type']}", bg=C["card"], fg=C["sub"],
                     font=("Segoe UI", 10)).pack(side="left")
            tk.Label(info, text=f"{r['capacite']} {t['pers']}", bg=C["card"], fg=C["sub"],
                     font=("Segoe UI", 10)).pack(side="right")
            # price
            tk.Label(body, text=f"{r['prix_nuit']:.0f} €{t['per_night']}", bg=C["card"],
                     fg=C["orange"], font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(6, 6))
            # status badge
            badge_f = tk.Frame(body, bg=C["card"]); badge_f.pack(fill="x")
            badge = tk.Label(badge_f, text=f"  ● {st}  ", bg=ac, fg="white",
                             font=("Segoe UI", 9, "bold"), pady=2)
            badge.pack(side="left")
            # action buttons
            bf = tk.Frame(badge_f, bg=C["card"]); bf.pack(side="right")
            rid = r["id"]
            make_btn(bf, t["btn_edit"], lambda rid=rid: self._edit_room(rid),
                     C["btn_edit"], icon="✏", size=8, pad_x=6, pad_y=3).pack(side="left", padx=2)
            make_btn(bf, t["btn_delete"], lambda rid=rid: self._del_room(rid),
                     C["btn_del"], icon="🗑", size=8, pad_x=6, pad_y=3).pack(side="left")

    def _edit_room(self, rid):
        with cn() as c: r = c.execute("SELECT * FROM chambres WHERE id=?", (rid,)).fetchone()
        if not r: return
        fields = [("lbl_name","entry",None),("lbl_type","combo",["Simple","Double","Suite"]),
                  ("lbl_capacity","entry",None),("lbl_price","entry",None),
                  ("lbl_status","combo",["Disponible","Occupée"])]
        vals = {"lbl_name":r["nom"],"lbl_type":r["type"],"lbl_capacity":str(r["capacite"]),
                "lbl_price":str(r["prix_nuit"]),"lbl_status":r["statut"]}
        def save(d):
            if not all(d.values()): return self.t["err_fill"]
            try: cap=int(d["lbl_capacity"]); px=float(d["lbl_price"])
            except: return self.t["err_fill"]
            with cn() as c:
                c.execute("UPDATE chambres SET nom=?,type=?,capacite=?,prix_nuit=?,statut=? WHERE id=?",
                          (d["lbl_name"],d["lbl_type"],cap,px,d["lbl_status"],rid))
            self.after(600, self.show_rooms)
        self._popup(self.t["edit_room"], fields, vals, save)

    def _del_room(self, rid):
        with cn() as c:
            busy = c.execute("SELECT COUNT(*) FROM reservations WHERE chambre_id=? AND statut='En cours'",
                             (rid,)).fetchone()[0]
        if busy: messagebox.showwarning(self.t["confirm_title"], self.t["err_room_busy"]); return
        if not messagebox.askyesno(self.t["confirm_title"], self.t["confirm_delete"]): return
        with cn() as c: c.execute("DELETE FROM chambres WHERE id=?", (rid,))
        self.show_rooms()

    # ══════════════════════════════════════════════════
    #  👥  CLIENTS
    # ══════════════════════════════════════════════════
    def show_clients(self):
        self._clear(); self._set_page("clients"); self._header("👥", self.t["clients_title"])
        # search
        sf = tk.Frame(self.main, bg=C["bg"]); sf.pack(fill="x", padx=PAD, pady=(16, 0))
        self._cl_search_e = make_entry(sf, placeholder=self.t["search_ph"])
        self._cl_search_e.pack(fill="x", ipady=8)
        self._cl_search_e.bind("<KeyRelease>", lambda e: self._render_clients())
        self._cl_box = tk.Frame(self.main, bg=C["bg"])
        self._cl_box.pack(fill="both", expand=True)
        self._render_clients()

    def _render_clients(self):
        for w in self._cl_box.winfo_children(): w.destroy()
        t = self.t
        raw = self._cl_search_e.get()
        q = "" if raw == t["search_ph"] else raw
        like = f"%{q}%"
        with cn() as c:
            rows = c.execute("SELECT * FROM clients WHERE nom LIKE ? OR prenom LIKE ? OR telephone LIKE ? ORDER BY id DESC",
                             (like, like, like)).fetchall()

        card = self._card_frame(self._cl_box)
        card.pack(fill="both", expand=True, padx=PAD, pady=(12, 20))

        # header row
        hdr = tk.Frame(card, bg=C["topbar"]); hdr.pack(fill="x")
        for txt, w in [(t["col_lastname"],18),(t["col_firstname"],18),(t["col_phone"],18),(t["col_actions"],16)]:
            tk.Label(hdr, text=txt, bg=C["topbar"], fg=C["blue"],
                     font=("Segoe UI",10,"bold"), width=w, anchor="w", pady=10, padx=12).pack(side="left")

        for i, r in enumerate(rows):
            bg = C["row_alt"] if i % 2 else C["card"]
            row = tk.Frame(card, bg=bg); row.pack(fill="x")
            for val in [r["nom"], r["prenom"], r["telephone"] or "—"]:
                tk.Label(row, text=val, bg=bg, fg=C["white"], font=("Segoe UI",10),
                         width=18, anchor="w", padx=12, pady=8).pack(side="left")
            bf = tk.Frame(row, bg=bg, padx=8, pady=4); bf.pack(side="left")
            cid = r["id"]
            make_btn(bf, t["btn_edit"], lambda cid=cid: self._edit_client(cid),
                     C["btn_edit"], icon="✏", size=8, pad_x=8, pad_y=3).pack(side="left", padx=(0,4))
            make_btn(bf, t["btn_delete"], lambda cid=cid: self._del_client(cid),
                     C["btn_del"], icon="🗑", size=8, pad_x=8, pad_y=3).pack(side="left")
            # subtle separator
            tk.Frame(card, bg=C["divider"], height=1).pack(fill="x")

    def _edit_client(self, cid):
        with cn() as c: r = c.execute("SELECT * FROM clients WHERE id=?", (cid,)).fetchone()
        if not r: return
        fields = [("lbl_lastname","entry",None),("lbl_firstname","entry",None),("lbl_phone","entry",None)]
        vals = {"lbl_lastname":r["nom"],"lbl_firstname":r["prenom"],"lbl_phone":r["telephone"] or ""}
        def save(d):
            if not d["lbl_lastname"] or not d["lbl_firstname"]: return self.t["err_fill"]
            with cn() as c:
                c.execute("UPDATE clients SET nom=?,prenom=?,telephone=? WHERE id=?",
                          (d["lbl_lastname"],d["lbl_firstname"],d["lbl_phone"],cid))
            self.after(600, self.show_clients)
        self._popup(self.t["edit_client"], fields, vals, save)

    def _del_client(self, cid):
        with cn() as c:
            n = c.execute("SELECT COUNT(*) FROM reservations WHERE client_id=?", (cid,)).fetchone()[0]
        if n: messagebox.showwarning(self.t["confirm_title"], self.t["err_client_busy"]); return
        if not messagebox.askyesno(self.t["confirm_title"], self.t["confirm_delete"]): return
        with cn() as c: c.execute("DELETE FROM clients WHERE id=?", (cid,))
        self.show_clients()

    # ══════════════════════════════════════════════════
    #  📅  RESERVATIONS
    # ══════════════════════════════════════════════════
    def show_reservations(self):
        self._clear(); self._set_page("reservations"); self._header("📅", self.t["resa_title"])
        sf = tk.Frame(self.main, bg=C["bg"]); sf.pack(fill="x", padx=PAD, pady=(16, 0))
        self._rs_search_e = make_entry(sf, placeholder=self.t["search_ph"])
        self._rs_search_e.pack(fill="x", ipady=8)
        self._rs_search_e.bind("<KeyRelease>", lambda e: self._render_resas())
        self._rs_box = tk.Frame(self.main, bg=C["bg"])
        self._rs_box.pack(fill="both", expand=True)
        self._render_resas()

    def _render_resas(self):
        for w in self._rs_box.winfo_children(): w.destroy()
        t = self.t
        raw = self._rs_search_e.get()
        q = "" if raw == t["search_ph"] else raw
        like = f"%{q}%"
        with cn() as c:
            rows = c.execute("""SELECT r.id, c.nom||' '||c.prenom client, ch.nom chambre,
                r.date_debut, r.date_fin, r.statut, r.montant
                FROM reservations r JOIN clients c ON c.id=r.client_id
                JOIN chambres ch ON ch.id=r.chambre_id
                WHERE c.nom LIKE ? OR c.prenom LIKE ? OR ch.nom LIKE ?
                ORDER BY r.id DESC""", (like, like, like)).fetchall()

        card = self._card_frame(self._rs_box)
        card.pack(fill="both", expand=True, padx=PAD, pady=(12, 20))

        hdr = tk.Frame(card, bg=C["topbar"]); hdr.pack(fill="x")
        cols = [t["col_client"],t["col_room"],t["col_start"],t["col_end"],t["col_status"],t["col_amount"],t["col_actions"]]
        ws   = [16, 14, 12, 12, 10, 10, 14]
        for txt, w in zip(cols, ws):
            tk.Label(hdr, text=txt, bg=C["topbar"], fg=C["blue"],
                     font=("Segoe UI",10,"bold"), width=w, anchor="w", pady=10, padx=8).pack(side="left")

        sc_map = {"En cours": C["green"], "Terminée": C["orange"], "Annulée": C["muted"]}
        for i, r in enumerate(rows):
            bg = C["row_alt"] if i % 2 else C["card"]
            row_f = tk.Frame(card, bg=bg); row_f.pack(fill="x")
            for val, w in zip([r["client"],r["chambre"],r["date_debut"],r["date_fin"]], [16,14,12,12]):
                tk.Label(row_f, text=val, bg=bg, fg=C["white"], font=("Segoe UI",10),
                         width=w, anchor="w", padx=8, pady=8).pack(side="left")
            # status with color
            sc = sc_map.get(r["statut"], C["sub"])
            tk.Label(row_f, text=r["statut"], bg=bg, fg=sc, font=("Segoe UI",10,"bold"),
                     width=10, anchor="w", padx=8).pack(side="left")
            tk.Label(row_f, text=f"{r['montant']:.0f} €", bg=bg, fg=C["white"],
                     font=("Segoe UI",10), width=10, anchor="w", padx=8).pack(side="left")
            bf = tk.Frame(row_f, bg=bg, padx=4); bf.pack(side="left")
            rid = r["id"]
            make_btn(bf, t["btn_edit"], lambda rid=rid: self._edit_resa(rid),
                     C["btn_edit"], icon="✏", size=8, pad_x=6, pad_y=3).pack(side="left", padx=(0,4))
            make_btn(bf, t["btn_delete"], lambda rid=rid: self._del_resa(rid),
                     C["btn_del"], icon="🗑", size=8, pad_x=6, pad_y=3).pack(side="left")
            tk.Frame(card, bg=C["divider"], height=1).pack(fill="x")

    def _edit_resa(self, rid):
        with cn() as c:
            r = c.execute("SELECT * FROM reservations WHERE id=?", (rid,)).fetchone()
            rooms = c.execute("SELECT id,nom FROM chambres").fetchall()
        if not r: return
        rn = [rm["nom"] for rm in rooms]; ri = [rm["id"] for rm in rooms]
        cr = next((rm["nom"] for rm in rooms if rm["id"]==r["chambre_id"]), "")
        fields = [("lbl_checkin","entry",None),("lbl_checkout","entry",None),
                  ("lbl_room","combo",rn),("lbl_status","combo",["En cours","Terminée","Annulée"])]
        vals = {"lbl_checkin":r["date_debut"],"lbl_checkout":r["date_fin"],"lbl_room":cr,"lbl_status":r["statut"]}
        def save(d):
            deb, fin = d["lbl_checkin"].strip(), d["lbl_checkout"].strip()
            try: d1=datetime.strptime(deb,"%Y-%m-%d"); d2=datetime.strptime(fin,"%Y-%m-%d"); assert d2>d1
            except: return self.t["err_date"]
            nri = rn.index(d["lbl_room"]) if d["lbl_room"] in rn else -1
            if nri<0: return self.t["err_fill"]
            nid=ri[nri]; nuits=(d2-d1).days
            with cn() as c:
                px=c.execute("SELECT prix_nuit FROM chambres WHERE id=?",(nid,)).fetchone()[0]
                mt=nuits*px
                if r["chambre_id"]!=nid or d["lbl_status"]!="En cours":
                    c.execute("UPDATE chambres SET statut='Disponible' WHERE id=?",(r["chambre_id"],))
                if d["lbl_status"]=="En cours":
                    c.execute("UPDATE chambres SET statut='Occupée' WHERE id=?",(nid,))
                c.execute("UPDATE reservations SET date_debut=?,date_fin=?,chambre_id=?,statut=?,montant=? WHERE id=?",
                          (deb,fin,nid,d["lbl_status"],mt,rid))
            self.after(600, self.show_reservations)
        self._popup(self.t["edit_resa"], fields, vals, save)

    def _del_resa(self, rid):
        if not messagebox.askyesno(self.t["confirm_title"], self.t["confirm_delete"]): return
        with cn() as c:
            r=c.execute("SELECT chambre_id,statut FROM reservations WHERE id=?",(rid,)).fetchone()
            if r and r["statut"]=="En cours":
                c.execute("UPDATE chambres SET statut='Disponible' WHERE id=?",(r["chambre_id"],))
            c.execute("DELETE FROM reservations WHERE id=?",(rid,))
        self.show_reservations()

    # ══════════════════════════════════════════════════
    #  ➕  NEW RESERVATION
    # ══════════════════════════════════════════════════
    def show_new_reservation(self):
        self._clear(); self._set_page("new"); self._header("➕", self.t["new_title"])
        t = self.t

        # Two-column form layout inside a card
        card = self._card_frame(self.main)
        card.pack(fill="x", padx=PAD, pady=(16, 20))
        tk.Frame(card, bg=C["accent"], height=3).pack(fill="x")
        body = tk.Frame(card, bg=C["card"], padx=32, pady=24); body.pack(fill="x")

        # Columns
        left  = tk.Frame(body, bg=C["card"]); left.pack(side="left", fill="both", expand=True, padx=(0,16))
        right = tk.Frame(body, bg=C["card"]); right.pack(side="left", fill="both", expand=True, padx=(16,0))

        vs = {k: tk.StringVar() for k in ["nom","prenom","tel","debut","fin"]}
        vs["debut"].set(str(date.today()))

        def field(parent, lbl, var):
            tk.Label(parent, text=lbl, bg=C["card"], fg=C["sub"],
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(12, 4))
            make_entry(parent, var).pack(fill="x", ipady=8)

        # Left column: client info
        tk.Label(left, text="👤  Client", bg=C["card"], fg=C["white"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Frame(left, bg=C["divider"], height=1).pack(fill="x", pady=(0, 4))
        field(left, t["lbl_lastname"], vs["nom"])
        field(left, t["lbl_firstname"], vs["prenom"])
        field(left, t["lbl_phone"], vs["tel"])

        # Right column: booking info
        tk.Label(right, text="🗓  Booking", bg=C["card"], fg=C["white"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Frame(right, bg=C["divider"], height=1).pack(fill="x", pady=(0, 4))

        tk.Label(right, text=t["lbl_room"], bg=C["card"], fg=C["sub"],
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(12, 4))
        with cn() as c:
            rooms = c.execute("SELECT id,nom,prix_nuit FROM chambres WHERE statut='Disponible'").fetchall()
        ch_lbl = [f"{r['nom']}  ·  {r['prix_nuit']:.0f} €{t['per_night']}" for r in rooms]
        ch_ids = [r["id"] for r in rooms]; ch_px = [r["prix_nuit"] for r in rooms]
        cv = tk.StringVar(value=ch_lbl[0] if ch_lbl else "")
        ttk.Combobox(right, textvariable=cv, values=ch_lbl, state="readonly",
                     font=("Segoe UI", 11)).pack(fill="x", ipady=5)

        field(right, t["lbl_checkin"], vs["debut"])
        field(right, t["lbl_checkout"], vs["fin"])

        # Bottom: message + button
        bottom = tk.Frame(card, bg=C["card"], padx=32, pady=16); bottom.pack(fill="x")
        msg = tk.Label(bottom, text="", bg=C["card"], font=("Segoe UI", 11, "bold"))
        msg.pack(pady=(0, 8))

        def save():
            nom=vs["nom"].get().strip(); prenom=vs["prenom"].get().strip()
            tel=vs["tel"].get().strip(); deb=vs["debut"].get().strip(); fin=vs["fin"].get().strip()
            if not all([nom,prenom,deb,fin,cv.get()]):
                msg.config(text=f"⚠  {t['err_fill']}", fg=C["accent"]); return
            try:
                d1=datetime.strptime(deb,"%Y-%m-%d"); d2=datetime.strptime(fin,"%Y-%m-%d"); assert d2>d1
            except: msg.config(text=f"⚠  {t['err_date']}", fg=C["accent"]); return
            i=ch_lbl.index(cv.get()); nuits=(d2-d1).days; mt=nuits*ch_px[i]
            with cn() as c:
                c.execute("INSERT INTO clients (nom,prenom,telephone) VALUES (?,?,?)",(nom,prenom,tel))
                cid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
                c.execute("INSERT INTO reservations (client_id,chambre_id,date_debut,date_fin,statut,montant) VALUES (?,?,?,?,?,?)",
                          (cid,ch_ids[i],deb,fin,"En cours",mt))
                c.execute("UPDATE chambres SET statut='Occupée' WHERE id=?",(ch_ids[i],))
            msg.config(text=f"✅  {t['ok_saved'].format(n=nuits,m=f'{mt:.0f}')}", fg=C["green"])
            for v in vs.values(): v.set(""); vs["debut"].set(str(date.today())); cv.set("")

        make_btn(bottom, f"  {t['btn_save']}  ", save, C["btn_save"],
                 icon="💾", size=12, pad_x=24, pad_y=10).pack(fill="x")

    # ── TREEVIEW TABLE ─────────────────────────────
    def _tree(self, parent, columns, rows):
        card = self._card_frame(parent)
        card.pack(fill="both", expand=True, padx=PAD, pady=(0, 20))
        tree = ttk.Treeview(card, columns=columns, show="headings",
                            style="T.Treeview", height=min(len(rows)+1, 12))
        vsb = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y"); tree.pack(fill="both", expand=True)
        for c in columns:
            tree.heading(c, text=c); tree.column(c, width=130, anchor="center", minwidth=80)
        for i, r in enumerate(rows):
            vs = [f"{v:,.0f} €" if isinstance(v, float) else str(v) for v in r]
            tag = "green" if len(r)>4 and r[4]=="En cours" else ("alt" if i%2 else "")
            tree.insert("", "end", values=vs, tags=(tag,))
        tree.tag_configure("green", foreground=C["green"])
        tree.tag_configure("alt",   background=C["row_alt"])


# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    App().mainloop()
