def ChangeMonthtoPortuguese(dateIn):
    date = list(dateIn)
    if date[1] == 1:
        date[1] = "Janeiro"
    elif date[1] == 2:
        date[1] = "Fevereiro"
    elif date[1] == 3:
        date[1] = "Marco"
    elif date[1] == 4:
        date[1] = "Abril"
    elif date[1] == 5:
        date[1] = "Maio"
    elif date[1] == 6:
        date[1] = "Junho"
    elif date[1] == 7:
        date[1] = "Julho"
    elif date[1] == 8:
        date[1] = "Agosto"
    elif date[1] == 9:
        date[1] = "Setembro"
    elif date[1] == 10:
        date[1] = "Outubro"
    elif date[1] == 11:
        date[1] = "Novembro"
    else:
        date[1] = "Dezembro"

    DayString = str(date[2])
    YearString = str(date[0])
    HourString = str(date[3])
    MinuteString = str(date[4])
    SecondString = str(date[5])
    FullDate = DayString+" de "+date[1]+" de "+YearString+", as "+HourString+"h"+MinuteString+"min"+SecondString+"s."
    date.append(FullDate)
    return(date)
