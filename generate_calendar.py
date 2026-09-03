from datetime import date, timedelta

def get_julian_easter(year: int) -> date:
    """
    Berechnet das koptisch-orthodoxe Osterdatum für ein gegebenes Jahr (GREGORIANISCHES DATUM).
    Basiert auf dem Alexandrinischen Computus (+13 Tage Versatz im 20./21. Jahrhundert).
    """
    a = year % 19
    b = year % 4
    c = year % 7
    d = (19 * a + 15) % 30
    e = (2 * b + 4 * c + 6 * d + 6) % 7
    return date(year, 3, 22) + timedelta(days=(d + e + 13))

def is_coptic_leap_year(coptic_year: int) -> bool:
    """Prüft, ob ein koptisches Jahr ein Schaltjahr ist."""
    return (coptic_year % 4) == 3

def generate_coptic_ics():
    current_year = date.today().year
    start_year = current_year
    end_year = current_year + 10  # Generiert automatisch die nächsten 10 Jahre
    
    events = []

    for year in range(start_year, end_year + 1):
        easter = get_julian_easter(year)
        
        # --- BEWEGLICHE FESTE & FASTENZEITEN ---
        jonah_start = easter - timedelta(days=69)
        jonah_end = jonah_start + timedelta(days=3)  # 3 Tage (Mo, Di, Mi)
        jonah_feast = easter - timedelta(days=66)     # Do
        
        lent_start = easter - timedelta(days=55)      # 55 Tage bis Ostern
        lazarus_saturday = easter - timedelta(days=8)
        palm_sunday = easter - timedelta(days=7)
        maundy_thursday = easter - timedelta(days=3)
        good_friday = easter - timedelta(days=2)
        thomas_sunday = easter + timedelta(days=7)
        ascension = easter + timedelta(days=39)
        pentecost = easter + timedelta(days=49)
        
        apostles_fast_start = pentecost + timedelta(days=1)
        apostles_fast_end = date(year, 7, 12)        # Apostelfest ist am 12. Juli
        
        # --- KOPTISCHES NEUJAHR (NAYROUZ) ---
        coptic_year = year - 284
        nayrouz_day = 12 if is_coptic_leap_year(coptic_year - 1) else 11
        nayrouz = date(year, 9, nayrouz_day)
        
        movable_events = [
            ("⛔ Fasten von Ninive (Jonafasten)", jonah_start, jonah_end, "3-tägiges strenges Fasten.\\nStufe: ⛔ Strenges Fasten (Kein Fisch 🚫)"),
            ("🎉 Fest des Propheten Jona", jonah_feast, jonah_feast + timedelta(days=1), "Festtag nach dem Jonafasten 🎉"),
            ("🚫 Große Fastenzeit (Großes Fasten)", lent_start, easter, "55-tägiges Fasten vor der Auferstehung.\\nStufe: 🚫 Kein Fisch erlaubt | Mittwochs & freitags strenges Fasten"),
            ("🎉 Lazarus-Samstag", lazarus_saturday, lazarus_saturday + timedelta(days=1), "Auferweckung des Hl. Lazarus 🎉"),
            ("🎉 Palmsonntag (Einzug in Jerusalem)", palm_sunday, palm_sunday + timedelta(days=1), "Großes Herrenfest: Hosanna-Sonntag 🎉"),
            ("⛔ Donnerstag des Bundes (Gründonnerstag)", maundy_thursday, maundy_thursday + timedelta(days=1), "Kleines Herrenfest: Einsetzung der Hl. Eucharistie ⛔"),
            ("⛔ Koptischer Karfreitag (Heiliger Freitag)", good_friday, good_friday + timedelta(days=1), "Kreuzigung unseres Herrn Jesus Christus ⛔"),
            ("🎉 Koptisches Osterfest (Auferstehung des Herrn)", easter, easter + timedelta(days=1), "Großes Herrenfest: Glorreiche Auferstehung 🎉"),
            ("🎉 Thomas-Sonntag", thomas_sunday, thomas_sunday + timedelta(days=1), "Kleines Herrenfest 🎉"),
            ("🎉 Christi Himmelfahrt", ascension, ascension + timedelta(days=1), "Großes Herrenfest 🎉"),
            ("🎉 Pfingsten (Herabkunft des Heiligen Geistes)", pentecost, pentecost + timedelta(days=1), "Großes Herrenfest 🎉"),
            ("🐟 Apostelfasten", apostles_fast_start, apostles_fast_end, "Fasten der Hl. Apostel.\\nStufe: 🐟 Fisch erlaubt (außer an Mittwochen & Freitagen ⚠️)"),
        ]

        fixed_events = [
            ("⛔ Paramoni (Weihnachtsvorabend)", date(year, 1, 6), date(year, 1, 7), "Strenges Fasten vor Weihnachten (Kein Fisch 🚫) ⛔"),
            ("🎉 Koptisches Weihnachtsfest (Geburt Christi)", date(year, 1, 7), date(year, 1, 8), "Großes Herrenfest 🎉"),
            ("🎉 Fest der Beschneidung des Herrn", date(year, 1, 14), date(year, 1, 15), "Kleines Herrenfest 🎉"),
            ("⛔ Paramoni (Epiphanias-Vorabend)", date(year, 1, 18), date(year, 1, 19), "Strenges Fasten vor der Taufe Jesu (Kein Fisch 🚫) ⛔"),
            ("🎉 Taufe Jesu (Epiphanias / Theophanie)", date(year, 1, 19), date(year, 1, 20), "Großes Herrenfest 🎉"),
            ("🎉 Erstes Wunder Jesu (Hochzeit zu Kana)", date(year, 1, 21), date(year, 1, 22), "Kleines Herrenfest 🎉"),
            ("🎉 Darstellung Jesu im Tempel", date(year, 2, 15), date(year, 2, 16), "Kleines Herrenfest 🎉"),
            ("🎉 Fest des Heiligen Kreuzes (Frühling)", date(year, 3, 19), date(year, 3, 20), "Auffindung des Hl. Kreuzes durch Kaiserin Helena 🎉"),
            ("🎉 Einzug der Hl. Familie in Ägypten", date(year, 6, 1), date(year, 6, 2), "Kleines Herrenfest 🎉"),
            ("🎉 Fest der Heiligen Apostel (Petrus & Paulus)", date(year, 7, 12), date(year, 7, 13), "Gedenktag der Apostelfürsten St. Petrus und St. Paulus 🎉"),
            ("🐟 Marienfasten", date(year, 8, 7), date(year, 8, 22), "15-tägiges Fasten der Jungfrau Maria.\\nStufe: 🐟 Fisch erlaubt (außer an Mittwochen & Freitagen ⚠️)"),
            ("🎉 Die Verklärung Jesu (Metamorphosis)", date(year, 8, 19), date(year, 8, 20), "Kleines Herrenfest 🎉"),
            ("🎉 Aufnahme des Körpers der Hl. Maria", date(year, 8, 22), date(year, 8, 23), "Fest der Entschlafung und Aufnahme der Gottesgebärerin (Theotokos) 🎉"),
            (f"🎉 Nayrouz (Koptisches Neujahr {coptic_year})", nayrouz, nayrouz + timedelta(days=1), f"Koptisches Neujahr (1. Tout {coptic_year}) 🎉"),
            ("🎉 Fest des Heiligen Kreuzes (Herbst)", date(year, 9, 27), date(year, 9, 30), "3-tägiges Fest der Einweihung der Grabeskirche 🎉"),
            ("🐟 Adventsfasten / Weihnachtsfasten", date(year, 11, 25), date(year + 1, 1, 7), "43-tägiges Weihnachtsfasten.\\nStufe: 🐟 Fisch erlaubt (außer an Mittwochen & Freitagen ⚠️ sowie in der letzten Woche)"),
        ]

        # PRÜFUNG: Verkündigung des Herrn (29. Baramhat / 7. April)
        # Fällt es in die Karwoche (letzter Freitag der Fastenzeit bis Ostersonntag), wird es AUSGEKLAMMERT.
        annunciation = date(year, 4, 7)
        last_friday_lent = easter - timedelta(days=9)
        if not (last_friday_lent <= annunciation <= (easter + timedelta(days=1))):
            fixed_events.append(("🎉 Verkündigung des Herrn", annunciation, annunciation + timedelta(days=1), "Großes Herrenfest 🎉"))

        all_year_events = movable_events + fixed_events
        
        for summary, dtstart, dtend, desc in all_year_events:
            event_slug = summary.split()[1].replace("(", "").replace(")", "").lower() if len(summary.split()) > 1 else "event"
            uid = f"{dtstart.strftime('%Y%m%d')}-{event_slug}-{year}@koptisch-orthodox.org"
            events.append(
                f"BEGIN:VEVENT\n"
                f"UID:{uid}\n"
                f"DTSTAMP:20260903T120000Z\n"
                f"SUMMARY:{summary}\n"
                f"DESCRIPTION:{desc}\n"
                f"DTSTART;VALUE=DATE:{dtstart.strftime('%Y%m%d')}\n"
                f"DTEND;VALUE=DATE:{dtend.strftime('%Y%m%d')}\n"
                f"END:VEVENT"
            )

    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Koptisch-Orthodoxer Kalender Generator//DE\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:PUBLISH\n"
        "X-WR-CALNAME:Koptisch-Orthodoxer Kalender\n"
        "X-WR-CALDESC:Offizieller Koptisch-Orthodoxer Liturgiekalender mit Herrenfesten\\, Fastenzeiten und Heiligenfesten.\\n\\nFastenregeln:\\n🐟 Fisch erlaubt (außer an Mittwochen & Freitagen)\\n🚫 Kein Fisch erlaubt\\n⚠️ Mittwochs & freitags: Fasten das ganze Jahr (außer Kamsine/Herrenfeste)\\n⛔ Strenges Fasten\n"
        + "\n".join(events) +
        "\nEND:VCALENDAR"
    )

    with open("kalender.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)

if __name__ == "__main__":
    generate_coptic_ics()