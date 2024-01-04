from flask import Flask, render_template 
import math 
import random 
 
app = Flask(__name__) 
 
@app.route('/') 
def principal(): 
    return render_template("index.html") 
 
@app.route('/resultado') 
def resultado(): 
    coord = { 
        'Jiloyork': (19.916012, -99.580580), 
        'Toluca': (19.289165, -99.655697), 
        'Atlacomulco': (19.799520, -99.873844), 
        'Guadalajara': (20.677754472859146, -103.34625354877137), 
        'Monterrey': (25.69161110159454, -100.321838480256), 
        'QuintanaRoo': (21.163111924844458, -86.80231502121464), 
        'Michoacan': (19.701400113725654, -101.20829680213464), 
        'Aguascalientes': (21.87641043660486, -102.26438663286967), 
        'CDMX': (19.432713075976878, -99.13318344772986), 
        'QRO': (20.59719437542255, -100.38667040246602) 
    } 
 
    def distancia(coord1, coord2): 
        lat1 = coord1[0] 
        lon1 = coord1[1] 
        lat2 = coord2[0] 
        lon2 = coord2[1] 
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) 
 
    def evalua_ruta(ruta): 
        total = 0 
        for i in range(0, len(ruta) - 1): 
            ciudad1 = ruta[i] 
            ciudad2 = ruta[i + 1] 
            total = total + distancia(coord[ciudad1], coord[ciudad2]) 
        ciudad1 = ruta[i + 1] 
        ciudad2 = ruta[0] 
        total = total + distancia(coord[ciudad1], coord[ciudad2]) 
        return total 
 
    def simulated_annealing(ruta): 
        T = 20 
        T_MIN = 0 
        V_enfriamiento = 100 
 
        while T > T_MIN: 
            dist_actual = evalua_ruta(ruta) 
            for i in range(1, V_enfriamiento): 
                # Intercambios de dos ciudades aleatoriamente 
                i = random.randint(0, len(ruta) - 1) 
                j = random.randint(0, len(ruta) - 1) 
                ruta_tmp = ruta[:] 
                ciudad_tmp = ruta_tmp[i] 
                ruta_tmp[i] = ruta_tmp[j] 
                ruta_tmp[j] = ciudad_tmp 
                dist = evalua_ruta(ruta_tmp) 
                delta = dist_actual - dist 
                if dist < dist_actual or random.random() < math.exp(delta / T): 
                    ruta = ruta_tmp 
 
            # Enfriar a T linealmente 
            T = T - 0.005 
 
        return ruta 
 
    ruta = list(coord.keys())  # Crear una ruta inicial aleatoria 
    random.shuffle(ruta) 
    mejor_ruta = simulated_annealing(ruta) 
    distancia_total = evalua_ruta(mejor_ruta) 
     
    return render_template("resultado.html", mejor_ruta=mejor_ruta, distancia_total=distancia_total) 
 
if __name__ == "__main__": 
    app.run()