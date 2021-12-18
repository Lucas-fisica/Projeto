from numpy import sin, cos, pi, arctan, mean, sum, sqrt, array, random, arange


def seno(date: array, feq: float):
    """retorna valores do seno para um date fornecido e uma frequencia
    """
    return sin(2*pi*date*feq)


def cosseno(date: array, feq: float):
    """Retorna valores do Cosseno para um date fornecido e uma frequencia
    """
    return cos(2*pi*date*feq)


def condi(a: float, b: float):
    """retorna o valor de fi para valores de A e B fornecidos
    """
    if a > 0:
        fi = arctan(-b / a)
        print(1)
    elif a < 0 < b:
        fi = arctan(-b / a) - pi
        print(2)
    elif a < 0 >= b:
        fi = arctan(-b / a) + pi
        print(3)
    elif a == 0 < b:
        fi = -pi/2
        print(4)
    elif a == 0 > b:
        fi = pi/2
        print(5)
    else:
        fi = pi/2
        print(6)
    return fi

# Modelo de ajuste
def modelo(xdate: array, a: float, b: float, feq: float):
    return a*cosseno(xdate, feq)+b*seno(xdate, feq)


def mmq(xdate: array, ydata: array, feq: float):
    """retorna os valores dos paramentros de ajuste para um xdate, ydate e
     uma frequencia fornecidos. O calculo é feito pelo metodo dos minimos quadrados
    """
    sen = seno(xdate, feq=feq)
    coss = cosseno(xdate, feq=feq)
    sen_2 = sen**2
    cos_2 = coss**2
    sencos = sen*coss
    delta = sum(cos_2)*sum(sen_2)-(sum(sencos))**2
    a = (sum(ydata*coss)*sum(sen_2)-sum(ydata*sen)*sum(sencos))/delta
    b = ((sum(ydata*sen)*sum(cos_2))-sum(ydata*coss)*sum(sencos))/delta
    r = sqrt(a**2 + b**2)
    fi = condi(a, b)
    return a, b, r, fi


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit as cf

    # criando alguns sinais de teste
    x = arange(1, 250)
    y0 = 3 * cosseno(x, 1/12) + 5 * seno(x, 1/12) + random.standard_normal(len(x))
    y1 = 7 * seno(x, 1/6) + random.standard_normal(len(x))
    y2 = 13 * cosseno(x, 1/25) - random.standard_normal(len(x))
    y3 = 5*seno(cosseno(x, 1/4), 1/4)
    y4 = 5 * seno(cosseno(x, 1 / 35), 1 / 35)+34*cosseno(x, 1/35)
    # sobrepondo os sinais
    y = y0+y1+y2+y3+y4
    # calculando os valores de A, B e fi para uma frequencia especifica usando como base o
    #dos minimos quadrados definido acima

    feq = 1/35
    yx = mmq(xdate=x, ydata=y, feq=feq)+mean(y)
    print('valores pra o mmq =',yx)
    # fazendo o ajuste usando o mmq definido acima
    ajuste = modelo(xdate=x, a=yx[0], b=yx[1], feq=feq)

    # Fazendo o ajuste com o scipy.optimize.curve_fit

    param, _ = cf(f=modelo, xdata=x, ydata=y, p0=(0, 0, feq))
    print('Valores do Scipy =', param)
    ajuste_scipy = modelo(xdate=x, a=param[0], b=param[1], feq=feq)+mean(y)

    # plotando os resultados
    _, ax = plt.subplots(2, 1)
    ax[0].plot(x, y, label='Sinal')
    ax[0].plot(x, ajuste, label='mmq')
    ax[0].legend()
    ax[1].plot(x, ajuste_scipy, label='Scipy')
    ax[1].plot(x, y, label='Sinal')
    ax[1].legend()
    plt.show()

