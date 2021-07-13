def teamOpp():
    if "Do we have lead?":
        if "Can we search?":
            return "Search Card"
        else:
            if "Do we have Aces not Trump?":
                return "Random Ace"
            else:
                if "Do we have random no T no Trump?":
                    return "Random card"
                else:
                    return "Random card"
    else:
        if "Do we know our Partner?":
            if "Parter owns Trick?":
                return "Max value card"
            else:
                if "Can we win this trick?":
                    return "Max value winning Card"
                else:
                    if "Do we have Cards not Trump?":
                        return "Min value card not Trump"
                    else:
                        return "Min value"
        else:
            if "Can we win this trick?":
                return "Max value Card"
            else:
                if "Do we have Cards not Trump?":
                    return "Min value card not Trump"
                else:
                    return "Min value"