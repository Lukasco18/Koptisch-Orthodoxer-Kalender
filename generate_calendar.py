import os
import datetime
from datetime import date, datetime as dt, timedelta, timezone
import uuid

# ==============================================================================
# 1. KOPTISCHE DATUMSBERECHNUNG (JDN-KONVERTIERUNG)
# ==============================================================================

COPTIC_MONTHS = [
    ("Thout", "Tout"),
    ("Paopi", "Baba"),
    ("Hathor", "Hatour"),
    ("Koiak", "Kiahk"),
    ("Tobi", "Touba"),
    ("Meshir", "Amshir"),
    ("Paremhat", "Baramhat"),
    ("Parmouti", "Baramouda"),
    ("Pashons", "Bashans"),
    ("Paoni", "Baona"),
    ("Epip", "Abib"),
    ("Mesori", "Misra"),
    ("Pi Kogi Enavot", "Nasie"),
]

def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return (
        day
        + (153 * m + 2) // 5
        + 365 * y
        + y // 4
        - y // 100
        + y // 400
        - 32045
    )

def jdn_to_coptic(jdn: int):
    c_year = (4 * (jdn - 1825030) + 1463) // 1461
    jdn_1_thout = 1825029 + 365 * (c_year - 1) + ((c_year - 1) // 4) + 1

    if jdn < jdn_1_thout:
        c_year -= 1
        jdn_1_thout = 1825029 + 365 * (c_year - 1) + ((c_year - 1) // 4) + 1

    day_of_year = jdn - jdn_1_thout

    if day_of_year < 360:
        c_month = day_of_year // 30
        c_day = (day_of_year % 30) + 1
    else:
        c_month = 12
        c_day = (day_of_year - 360) + 1

    return c_day, c_month, c_year


# ==============================================================================
# 2. DYNAMISCHE OSTER- UND PARAMOUN-BERECHNUNGEN
# ==============================================================================

def get_orthodox_easter(year: int) -> date:
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    julian_month = (d + e + 114) // 31
    julian_day = ((d + e + 114) % 31) + 1
    
    julian_easter = date(year, julian_month, julian_day)
    return julian_easter + timedelta(days=13)

def get_paramoun_dates(feast_date: date) -> list[date]:
    weekday = feast_date.weekday()
    if weekday == 6:
        return [feast_date - timedelta(days=2), feast_date - timedelta(days=1)]
    elif weekday == 0:
        return [
            feast_date - timedelta(days=3),
            feast_date - timedelta(days=2),
            feast_date - timedelta(days=1)
        ]
    else:
        return [feast_date - timedelta(days=1)]


# ==============================================================================
# 3. KOPTISCHE FASTEN- UND FESTLOGIK (TAGESPRÜFUNG)
# ==============================================================================

def get_daily_status(g_date: date, c_day: int, m_idx: int) -> str:
    weekday = g_date.weekday()
    year = g_date.year

    easter = get_orthodox_easter(year)
    jona_start = easter - timedelta(days=69)
    jona_end = jona_start + timedelta(days=2)
    jona_feast = jona_end + timedelta(days=1)
    
    lent_start = easter - timedelta(days=55)
    lazarus_sat = easter - timedelta(days=8)
    palm_sunday = easter - timedelta(days=7)
    good_friday = easter - timedelta(days=2)
    holy_saturday = easter - timedelta(days=1)
    
    fifty_days_end = easter + timedelta(days=49)
    ascension = easter + timedelta(days=39)
    
    apostles_fast_start = fifty_days_end + timedelta(days=1)
    apostles_fast_end = date(year, 7, 11)

    nativity_date = date(year, 1, 7)
    theophany_date = date(year, 1, 19)
    nativity_paramouns = get_paramoun_dates(nativity_date)
    theophany_paramouns = get_paramoun_dates(theophany_date)

    if g_date == easter:
        return "🎉 Koptisches Osterfest (Resurrection)"
    elif g_date == holy_saturday:
        return "✝️ Koptischer Karsamstag"
    elif g_date == good_friday:
        return "✝️ Karfreitag (Strengstes Fasten)"
    elif g_date == palm_sunday:
        return "🌿 Palmsonntag"
    elif g_date == lazarus_sat:
        return "✝️ Lazarus-Samstag"
    elif g_date == ascension:
        return "☁️ Christi Himmelfahrt (Kein Fasten)"
    elif g_date == fifty_days_end:
        return "🕊️ Pfingsten (Kein Fasten)"
    elif jona_start <= g_date <= jona_end:
        return "🐋 Jona-Fasten (Strenges Fasten)"
    elif g_date == jona_feast:
        return "🎉 Fest des Propheten Jona"

    if palm_sunday < g_date < good_friday:
        return "✝️ Karwoche (Strenges Fasten)"

    if lent_start <= g_date < lazarus_sat:
        if weekday in (2, 4):
            return "🥗 Großes Fasten (Mittwoch/Freitag - Streng)"
        return "🥗 Großes Fasten (Kein Fisch)"

    if easter <= g_date <= fifty_days_end:
        return "🎉 50 Freudentage / Pentekostarion (Kein Fasten)"

    if apostles_fast_start <= g_date <= apostles_fast_end:
        if weekday in (2, 4):
            return "🥗 Apostelfasten (Mittwoch/Freitag - Streng)"
        return "🐟 Apostelfasten (Fisch erlaubt)"

    if g_date in nativity_paramouns:
        return "🍽️ Paramoun von Weihnachten (Strenges Fasten)"
    elif g_date == nativity_date:
        return "🎉 Koptisches Weihnachtsfest (Fastenfrei)"
    elif date(year, 1, 8) <= g_date < (theophany_paramouns[0] if theophany_paramouns else theophany_date):
        if g_date == date(year, 1, 14):
            return "🎉 Beschneidung des Herrn"
        return "🎉 12 Freudentage nach Weihnachten (Kein Fasten)"

    if g_date in theophany_paramouns:
        return "🍽️ Paramoun der Taufe Christi (Strenges Fasten)"
    elif g_date == theophany_date:
        return "🎉 Theophanie (Fest der Taufe Christi)"
    elif g_date == date(year, 1, 21):
        return "🎉 Hochzeit zu Kana"

    if m_idx == 0:
        if c_day == 1:
            return "🎉 Koptisches Neujahr (Nayrouz)"
        elif 17 <= c_day <= 19:
            if weekday in (2, 4):
                return "✝️ Fest der Kreuzerhöhung (Fastentag Mi/Fr)"
            return "🎉 Fest der Kreuzerhöhung (Kein Fasten)"

    if g_date == date(year, 4, 7):
        return "🎉 Mariä Verkündigung"
    elif g_date == date(year, 6, 1):
        return "🎉 Einzug Christi in Ägypten"
    elif g_date == date(year, 7, 12):
        return "🎉 Fest der Apostel Petrus und Paulus"
    elif g_date == date(year, 8, 19):
        return "🎉 Verklärung des Herrn"
    elif g_date == date(year, 8, 22):
        return "🎉 Aufnahme des Körpers der Hl. Maria"

    if date(year, 8, 7) <= g_date <= date(year, 8, 21):
        if weekday in (2, 4):
            return "🥗 Fasten der Hl. Maria (Mittwoch/Freitag - Streng)"
        return "🐟 Fasten der Hl. Maria (Fisch erlaubt)"

    is_advent = (g_date >= date(year, 11, 25)) or (g_date <= date(year, 1, 6))
    if is_advent and g_date not in nativity_paramouns and g_date != nativity_date:
        if weekday in (2, 4):
            return "🥗 Geburtsfasten (Mittwoch/Freitag - Streng)"
        return "🐟 Geburtsfasten (Fisch erlaubt)"

    if weekday in (2, 4):
        return "🥗 Fastentag (Mittwoch/Freitag)"

    return "Kein Fasten"


# ==============================================================================
# 4. REPARATUR-, INTEGRITÄTS- UND ICS-GENERATIONSLOGIK
# ==============================================================================

def repair_and_read_existing_ics(filepath: str):
    """Liest die bestehende Datei, entfernt abgebrochene Blöcke am Ende

    und findet das letzte valide Datum.
    """
    if not os.path.exists(filepath):
        return [], None

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\r\n') for line in f.readlines()]

    # Entferne evtl. vorhandenen VCALENDAR-Abschluss für nahtloses Anfügen
    if lines and lines[-1] == "END:VCALENDAR":
        lines.pop()

    # Schneide unvollständige Zeilen/Events am Ende ab
    while lines and lines[-1] != "END:VEVENT":
        lines.pop()

    # Letztes Startdatum ermitteln
    last_date = None
    for line in reversed(lines):
        if line.startswith("DTSTART"):
            date_str = line.split(":")[-1]
            last_date = dt.strptime(date_str, "%Y%m%d").date()
            break

    if last_date:
        next_start_date = last_date + timedelta(days=1)
        return lines, next_start_date

    return [], None


def generate_coptic_ics(target_end_date: date, filename: str = "kalender.ics"):
    """Prüft eine vorhandene Datei, repariert Lücken und führt die Kalendererstellung fort."""
    existing_lines, resume_date = repair_and_read_existing_ics(filename)

    if existing_lines and resume_date:
        print(f"Bestehende Datei erkannt und repariert. Setze nahtlos ab {resume_date} fort...")
        start_date = resume_date
        base_header = "\n".join(existing_lines) + "\n"
    else:
        print("Erstelle neue Kalenderdatei...")
        start_date = date.today()  # Beginn der ersten Nasie-Tage
        base_header = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Koptischer Kalender Generator//DE
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Koptischer Kalender
X-WR-TIMEZONE:Europe/Vienna
"""

    if start_date > target_end_date:
        print("Der Kalender ist bereits auf dem neuesten Stand.")
        return

    events = []
    curr = start_date

    while curr <= target_end_date:
        jdn = gregorian_to_jdn(curr.year, curr.month, curr.day)
        c_day, m_idx, c_year = jdn_to_coptic(jdn)

        m_name_eng, m_name_alt = COPTIC_MONTHS[m_idx]
        status = get_daily_status(curr, c_day, m_idx)

        coptic_date_str = f"{c_day}. {m_name_eng} ({m_name_alt}) {c_year}"
        dtstart = curr.strftime("%Y%m%d")
        dtend = (curr + timedelta(days=1)).strftime("%Y%m%d")
        uid = f"coptic-{dtstart}-{uuid.uuid4().hex[:6]}@kalender"
        dtstamp = dt.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        event = f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
SUMMARY:📅 {coptic_date_str} | {status}
DESCRIPTION:Koptisches Datum: {coptic_date_str}\\nStatus: {status}
STATUS:CONFIRMED
END:VEVENT"""
        events.append(event)
        curr += timedelta(days=1)

    events_block = "\n".join(events)
    final_ics = f"{base_header}{events_block}\nEND:VCALENDAR\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_ics)

    print(f"Kalenderdatei '{filename}' wurde erfolgreich bis {target_end_date} vervollständigt!")

if __name__ == "__main__":
    # Generiert/Repariert den Kalender bis 1 Jahr in die Zukunft
    target_date = date.today() + timedelta(days=365)
    generate_coptic_ics(target_date, "kalender.ics")
