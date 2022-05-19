import matplotlib.pyplot as plt

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Tablet:
    name: str
    month: int
    day: Optional[int]


NEBUCHADNEZZAR = [
    Tablet("GCCI 1, 218.", 1, 2),
    Tablet("Nbk. 41.", 1, 5),
    Tablet("Nbk. 411.", 1, 11),
    Tablet("*Bertin 1162.", 1, 21),
    Tablet("Nbk. 412.", 1, None),
    Tablet("GCCI 1, 93.", 2, 9),
    Tablet("VS 2, 1.", 2, 9),
    Tablet("CT 57, 121.", 2, 10),
    Tablet("CT 57, 82.", 2, 11),
    Tablet("CT 56, 312.", 2, 12),
    Tablet("GCCI 1, 159.", 2, 12),
    Tablet("Nbk. 413.", 2, 12),
    Tablet("*Bertin 1161.", 2, 20),
    Tablet("CT 57, 517.", 2, 23),
    Tablet("TuM 2/3, 225.", 2, 28),
    Tablet("Nbk. 414.", 2, None),
    Tablet("CT 57, 393.", 3, 5),
    Tablet("GCCI 1, 17.", 3, 11),
    Tablet("*AUWE 18, 1.", 3, 16),
    Tablet("Dillard, NB Texts:FLP 1555.", 3, 22),
    Tablet("CT 57, 43.", 4, 18),
    Tablet("Nbk. 415.", 4, 27),
    Tablet("AUWE 5, 147.", 4, None),
    Tablet("GCCI 2, 189.", 5, 8),
    Tablet("VS 3, 36.", 5, 9),
    Tablet("YOS 17, 9.", 5, 15),
    Tablet("Dillard, NB Texts:FLP 1556.", 5, 22),
    Tablet("CT 57, 49.", 5, 27),
    Tablet("BE 8/1, 23.", 5, 28),
    Tablet("*Goetze JNES 3 44:NCBT 286.", 6, 8),
    Tablet("Zawadzki ZA 86 217.", 6, 12),
    Tablet("AnOr 8, 18.", 6, 14),
    Tablet("GCCI 1, 164.", 6, 15),
    Tablet("Beaulieu NABU 1989/3 43.", 6, 16),
    Tablet("*Goetze JNES 3 44:NCBT 286.", 6, 21),
    Tablet("TCL 12, 58.", 6, 26)
]

AMEL = [
    Tablet("Cat.BM 8", 5, 20),
    Tablet("AOATS 4, 79.", 5, None),
    Tablet("Evetts, EvM. 1.", 6, 26),
    Tablet("ADFU 10, 56.", 6, 28),
    Tablet("Sack, CDCP n65.", 7, 10),
    Tablet("AUWE 5, 5.", 7, 16),
    Tablet("AOATS 4, 14.", 7, 17),
    Tablet("AOATS 4, 56.", 7, 20),
    Tablet("Evetts, EvM. 2.", 7, 19),
    Tablet("BIN 2, 109.", 7, 20),
    Tablet("AUWE 5, 4.", 9, 7),
    Tablet("BIN 1, 136.", 9, 7),
    Tablet("AOATS 4, 76.", 9, 18),
    Tablet("AOATS 4, 19.", 9, 23),
    Tablet("Evetts, EvM. 3.", 9, 24),
    Tablet("Evetts, EvM. 4.", 9, 28),
    Tablet("AOATS 4, 77.", 10, 1),
    Tablet("CT 57, 330.", 10, 1),
    Tablet("Sack, CDCP App. n3.", 10, 4),
    Tablet("AOATS 4, 88.", 10, 5),
    Tablet("GCCI 2, 94.", 10, 18),
    Tablet("GCCI 2, 79.", 10, 30),
    Tablet("Zawadzki ZA 86 218.", 11, 5),
    Tablet("Evetts, EvM. 5.", 11, 19),
    Tablet("Evetts, EvM. 6.", 11, 28),
    Tablet("GCCI 2, 93.", 12, 1),
    Tablet("CT 55, 702.", 12, 2),
    Tablet("AOATS 4, 23.", 12, 5),
    Tablet("Sack ZA 67 43f.", 12, 5),
    Tablet("Evetts, EvM. 7.", 12, 7),
    Tablet("CM 3, 51.", 12, 8),
    Tablet("AOATS 4, 66.", 12, 11),
    Tablet("Stigers JCS 28 n19.", 12, 12),
    Tablet("*AUWE 18, 69.", 12, 15),
    Tablet("AOATS 4, 40.", 12, 15),
    Tablet("GCCI 2, 88.", 12, 19),
    Tablet("Speleers, Receuil 277.", 12, 26),
    Tablet("Evetts, EvM. 8.", 12, 28)
]

MONTH_FRACTION = 1 / 12
DAY_FRACTION = 1 / ( 29.53 * 12)


def tablets_to_data(year: int, tablets: List[Tablet]):
    output = []
    for t in tablets:
        month_component = MONTH_FRACTION * (t.month - 1)
        # Unknown day - approximate to middle of month
        day = t.day if t.day is not None else 15
        day_component = DAY_FRACTION * (day - 1)
        value = month_component + day_component + year
        if len(output) > 0:
            last = output[len(output) - 1]
            # Where multiple matches for a single day, place in the slot of the next day instead
            if last == value:
                value = value + DAY_FRACTION
        output.append(value)
    assert len(output) == len(tablets)
    return output


def do_plot(title, data, ticks, output):
    fig, ax1 = plt.subplots()
    ax1.eventplot(data, color=['b', 'g'], linelengths = 1, lineoffsets = [0, -0.5])
    ax1.set_title(title)
    ax1.set_xlabel('Nebuchadnezzar II Years')
    ax1.xaxis.set_ticks(ticks)
    ax1.yaxis.set_visible(False)
    ax1.legend(['Nebuchadnezzar II', 'Amel-Marduk'])
    plt.savefig(output)


data = [tablets_to_data(43, NEBUCHADNEZZAR), tablets_to_data(43, AMEL)]
do_plot("Standard Chronology", data, [43, 44], "../src/graphics/nebuchadnezzar_amel_marduk.svg")

data = [tablets_to_data(43, NEBUCHADNEZZAR), tablets_to_data(44, AMEL)]
do_plot("Watchtower Chronology?", data, [43, 44], "../src/graphics/nebuchadnezzar_amel_marduk2.svg")
