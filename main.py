# pedir gt
# pedir bps
# pedir Ancho de banda

# numero de armonicos = bw/primeroArmonico


import math
from mpl_toolkits import mplot3d

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fake_gt = input("Ingrese g(t)")
# for each character in fake_gt, it converts that character into an int and adds it into gt.
gt = [int(character) for character in str(fake_gt)]
print("gt: ", gt)

#cada vez que el bit cambia, hay un nuevo limite
limites = []
counter: int = 0
bitAnterior = gt[0]
x: int
for x in gt:
    if x != bitAnterior:
        bitAnterior = x
        limites.append(counter)
    counter += 1
print("Limite de las integrales: ", limites)

#obtener limites inferiores y superiores
limites_superiores = limites[1::2]
limites_inferiores = limites[::2]
print("limites superiores: ", limites_superiores)
print("limites inferiores: ", limites_inferiores)


numeroDeBits = float(len(gt))
print("Numero de Bits: ", numeroDeBits)

bps = float(input("Ingrese bps"))
print("bps: ", bps)

anchoDeBanda = float(input("Ingrese el ancho de banda"))
print("Ancho de banda: ", anchoDeBanda)

frecuenciaFundamenta = float(bps / numeroDeBits)

numeroDeArmonicos = anchoDeBanda / frecuenciaFundamenta

print("Frecuencia fundamental: ", frecuenciaFundamenta)
print("numero de armonicos: ", numeroDeArmonicos)

# Componente de Voltaje Directo
numeroDeCeros = gt.count(0)
numeroDeUnos = numeroDeBits - numeroDeCeros
print("numero de ceros = ", numeroDeCeros)
print("numero de unos = ", numeroDeUnos)
dc = float(numeroDeUnos) / float(numeroDeBits)

print("dc = ", dc)

# Amplitud del Seno


def dar_base_an(n, limite_inferior, limite_superior):
    base: float = math.cos(0.25 * math.pi * n * limite_inferior) - math.cos(0.25 * math.pi * n * limite_superior)
    return base


def amplitud_del_seno(n):
    an: float = 0.0
    for i in range(0, len(limites_superiores)):
        an += (dar_base_an(n, limites_inferiores[i], limites_superiores[i]))
    an /= (math.pi*n)
    return an

# Amplitud del coseno


def dar_base_bn(n, limite_inferior, limite_superior):
    base: float = float(math.sin(0.25 * math.pi * n * limite_superior) - math.sin(0.25 * math.pi * n * limite_inferior))
    return base


def amplitud_del_cose(n):
    bn = 0.0
    for i in range(0, len(limites_superiores)):
        bn += (dar_base_bn(n, limites_inferiores[i], limites_superiores[i]))
    bn /= (math.pi * n)
    return bn


lista_cn: list = []
lista_angulon: list = []

print("n", "          ", "an", "          ", "bn", "          ", "cn", "          ", "On")

for n in range(1, int(numeroDeArmonicos)+1):

    if n == numeroDeBits:
        an = 0
        bn = 0
        cn = 0
        angulon = 0
    else:
        an = amplitud_del_seno(n)
        bn = amplitud_del_cose(n)
        cn = math.sqrt(an * an + bn * bn)
        angulon = math.atan(bn / an)
        if an<0:
            angulon += math.pi

    lista_cn.append(cn)
    lista_angulon.append(angulon)
    print(n, "    ", round(an, 6) , "    ", round(bn, 6) ,  "    ", round(cn, 6), "    ", round(angulon, 6))



##Hasta aqui todo bien


def dar_armonico(n, t):
    return lista_cn[n] * np.sin(2 * np.pi * (n+1) * frecuenciaFundamenta * t + lista_angulon[n])


tiempo = 1/300
step = 0.000001
lista_valores_y = []
lista_valores_x = []
for i in np.arange(0.0, tiempo, step):
    lista_valores_y.append(dar_armonico(1, i))
    lista_valores_x.append(i)






# make 3d axes
fig = plt.figure()
ax = fig.gca(projection='3d')

# Parametros

t = np.arange(0, 1/frecuenciaFundamenta, .000001)


def gt_final(t):
    result = dc + np.array([lista_cn[n] * np.sin(2*np.pi*(n+1)*frecuenciaFundamenta*t + lista_angulon[n]) for n in range(0, len(lista_cn), 1)]).sum()
    return result


gfinal = np.vectorize(gt_final)
n = []
for i in range(0, len(t)):
    n.append(0)
ax.plot(n, t, gfinal(t))

#por cada armonico
for armonico_numero in range(0, len(lista_cn), 1):
    n = []
    for i in range(0, len(t)):
        n.append(armonico_numero)
    z1 = np.vectorize(dar_armonico)
    ax.plot(n, t, z1(n, t))




# make labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()