import swisseph as swe
from datetime import datetime
import pytz  # Install using `pip install pytz`

# Set the path to the Swiss Ephemeris data files
swe.set_ephe_path('./ephe')  # Replace './ephe' with your actual path to the ephemeris files

# Define the planets to calculate
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Rahu (North Node)": swe.MEAN_NODE,  # Mean Rahu
    "Ketu (South Node)": swe.MEAN_NODE  # Mean Ketu (Rahu + 180 degrees)
}


def jd(d, m, y):
    if m < 3:
        m += 12
        y -= 1
    a = y // 100
    b = 30.6 * (m + 1)
    l = int(b)
    j = 365 * y + y // 4 + l + 2 - a + a // 4 + d
    return j

def calculate_b6(d, m, y):
    h = 12
    mt = 0
    s = 0
    time_zone = 5.5
    h6 = (h + mt / 60 + s / 3600 - (12 + time_zone)) / 24
    b6 = (jd(d, m, y) - 694025 + h6) / 36525
    return b6

def raman_ayan(dd, mm, yy):
    return 21.013972 + 1.398191 * calculate_b6(dd, mm, yy)

def lahiri_ayan(dd, mm, yy):
    b6 = calculate_b6(dd, mm, yy)
    return 22.460148 + 1.396042 * b6 + 0.000308 * b6 * b6

def kpayan_old(dd, mm, yy):
    return (yy + (mm * 30 + dd) / 365 - 297.3204723) * 50.2388475 / 3600

def kpayan_new(dd, mm, yy):
    kpaya_on_1st_jan = 22 + (1335 + (yy - 1900) * 50.2388475) / 3600 + (yy - 1900) * (yy - 1900) * 0.000111 / 3600
    days_after_1st_jan = ((mm - 1) * 30 + (dd - 1)) / 3600
    correction_for_days = days_after_1st_jan / 365 * (50.2388475 + 0.000111 * 20)
    new_aya = kpaya_on_1st_jan + correction_for_days
    return new_aya

def kpayan_khu(dd, mm, yy):
    day_aya = 50.2388475 / 365.25
    total_day = (yy - 291) * 365.25
    total_day += mm * 30 + dd - 114
    new_aya = day_aya * total_day
    new_aya /= 3600
    return new_aya

def dms(x):
    negative = False
    if x < 0:
        negative = True
        x = -x
    deg = int(x)
    parts = f"{deg}:"
    temp = x - deg
    min_ = int(temp * 60)
    parts += f"{min_}:"
    temp = temp * 60 - min_
    sec = int(temp * 60 + 0.5)
    parts += f"{sec}"
    if negative:
        parts = "-" + parts
    return parts


def get_ut_time(local_time, timezone_str):
    """
    Convert local time to Universal Time (UT).

    :param local_time: A datetime object representing the local time
    :param timezone_str: Timezone string (e.g., 'Asia/Kolkata', 'America/New_York')
    :return: A datetime object representing the time in Universal Time (UT)
    """
    local_tz = pytz.timezone(timezone_str)
    local_time = local_tz.localize(local_time)  # Localize the time
    ut_time = local_time.astimezone(pytz.utc)  # Convert to Universal Time (UTC/UT)
    print(f"local_tz {local_tz} local_time {local_time} ut_time {ut_time}")

    return ut_time

def calculate_planet_positions(year, month, day, hour, timezone):
    """
    Calculate Julian date, Lahiri ayanamsa, and positions of all planets.

    :param year: Year (e.g., 2024)
    :param month: Month (1-12)
    :param day: Day (1-31)
    :param hour: Fractional hours (e.g., 12.5 for 12:30 PM)
    :param timezone: Timezone string (e.g., 'Asia/Kolkata', 'America/New_York')
    :return: Dictionary with positions of all planets (tropical and sidereal)
    """
    # Step 1: Get UT time
    local_time = datetime(year, month, day, int(hour), int((hour % 1) * 60))  # Create local datetime
    ut_time = get_ut_time(local_time, timezone)
    print(f"ut_time {ut_time}")
    # Step 2: Convert UT time to Julian Day
    julian_day = swe.julday(ut_time.year, ut_time.month, ut_time.day,
                            ut_time.hour + ut_time.minute / 60.0)

    # Step 3: Calculate Lahiri Ayanamsa
    # lahiri_ayanamsa = 23.866111
    
    lahiri_ayanamsa = lahiri_ayan(day, month, year)

    print(f"lahiri_ayanamsa {lahiri_ayanamsa}")
    # Step 4: Calculate positions for all planets
    positions = {}
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    for planet_name, planet_id in PLANETS.items():
        result, _ = swe.calc_ut(julian_day, planet_id, swe.FLG_SWIEPH)
        tropical_longitude = result[0]

        # Adjust for Lahiri ayanamsa to get sidereal position
        sidereal_longitude = tropical_longitude - lahiri_ayanamsa
        if sidereal_longitude < 0:
            sidereal_longitude += 360  # Ensure within 0-360 degrees
            
        sign_index = int(sidereal_longitude // 30)  # 30 degrees per sign
        sign_name = zodiac_signs[sign_index]
        degree_in_sign = sidereal_longitude % 30  # Degree within sign


        # Add the positions to the dictionary
        positions[planet_name] = {
            "sign": sign_name,
            "degree": round(degree_in_sign, 6),
            "tropical": round(tropical_longitude, 6),
            "sidereal": round(sidereal_longitude, 6)
        }

    # Return results
    return {
        "julian_date": julian_day,
        "ut_time": ut_time.strftime("%Y-%m-%d %H:%M:%S"),
        "lahiri_ayanamsa": round(lahiri_ayanamsa, 6),
        "planet_positions": positions
    }

# Example usage
# if __name__ == "__main__":
    # Input: Gregorian date (Year, Month, Day, Hour) and Timezone
    year = 2000
    month = 8
    day = 15
    hour = 11.45  # 3:00 PM local time
    # year = 2000
    # month = 9
    # day = 5
    # hour = 12.25  # 3:00 PM local time
    timezone = 'Asia/Kolkata'  # Replace with your timezone, e.g., 'America/New_York'

    # Perform the calculations
    results = calculate_planet_positions(year, month, day, hour, timezone)

    # Print the results
    print(f"UT Time: {results['ut_time']}")
    print(f"Julian Date: {results['julian_date']}")
    print(f"Lahiri Ayanamsa: {results['lahiri_ayanamsa']} degrees")
    print("Planet Positions:")
    for planet, pos in results['planet_positions'].items():
        print(f"{planet} Sign {pos['sidereal'] / 30} degree {pos['sidereal'] % 30}")
        print(f"{planet}: Tropical = {pos['tropical']}°, Sidereal = {pos['sidereal']}°\n")
