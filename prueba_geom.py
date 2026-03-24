import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np

# ==========================================
# 1. CONFIGURACIÓN EXACTA
# ==========================================
st.set_page_config(page_title="TFG: Geometría y Anti-Squat", layout="wide")
st.title("🏁 Dashboard TFG: Análisis Cinemático y Anti-Squat")

# ==========================================
# 2. PANEL DE CONTROL
# ==========================================
st.sidebar.header("⚙️ Setup de la Moto")

tab_chasis, tab_susp, tab_trans, tab_ruedas, tab_cdg = st.sidebar.tabs(["Chasis", "Suspensiones", "Transmisión", "Ruedas", "CDG"])

with tab_ruedas:
    st.markdown("**Neumático Delantero (Serie Moto3)**")
    w_f = st.number_input("Ancho (mm) Del.", value=90.0)
    p_f = st.number_input("Perfil (%) Del.", value=58.0)
    r_f = st.number_input("Llanta (Pulgadas) Del.", value=17.0)
    Df = (r_f * 25.4) + 2.0 * (w_f * (p_f / 100.0))
    st.info(f"Diámetro Calculado: {Df:.1f} mm")

    st.divider()
    st.markdown("**Neumático Trasero (Serie Moto3)**")
    w_r = st.number_input("Ancho (mm) Tras.", value=115.0)
    p_r = st.number_input("Perfil (%) Tras.", value=75.0)
    r_r = st.number_input("Llanta (Pulgadas) Tras.", value=17.0)
    Dr = (r_r * 25.4) + 2.0 * (w_r * (p_r / 100.0))
    st.info(f"Diámetro Calculado: {Dr:.1f} mm")

with tab_chasis:
    metodo_chasis = st.radio(
        "Definición del Chasis:",
        ["A: Comercial (Wheelbase, Rake)", "B: Geometría Rígida Pura (Cinta Métrica)"],
        index=1
    )
    st.divider()
    
    if metodo_chasis == "A: Comercial (Wheelbase, Rake)":
        st.info("Método A: El chasis se congrega rígidamente usando cotas de catálogo y rotará libremente en el espacio.")
        p_estatica_input = st.number_input("Batalla Comercial (Ficha Técnica)", value=1263.5, format="%.1f")
        L_basc_ficha = st.number_input("Basculante Comercial (Ficha Técnica)", value=561.5, format="%.1f")
        ang_lanz_input = st.number_input("Ángulo Rake Base", value=22.19, format="%.2f")
        L_pipa_input = st.number_input("Longitud Pipa Dirección", value=139.0, format="%.1f")
        
        st.divider()
        d_offset = st.number_input("Offset Tijas", value=33.5, format="%.1f")
        grosor_tija = st.number_input("Grosor Tija Superior", value=19.5, format="%.1f")
        
        st.markdown("**Anclajes Traseros (Coords Clásicas Locales)**")
        H_amort = st.number_input("Y Pivot a Amortiguador Sup.", value=124.17, format="%.2f")
        d_amort = st.number_input("X Soporte Amortiguador (d_amort)", value=50.44, format="%.2f")
        H_link = st.number_input("Y Pivot a Bieleta", value=-132.09, format="%.2f")
        d_link = st.number_input("X Soporte Bieleta (d_link)", value=10.42, format="%.2f")
    else:
        st.info("Top-Down Puro (Goma Métrica): El chasis flota antes de auto-equilibrarse en el asfalto por gravedad.")
        L_pipa_input = st.number_input("Longitud Pipa Dirección", value=139)
        d_piv_top = st.number_input("Distancia barra PIVOT a Pipa SUPERIOR", value=593.05)
        d_piv_bot = st.number_input("Distancia barra PIVOT a Pipa INFERIOR", value=568.022, format="%.3f")

        st.divider()
        d_offset = st.number_input("Offset Tijas", value=33.5)
        grosor_tija = st.number_input("Grosor Tija Superior", value=19.5)
        
        st.markdown("**Anclajes Traseros (Multilateración)**")
        d_piv_amort = st.number_input("Distancia PIVOT a Soporte AMORT.", value=134.02, format="%.3f")
        d_top_amort = st.number_input("Distancia Pipa SUP a Soporte AMORT.", value=563.94, format="%.3f")
        d_piv_link = st.number_input("Distancia PIVOT a Soporte BIELETA", value=132.5, format="%.3f")
        d_bot_link = st.number_input("Distancia Pipa INF a Soporte BIELETA", value=648.135, format="%.3f")
        
        st.info("Cota de Cierre (Evita Inversiones)")
        d_amort_link = st.number_input("Distancia AMORTIGUADOR a BIELETA", value=259.361, format="%.3f")

    st.markdown("**Anclajes en el Basculante (Rocker Pivot)**")
    l_basc_piv = st.number_input("X Pivot a Anclaje Bieleta en Basc.", value=170.0)
    h_basc_piv = st.number_input("Y Pivot a Anclaje Bieleta en Basc.", value=46.0)

    st.markdown("**Geometría de Bieletas (Rocker y Tirante)**")
    L_link = st.number_input("Longitud del Tirante (Pullrod)", value=168.0)
    d_t_ba = st.number_input("Triángulo: Basc. a Amortiguador", value=115.0)
    d_t_bl = st.number_input("Triángulo: Basc. a Tirante", value=68.0)
    d_t_la = st.number_input("Triángulo: Tirante a Amortiguador", value=95.5)
    flip_rocker = st.checkbox("Orientación de Bieleta Inversa", value=False)
with tab_susp:
    L_horq_ext = st.number_input("Longitud Horquilla Ext. Total", value=625.0)
    L_amort_ext = st.number_input("Longitud Amortiguador Ext.", value=314.0)
    
    st.markdown("**Ajuste en Tijas (Setup Pista)**")
    deslizamiento_horquilla = st.slider("Deslizar Horquilla en Tija (mm)", 0.0, 100.0, 0.0, help="La horquilla sobresale esto por encima de la tija. El chasis base se calcula con 0.")
    
    st.divider()
    recorrido_max_horq = st.number_input("Recorrido Máx. Horquilla", value=120.0)
    c_horq = st.slider("COMPRESIÓN HORQUILLA (mm)", 0.0, float(recorrido_max_horq), 0.0)
    
    recorrido_max_amort = st.number_input("Recorrido Máx. Amortiguador", value=60.0)
    c_amort = st.slider("COMPRESIÓN AMORTIGUADOR (mm)", 0.0, float(recorrido_max_amort), 0.0)

with tab_cdg:
    st.markdown("**Cálculo de Centro de Gravedad (CDG)**")
    modo_cdg = st.radio("Modo de Integración:", ["Calculado (Moto + Piloto)", "Aporte Manual Combinado"])
    
    if modo_cdg == "Aporte Manual Combinado":
        masa_total = st.number_input("Masa Total (kg)", value=145.0)
        d_cdg = st.number_input("X Pivot a CDG (Horizontal)", value=150.0) 
        h_cdg = st.number_input("Y Pivot a CDG (Vertical)", value=135.0)
    else:
        st.markdown("**🔹 Vehículo**")
        peso_moto = st.number_input("Peso Moto (kg)", value=85.0)
        x_moto = st.number_input("X Pivot a CDG Moto", value=200.0)
        y_moto = st.number_input("Y Pivot a CDG Moto", value=150.0)
        
        st.markdown("**🔹 Piloto**")
        peso_piloto = st.number_input("Peso Piloto (kg)", value=60.0)
        x_piloto = st.number_input("X Pivot a CDG Piloto", value=80.0)
        y_piloto = st.number_input("Y Pivot a CDG Piloto", value=450.0)

        masa_total = peso_moto + peso_piloto
        st.info(f"Masa Conjunto: {masa_total} kg")
        
        d_cdg = (peso_moto * x_moto + peso_piloto * x_piloto) / masa_total if masa_total > 0 else 0
        h_cdg = (peso_moto * y_moto + peso_piloto * y_piloto) / masa_total if masa_total > 0 else 0
        
        st.success(f"CDG Combinado Calculado:\n**X: {d_cdg:.1f} mm &nbsp;|&nbsp; Y: {h_cdg:.1f} mm**")

with tab_trans:
    
    st.divider()
    st.markdown("**Sistema de Transmisión (Desarrollos y Cadena)**")
    d_pinon = st.number_input("X Pivot a Piñón", value=85.0) 
    h_pinon = st.number_input("Y Pivot a Piñón", value=5.0)  
    
    tipo_cadena = st.selectbox("Paso de Cadena", ["520", "525", "530", "428", "415"], index=4)
    pitch_mm = 15.875 if tipo_cadena in ["520", "525", "530"] else 12.7  
    Z_pinon = st.number_input("Dientes Piñón (Z)", value=15, step=1)
    Z_corona = st.number_input("Dientes Corona (Z)", value=45, step=1)
    
    L_basc_min = st.number_input("Rango Basculante MÍNIMO (mm)", value=560.0)
    L_basc_max = st.number_input("Rango Basculante MÁXIMO (mm)", value=595.0)

# ==========================================
# 3. MOTOR CINEMÁTICO RÍGIDO (BASE A 0mm)
# ==========================================
radio_del = Df / 2
radio_tras = Dr / 2

def intersect_circles(p0, r0, p1, r1, pick_highest_y=False, pick_highest_x=False, pick_lowest_x=False):
    d = np.linalg.norm(p1 - p0)
    if d == 0: return None
    
    # Soft limits para evitar que desaparezca si la geometria se rompe
    if d > (r0 + r1): d = r0 + r1 - 0.001
    elif d < abs(r0 - r1): d = abs(r0 - r1) + 0.001
        
    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h = math.sqrt(abs(r0**2 - a**2))
    p2 = p0 + a * (p1 - p0) / d # type: ignore
    p3_1 = np.array([p2[0] + h * (p1[1] - p0[1]) / d, p2[1] - h * (p1[0] - p0[0]) / d])
    p3_2 = np.array([p2[0] - h * (p1[1] - p0[1]) / d, p2[1] + h * (p1[0] - p0[0]) / d])
    
    if pick_highest_x: return p3_1 if p3_1[0] > p3_2[0] else p3_2
    if pick_lowest_x: return p3_1 if p3_1[0] < p3_2[0] else p3_2
    if pick_highest_y: return p3_1 if p3_1[1] > p3_2[1] else p3_2
    return p3_1 if p3_1[1] < p3_2[1] else p3_2

def intersect_circles_all(p0, r0, p1, r1):
    d = np.linalg.norm(p1 - p0)
    if d == 0: return None, None
    if d > (r0 + r1): d = r0 + r1 - 0.001
    elif d < abs(r0 - r1): d = abs(r0 - r1) + 0.001
    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h = math.sqrt(abs(r0**2 - a**2))
    p2 = p0 + a * (p1 - p0) / d # type: ignore
    p3_1 = np.array([p2[0] + h * (p1[1] - p0[1]) / d, p2[1] - h * (p1[0] - p0[0]) / d])
    p3_2 = np.array([p2[0] - h * (p1[1] - p0[1]) / d, p2[1] + h * (p1[0] - p0[0]) / d])
    return p3_1, p3_2

# ==========================================
# CONSTRUCCIÓN RÍGIDA DEL ANCLAJE TRASERO PARA CADENA
# ==========================================
Pivot_local = np.array([0.0, 0.0])

if metodo_chasis == "A: Comercial (Wheelbase, Rake)":
    F_Amort_local = np.array([-float(d_amort), float(H_amort)])
    F_Link_local = np.array([-float(d_link), float(H_link)])
else:
    bot_pipa_tmp = np.array([d_piv_bot, 0.0])
    top_pipa_tmp = intersect_circles(Pivot_local, d_piv_top, bot_pipa_tmp, L_pipa_input, pick_highest_y=True)
    if top_pipa_tmp is None:
        st.error("❌ Geometría de Pipa rota.")
        st.stop()
        top_pipa_tmp = np.array([0.,0.])

    # NORMALIZACIÓN AL HORIZONTE TEMPRANA
    v_pipa_ini = top_pipa_tmp - bot_pipa_tmp
    ang_actual = math.atan2(v_pipa_ini[1], v_pipa_ini[0])
    # Forzamos la Pipa a mirar hacia atrás (114º) para que el solver local asiente el chasis a derechas
    theta_norm = math.radians(114.0) - ang_actual
    
    mat_norm = np.array([
        [math.cos(theta_norm), -math.sin(theta_norm)],
        [math.sin(theta_norm),  math.cos(theta_norm)]
    ])

    top_pipa_local_B = np.dot(mat_norm, top_pipa_tmp)
    bot_pipa_local_B = np.dot(mat_norm, bot_pipa_tmp)

    # Buscar anclajes traseros en el chasis ya levantado para que 'menor X' siempre mire hacia atrás físicamente
    opt_a1, opt_a2 = intersect_circles_all(Pivot_local, d_piv_amort, top_pipa_local_B, d_top_amort)
    opt_b1, opt_b2 = intersect_circles_all(Pivot_local, d_piv_link, bot_pipa_local_B, d_bot_link)

    best_pair = None
    min_error = float('inf')
    best_x_amort = float('inf')

    for a in [opt_a1, opt_a2]:
        for b in [opt_b1, opt_b2]:
            if a is not None and b is not None:
                dist = np.linalg.norm(a - b)
                err = abs(dist - d_amort_link)
                # Tolerancia de 1.5mm para identificar si hay un "espejo" en competición
                if err < min_error - 1.5:
                    min_error = err
                    best_pair = (a, b)
                    best_x_amort = a[0]
                elif abs(err - min_error) <= 1.5:
                    # En caso de espejo geométrico paramétrico, obligamos a que el amortiguador vaya HACIA ATRÁS (menor X)
                    if a[0] < best_x_amort:
                        best_pair = (a, b)
                        best_x_amort = a[0]

    if best_pair is None:
        st.error("❌ Triángulos de anclaje trasero no pueden cerrarse.")
        st.stop()
        F_Amort_local = np.array([0.,0.])
        F_Link_local = np.array([0.,0.])
    else:
        F_Amort_local, F_Link_local = best_pair
        if min_error > 2.0:
            st.warning(f"⚠️ Aviso: La Cota de Cierre real difiere del modelo matemático en {min_error:.1f} mm.")

# ==========================================
# SOLVER DE CADENA PARA RECUPERAR L_basc
# ==========================================
def evaluar_amort_for_lbasc(Ry, lbasc_test):
    Rx = -math.sqrt(max(0, lbasc_test**2 - Ry**2))
    vp = np.array([Rx, Ry])
    vu = vp / max(1.0, np.linalg.norm(vp))
    vperp = np.array([-vu[1], vu[0]])
    
    sr = l_basc_piv * vu + h_basc_piv * vperp
    rl = intersect_circles(F_Link_local, L_link, sr, d_t_bl, pick_highest_y=flip_rocker)
    if rl is None: return None
    ra = intersect_circles(sr, d_t_ba, rl, d_t_la, pick_highest_x=True)
    if ra is None: return None
    return np.linalg.norm(ra - F_Amort_local)

def resolver_Ry_for_lbasc(L_target, lbasc_test):
    low, high = -lbasc_test + 1, lbasc_test / 2.0
    for _ in range(40):
        mid = (low + high) / 2.0
        L_mid = evaluar_amort_for_lbasc(mid, lbasc_test)
        if L_mid is None: break
        if L_mid < L_target: high = mid
        else: low = mid
    return (low + high) / 2.0

def get_links_for_lbasc(lbasc_test):
    ry = resolver_Ry_for_lbasc(L_amort_ext, lbasc_test)
    rx = -math.sqrt(max(0, lbasc_test**2 - ry**2))
    c_dist = math.sqrt((rx - d_pinon)**2 + (ry - h_pinon)**2)
    return (Z_corona + Z_pinon) / 2.0 + (2 * c_dist) / pitch_mm + ((Z_corona - Z_pinon)/(2*math.pi))**2 * (pitch_mm / c_dist)

links_min = get_links_for_lbasc(L_basc_min)
links_max = get_links_for_lbasc(L_basc_max)
if links_min > links_max: links_min, links_max = links_max, links_min

l_min_even = math.ceil(links_min / 2.0) * 2
l_max_even = math.floor(links_max / 2.0) * 2

valid_configs = []
def calc_C_from_links(L_esl):
    t1 = 2 * L_esl - Z_corona - Z_pinon
    t2 = t1**2 - (8 / (math.pi**2)) * (Z_corona - Z_pinon)**2
    if t2 < 0: return None
    return (pitch_mm / 8.0) * (t1 + math.sqrt(t2))

for L_esl in range(int(l_min_even), int(l_max_even) + 2, 2):
    C_req = calc_C_from_links(L_esl)
    if C_req is None: continue
    l_bajo = min(L_basc_min, L_basc_max)
    l_alto = max(L_basc_min, L_basc_max)
    for _ in range(30):
        l_medio = (l_bajo + l_alto) / 2.0
        ry_m = resolver_Ry_for_lbasc(L_amort_ext, l_medio) # type: ignore
        rx_m = -math.sqrt(max(0, l_medio**2 - ry_m**2))
        c_m = math.sqrt((rx_m - d_pinon)**2 + (ry_m - h_pinon)**2)
        if c_m < C_req: l_bajo = l_medio
        else: l_alto = l_medio
    valid_configs.append((L_esl, (l_bajo + l_alto)/2.0)) # type: ignore

with tab_trans:
    if len(valid_configs) > 0:
        opciones_str = [f"{cfg[0]} Eslabones (L_basc = {cfg[1]:.1f} mm)" for cfg in valid_configs]
        seleccion_str = st.radio("Ajuste de Cadena y Batalla:", opciones_str)
        idx = opciones_str.index(seleccion_str)
        L_basc = valid_configs[idx][1]
    else:
        st.warning("⚠️ El rango del basculante no permite ajustar eslabones pares enteros.")
        L_basc = (L_basc_min + L_basc_max) / 2.0

radio_pinon = pitch_mm / (2 * math.sin(math.pi / Z_pinon))
radio_corona = pitch_mm / (2 * math.sin(math.pi / Z_corona))

def evaluar_amortiguador(Ry):
    Rx = -math.sqrt(max(0, L_basc**2 - Ry**2))
    vp = np.array([Rx, Ry])
    vu = vp / max(1.0, np.linalg.norm(vp))
    vperp = np.array([-vu[1], vu[0]])
    sr = l_basc_piv * vu + h_basc_piv * vperp
    rl = intersect_circles(F_Link_local, L_link, sr, d_t_bl, pick_highest_y=flip_rocker)
    if rl is None: return None
    ra = intersect_circles(sr, d_t_ba, rl, d_t_la, pick_highest_x=True)
    if ra is None: return None
    return np.linalg.norm(ra - F_Amort_local)

def resolver_Ry(L_target):
    low, high = -L_basc + 1, L_basc / 2.0
    for _ in range(40):
        mid = (low + high) / 2.0
        L_mid = evaluar_amortiguador(mid) # type: ignore
        if L_mid is None: break
        if L_mid < L_target: high = mid
        else: low = mid
    return (low + high) / 2.0

# ==========================================
# CONSTRUCCIÓN TUBULAR DEL TREN FRONTAL
# ==========================================
if metodo_chasis == "A: Comercial (Wheelbase, Rake)":
    # Base inamovible matemática que define la estructura
    y_ficha = resolver_Ry_for_lbasc(L_amort_ext, L_basc_ficha) # type: ignore
    x_ficha = -math.sqrt(max(0, L_basc_ficha**2 - y_ficha**2))
    h_piv_ficha = radio_tras - y_ficha
    
    rake_rad_stat = math.radians(ang_lanz_input)
    v_up_local = np.array([-math.sin(rake_rad_stat), math.cos(rake_rad_stat)])
    v_fwd_local = np.array([math.cos(rake_rad_stat), math.sin(rake_rad_stat)])
    
    eje_d_ficha = np.array([x_ficha + p_estatica_input, radio_del - h_piv_ficha])
    tija_sup_face_stat = eje_d_ficha + L_horq_ext * v_up_local
    tija_base_stat = tija_sup_face_stat - grosor_tija * v_up_local
    top_pipa_local = tija_base_stat - d_offset * v_fwd_local
    bot_pipa_local = top_pipa_local - L_pipa_input * v_up_local
    
    chasis_sup_local = np.array([0, float(H_amort)])
    chasis_inf_local = np.array([0, float(H_link)])
else:
    top_pipa_local = top_pipa_local_B
    bot_pipa_local = bot_pipa_local_B
    
    dx_pipa = bot_pipa_local[0] - top_pipa_local[0] # type: ignore
    dy_pipa = top_pipa_local[1] - bot_pipa_local[1] # type: ignore
    ang_pipa_local = math.atan2(float(dx_pipa), float(dy_pipa))
    
    v_up_local = np.array([-math.sin(ang_pipa_local), math.cos(ang_pipa_local)])
    v_fwd_local = np.array([math.cos(ang_pipa_local), math.sin(ang_pipa_local)])
    
    tija_base_stat = top_pipa_local + d_offset * v_fwd_local
    tija_sup_face_stat = tija_base_stat + grosor_tija * v_up_local
    
    chasis_sup_local = np.array([0, float(F_Amort_local[1])]) # type: ignore
    chasis_inf_local = np.array([0, float(F_Link_local[1])]) # type: ignore

v_up = v_up_local # Alias para la Fase 9
centro_pipa_local = (top_pipa_local + bot_pipa_local) / 2 # type: ignore

# ==========================================
# PRE-ENSAMBLAJE CINEMÁTICO REAL LOCAL
# ==========================================
eje_t_y_stat = resolver_Ry(L_amort_ext)
h_pivot = radio_tras - eje_t_y_stat
eje_t_x_stat = -math.sqrt(max(0, L_basc**2 - eje_t_y_stat**2))
R_local = np.array([eje_t_x_stat, eje_t_y_stat])

sup_amort_local = F_Amort_local
inf_biel_local = F_Link_local

# ==========================================
# CÁLCULO DE COMPRESIONES
# ==========================================
top_fork_local = tija_sup_face_stat + deslizamiento_horquilla * v_up_local

L_horq_comp = L_horq_ext - c_horq
F_local = top_fork_local - L_horq_comp * v_up_local

Ry_comp = resolver_Ry(L_amort_ext - c_amort)
Rx_comp = -math.sqrt(max(0, L_basc**2 - Ry_comp**2))
R_local_comp = np.array([Rx_comp, Ry_comp])

F_local_stat = top_fork_local - L_horq_ext * v_up_local

# ==========================================
# ROTACIÓN GLOBAL HACIA EL SUELO (EL MILAGRO FÍSICO)
# ==========================================
delta_x = F_local[0] - R_local_comp[0] # type: ignore
delta_y = F_local[1] - R_local_comp[1] # type: ignore
p_dinamico = math.sqrt(delta_x**2 + delta_y**2)

gamma_local = math.atan2(delta_y, delta_x)
gamma_target = math.asin((radio_del - radio_tras) / p_dinamico)
theta = gamma_target - gamma_local
pitch_grados = math.degrees(theta)

ds_x = F_local_stat[0] - R_local[0] # type: ignore
ds_y = F_local_stat[1] - R_local[1] # type: ignore
p_estatica = math.sqrt(ds_x**2 + ds_y**2)

matriz_rot = np.array([
    [math.cos(theta), -math.sin(theta)],
    [math.sin(theta),  math.cos(theta)]
])

# Rotación al plano mundial
Pivot_world = np.array([0, 0])
R_world = np.dot(matriz_rot, R_local_comp)
F_world = np.dot(matriz_rot, F_local)
top_pipa_world = np.dot(matriz_rot, top_pipa_local)
bot_pipa_world = np.dot(matriz_rot, bot_pipa_local)
centro_pipa_world = np.dot(matriz_rot, centro_pipa_local)
tija_sup_face_world = np.dot(matriz_rot, tija_sup_face_stat)
tija_base_world = np.dot(matriz_rot, tija_base_stat)
top_fork_world = np.dot(matriz_rot, top_fork_local)

sup_amort_world = np.dot(matriz_rot, sup_amort_local)
inf_biel_world = np.dot(matriz_rot, inf_biel_local)
chasis_sup_world = np.dot(matriz_rot, chasis_sup_local)
chasis_inf_world = np.dot(matriz_rot, chasis_inf_local)

# --- SISTEMA DE BIELETAS TRASERO ---
v_basc = R_world - Pivot_world
v_basc_unit = v_basc / max(1.0, np.linalg.norm(v_basc))
v_basc_perp = np.array([-v_basc_unit[1], v_basc_unit[0]]) 
# Sumamos el vector perpendicular para asegurar que ancla POR DEBAJO del basculante
swingarm_mount_base = Pivot_world + l_basc_piv * v_basc_unit
rocker_pivot_world = swingarm_mount_base + h_basc_piv * v_basc_perp

rocker_L_world = intersect_circles(inf_biel_world, L_link, rocker_pivot_world, d_t_bl, pick_highest_y=flip_rocker)

if rocker_L_world is not None:
    # Seleccionamos highest_x = True para forzar que el amortiguador caiga por delante del triángulo
    rocker_A_world = intersect_circles(rocker_pivot_world, d_t_ba, rocker_L_world, d_t_la, pick_highest_x=True)
else:
    rocker_A_world = None

suelo_y = R_world[1] - radio_tras

# Rake Vector tras rotación
v_up_world = np.dot(matriz_rot, v_up_local)
rake_din_rad = math.atan2(-v_up_world[0], v_up_world[1])
ang_lanz_dinamico = math.degrees(rake_din_rad)

# Trail
distancia_y_al_suelo = centro_pipa_world[1] - suelo_y
steer_ground_x = centro_pipa_world[0] + (distancia_y_al_suelo * math.tan(rake_din_rad))
trail_real = steer_ground_x - F_world[0]
angulo_basc = math.degrees(math.asin(abs(R_world[1] - suelo_y - radio_tras) / L_basc))

# --- FASE 4: TRANSMISIÓN ---
cdg_world = np.dot(matriz_rot, np.array([d_cdg, h_cdg]))
pinon_world = np.dot(matriz_rot, np.array([d_pinon, h_pinon]))
corona_world = R_world

v_centros = pinon_world - corona_world
dist_centros = max(1.0, np.linalg.norm(v_centros)) 
angulo_centros = math.atan2(v_centros[1], v_centros[0])
angulo_tangente = math.asin((radio_corona - radio_pinon) / dist_centros)
angulo_top = angulo_centros + (math.pi / 2) - angulo_tangente
angulo_bot = angulo_centros - (math.pi / 2) + angulo_tangente

top_corona = corona_world + np.array([radio_corona * math.cos(angulo_top), radio_corona * math.sin(angulo_top)])
top_pinon = pinon_world + np.array([radio_pinon * math.cos(angulo_top), radio_pinon * math.sin(angulo_top)])

bot_corona = corona_world + np.array([radio_corona * math.cos(angulo_bot), radio_corona * math.sin(angulo_bot)])
bot_pinon = pinon_world + np.array([radio_pinon * math.cos(angulo_bot), radio_pinon * math.sin(angulo_bot)])

# ==========================================
# 5. ANÁLISIS DE ANTI-SQUAT EXACTO
# ==========================================
v_tiro = top_pinon - top_corona
v_tiro_norm = v_tiro / np.linalg.norm(v_tiro)
p2_cadena = top_pinon + v_tiro_norm * 5000 

v_basc = Pivot_world - R_world
v_basc_norm = v_basc / np.linalg.norm(v_basc)
p2_basc = Pivot_world + v_basc_norm * 5000

def get_intersection(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = p3; x4, y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    return np.array([x1 + ua*(x2-x1), y1 + ua*(y2-y1)])

ic_point = get_intersection(top_corona, p2_cadena, R_world, p2_basc)

contacto_trasero_x = R_world[0]
contacto_trasero_y = suelo_y

if ic_point is not None:
    dist_ic_x = ic_point[0] - contacto_trasero_x
    dist_cdg_x = cdg_world[0] - contacto_trasero_x
    
    slope_ic = (ic_point[1] - suelo_y) / dist_ic_x if dist_ic_x != 0 else 0
    slope_cdg = (cdg_world[1] - suelo_y) / dist_cdg_x if dist_cdg_x != 0 else 0.0001
    
    percent_antisquat = (slope_ic / slope_cdg) * 100
    angulo_antisquat = math.degrees(math.atan(slope_ic))
    
    y_prolongada_as = contacto_trasero_y + slope_ic * dist_cdg_x
else:
    percent_antisquat = 0.0
    angulo_antisquat = 0.0
    y_prolongada_as = contacto_trasero_y

# ==========================================
# 6. DASHBOARD Y RESULTADOS
# ==========================================
if rocker_L_world is not None and rocker_A_world is not None:
    L_amort_actual = np.linalg.norm(rocker_A_world - sup_amort_world)
    compresion_real = L_amort_ext - L_amort_actual
else:
    L_amort_actual = 0.0
    compresion_real = 0.0

recorrido_rueda = R_local_comp[1] - R_local[1]
motion_ratio = recorrido_rueda / c_amort if c_amort > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Rake Din.", f"{ang_lanz_dinamico:.2f} °", f"{pitch_grados:+.2f}° Pitch", delta_color="inverse")
col2.metric("Trail", f"{trail_real:.1f} mm")
delta_p = p_dinamico - p_estatica
col3.metric("Dist. Ejes", f"{p_dinamico:.1f} mm", f"{delta_p:+.1f} mm", delta_color="off")
col4.metric("% Anti-Squat", f"{percent_antisquat:.1f} %") 
col5.metric("Ángulo A-S", f"{angulo_antisquat:.2f} °")

st.markdown("##### Cinemática de Suspensión Trasera")
c1, c2, c3, c4 = st.columns(4)
c1.metric("h_pivot (Geométrico)", f"{h_pivot:.1f} mm", "1G Solver", delta_color="off")
c2.metric("L. Amortiguador", f"{L_amort_actual:.1f} mm", f"{-compresion_real:.1f} mm compresión", delta_color="inverse")
c3.metric("Recorrido Rueda (Eje Y)", f"{recorrido_rueda:.1f} mm", f"vs {c_amort:.1f} mm Amort.", delta_color="off")
c4.metric("Motion Ratio (Rueda/Amort)", f"{motion_ratio:.2f}")

st.divider()

# ==========================================
# 7. GRÁFICO TÉCNICO ALTA PRECISIÓN
# ==========================================
fig, ax = plt.subplots(figsize=(14, 7))

# ENCUADRE DINÁMICO
margen_x = 400
ax.set_xlim(R_world[0] - margen_x, F_world[0] + margen_x)

altura_maxima = max(tija_sup_face_world[1], top_pipa_world[1], cdg_world[1])
ax.set_ylim(suelo_y - 0, altura_maxima + 120)

# Suelo y ruedas
ax.axhline(suelo_y, color='black', lw=1.0)
ax.add_patch(plt.Circle((R_world[0], R_world[1]), radio_tras, color='gray', fill=False, ls='solid', lw=1.0))
ax.add_patch(plt.Circle((F_world[0], F_world[1]), radio_del, color='gray', fill=False, ls='solid', lw=1.0))

# Chasis (Inamovible)
# Eje estructural principal (X=0 en local)
ax.plot([0, chasis_sup_world[0]], [0, chasis_sup_world[1]], color='navy', lw=1.0)
ax.plot([0, chasis_inf_world[0]], [0, chasis_inf_world[1]], color='navy', lw=1.0)
ax.plot([centro_pipa_world[0], chasis_sup_world[0]], [centro_pipa_world[1], chasis_sup_world[1]], color='navy', lw=1.0)
ax.plot([centro_pipa_world[0], chasis_inf_world[0]], [centro_pipa_world[1], chasis_inf_world[1]], color='navy', lw=1.0)

# Soportes perpendiculares (hacia amortiguador y bieleta)
ax.plot([chasis_sup_world[0], sup_amort_world[0]], [chasis_sup_world[1], sup_amort_world[1]], color='navy', lw=1.0)
ax.plot([chasis_inf_world[0], inf_biel_world[0]], [chasis_inf_world[1], inf_biel_world[1]], color='navy', lw=1.0)
ax.plot([bot_pipa_world[0], top_pipa_world[0]], [bot_pipa_world[1], top_pipa_world[1]], color='navy', lw=1.0, solid_capstyle='butt')

tija_x = [top_pipa_world[0], tija_base_world[0], tija_sup_face_world[0], top_pipa_world[0] + (tija_sup_face_world[0]-tija_base_world[0]), top_pipa_world[0]]
tija_y = [top_pipa_world[1], tija_base_world[1], tija_sup_face_world[1], top_pipa_world[1] + (tija_sup_face_world[1]-tija_base_world[1]), top_pipa_world[1]]
ax.plot(tija_x, tija_y, color='navy', lw=1.0)

# Suspensión y Basculante
ax.plot([F_world[0], top_fork_world[0]], [F_world[1], top_fork_world[1]], color='green', lw=1.0) 
ax.plot([R_world[0], Pivot_world[0]], [R_world[1], Pivot_world[1]], color='red', lw=1.0)

# Soporte perpendicular del basculante a la bieleta
ax.plot([swingarm_mount_base[0], rocker_pivot_world[0]], [swingarm_mount_base[1], rocker_pivot_world[1]], color='red', lw=1.0)

if rocker_L_world is not None and rocker_A_world is not None:
    # Tirante (Pullrod)
    ax.plot([inf_biel_world[0], rocker_L_world[0]], [inf_biel_world[1], rocker_L_world[1]], color='cyan', lw=1.0, zorder=4)
    # Amortiguador trasero
    ax.plot([sup_amort_world[0], rocker_A_world[0]], [sup_amort_world[1], rocker_A_world[1]], color='yellow', lw=1.0, zorder=3)
    # Triángulo Bieleta (Rocker)
    rx = [rocker_pivot_world[0], rocker_L_world[0], rocker_A_world[0], rocker_pivot_world[0]]
    ry = [rocker_pivot_world[1], rocker_L_world[1], rocker_A_world[1], rocker_pivot_world[1]]
    ax.fill(rx, ry, color='blue', alpha=0.3, zorder=5)
    ax.plot(rx, ry, color='cyan', lw=1.0, zorder=5)

# Transmisión y Cadena Física
ax.plot(cdg_world[0], cdg_world[1], marker='+', color='orange', markersize=10, label='C.D.G.')
ax.add_patch(plt.Circle((pinon_world[0], pinon_world[1]), radio_pinon, color='goldenrod', fill=False, lw=1.0))
ax.add_patch(plt.Circle((corona_world[0], corona_world[1]), radio_corona, color='goldenrod', fill=False, lw=1.0))

ax.plot([top_corona[0], top_pinon[0]], [top_corona[1], top_pinon[1]], color='goldenrod', lw=1.0, label='Cadena Fija')
ax.plot([bot_corona[0], bot_pinon[0]], [bot_corona[1], bot_pinon[1]], color='goldenrod', lw=1.0)

# --- GEOMETRÍA DIRECCIÓN (RAKE Y TRAIL) ---
# Eje de dirección
ax.plot([centro_pipa_world[0], steer_ground_x], [centro_pipa_world[1], suelo_y], color='purple', ls='-.', lw=1.0, label='Eje Dirección')

# Trail (Elevamos la cota 45 mm del suelo para que la línea negra no lo tape)
y_cota = suelo_y + 45
ax.plot([F_world[0], F_world[0]], [suelo_y, y_cota + 15], color='purple', ls=':', lw=1.0)
ax.plot([steer_ground_x, steer_ground_x], [suelo_y, y_cota + 15], color='purple', ls=':', lw=1.0)
ax.plot([F_world[0], steer_ground_x], [y_cota, y_cota], color='purple', lw=1.0, label='Cota Trail')
ax.plot([F_world[0], F_world[0]], [y_cota - 15, y_cota + 15], color='purple', lw=1.0)
ax.plot([steer_ground_x, steer_ground_x], [y_cota - 15, y_cota + 15], color='purple', lw=1.0)

# Dibujo del Ángulo de Rake en el suelo
ax.plot([steer_ground_x, steer_ground_x], [suelo_y, suelo_y + 300], color='purple', ls=':', lw=1.0, label='Vertical Rake')
radio_arco = 200.0
theta_vals = np.linspace(math.pi/2, math.pi/2 + rake_din_rad, 20)
arc_x = steer_ground_x + radio_arco * np.cos(theta_vals)
arc_y = suelo_y + radio_arco * np.sin(theta_vals)
ax.plot(arc_x, arc_y, color='purple', lw=1.0)

# --- ANÁLISIS ANTI-SQUAT ---
if ic_point is not None:
    # Proyección punteada anti-squat solo desde el piñón
    ax.plot([top_pinon[0], ic_point[0]], [top_pinon[1], ic_point[1]], color='goldenrod', ls='--', lw=1.0, label='Tiro (Anti-Squat)')
    ax.plot([R_world[0], ic_point[0]], [R_world[1], ic_point[1]], color='red', ls='--', lw=1.0, label='Línea Basculante')
    ax.plot(ic_point[0], ic_point[1], 'mx', markersize=8, label='Instant Center')
    
    ax.plot([contacto_trasero_x, ic_point[0]], [contacto_trasero_y, ic_point[1]], color='magenta', ls='--', lw=1.0, label='Línea Anti-Squat')
    
    ax.plot([contacto_trasero_x, cdg_world[0]], [contacto_trasero_y, cdg_world[1]], color='gray', ls=':', lw=1.0, label='100% Anti-Squat')
    ax.plot([cdg_world[0], cdg_world[0]], [suelo_y, cdg_world[1]], color='gray', ls=':', lw=1.0)
    ax.plot(cdg_world[0], y_prolongada_as, 'mo', markersize=4) 
else:
    ax.plot([top_pinon[0], p2_cadena[0]], [top_pinon[1], p2_cadena[1]], color='goldenrod', ls='--', lw=1.0)
    ax.plot([R_world[0], p2_basc[0]], [R_world[1], p2_basc[1]], color='red', ls='--', lw=1.0)

ax.plot(0, 0, 'ko', markersize=3)
ax.set_aspect('equal')
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.4)

st.pyplot(fig)

# ==========================================
# 8. GRÁFICO MOTION RATIO (OPCIONAL)
# ==========================================
st.divider()
if st.checkbox("Analizar Curva de Motion Ratio (Progresividad)", value=False):
    st.subheader("Curva de Progresividad (Motion Ratio Instantáneo)")
    
    # Calculamos la cinemática para todo el recorrido del amortiguador
    pasos = 60
    compresiones = np.linspace(0, recorrido_max_amort, pasos)
    recorridos_rueda_array = []
    
    for c in compresiones:
        ry_test = resolver_Ry(L_amort_ext - c)
        if ry_test is not None:
            recorridos_rueda_array.append(ry_test - eje_t_y_stat) # type: ignore
        else:
            # Tolerancia por si el solver no convergió al tope de compresión
            recorridos_rueda_array.append(recorridos_rueda_array[-1] if len(recorridos_rueda_array)>0 else 0)
            
    # MR Instantáneo (derivada: ΔRueda / ΔAmortiguador)
    mr_inst = np.gradient(recorridos_rueda_array, compresiones)
    
    fig_mr, ax_mr = plt.subplots(figsize=(10, 4))
    ax_mr.plot(compresiones, mr_inst, color='blue', lw=1.0)
    
    # Marcador rojo para la posición en vivo del slider
    if c_amort >= 0:
        mr_actual_inst = np.interp(c_amort, compresiones, mr_inst)
        ax_mr.plot(c_amort, mr_actual_inst, 'ro', markersize=6, label=f'Setup Actual ({c_amort:.1f} mm comp.)')
        ax_mr.legend()
        
    ax_mr.set_xlabel("Recorrido Amortiguador (mm)")
    ax_mr.set_ylabel("Motion Ratio Instantáneo")
    ax_mr.set_title("Cinemática de las Bieletas: Progresividad del Basculante")
    
    # Centrar la curva visualmente (de 0 al doble del valor medio)
    margen_y = np.nanmean(mr_inst) * 2.0 if len(mr_inst) > 0 else 4.0
    # Evitamos que se rompa si el MR medio es muy bajo o 0
    ax_mr.set_ylim(bottom=0, top=max(1.0, margen_y))
    
    ax_mr.grid(True, linestyle=':', alpha=0.6)
    
    st.pyplot(fig_mr)

# ==========================================
# 9. GRÁFICO HORQUILLA DELANTERA (OPCIONAL)
# ==========================================
if st.checkbox("Analizar Cinemática Eje Delantero", value=False):
    st.subheader("Recorrido Horquilla vs Recorrido Vertical (Eje Y)")
    
    pasos_h = 60
    compresiones_h = np.linspace(0, recorrido_max_horq, pasos_h)
    caidas_y_mundo = []
    
    # Base: horquilla extendida (c=0) pero con el amortiguador actual
    F_ext = top_fork_local - L_horq_ext * v_up
    d_x_ext = F_ext[0] - R_local_comp[0]
    d_y_ext = F_ext[1] - R_local_comp[1]
    ang_w_ext = math.asin((radio_del - radio_tras) / math.sqrt(max(0.001, d_x_ext**2 + d_y_ext**2)))
    rot_ext = ang_w_ext - math.atan2(d_y_ext, d_x_ext)
    p_rel_ext = tija_sup_face_stat - R_local_comp
    h_pipa_ext = p_rel_ext[0]*math.sin(rot_ext) + p_rel_ext[1]*math.cos(rot_ext) + radio_tras
    
    for c in compresiones_h:
        F_c = top_fork_local - (L_horq_ext - c) * v_up
        d_x = F_c[0] - R_local_comp[0]
        d_y = F_c[1] - R_local_comp[1]
        ang_w = math.asin((radio_del - radio_tras) / math.sqrt(max(0.001, d_x**2 + d_y**2)))
        rot_c = ang_w - math.atan2(d_y, d_x)
        p_rel_c = tija_sup_face_stat - R_local_comp
        h_pipa_c = p_rel_c[0]*math.sin(rot_c) + p_rel_c[1]*math.cos(rot_c) + radio_tras
        caidas_y_mundo.append(h_pipa_ext - h_pipa_c)
        
    recorridos_y_local = compresiones_h * v_up[1]
    
    fig_h, ax_h = plt.subplots(figsize=(10, 4))
    ax_h.plot(compresiones_h, recorridos_y_local, color='green', lw=1.0, label='Recorrido Eje Y (Local Chasis)')
    ax_h.plot(compresiones_h, caidas_y_mundo, color='purple', ls='--', lw=1.0, label='Caída Vertical Real (Steering Head vs Suelo)')
    
    # Marcador Setup Actual
    if c_horq >= 0:
        y_loc_actual = c_horq * v_up[1]
        ax_h.plot(c_horq, y_loc_actual, 'go', markersize=4, label=f'Setup Actual ({c_horq:.1f} mm Horquilla)')
        
    ax_h.set_xlabel("Recorrido Tubo Horquilla (mm)")
    ax_h.set_ylabel("Recorrido Vertical Eje Y (mm)")
    ax_h.set_title("Cinemática Delantera: Suspensión Telescópica")
    ax_h.set_ylim(bottom=0)
    ax_h.legend()
    ax_h.grid(True, linestyle=':', alpha=0.6)
    
    st.pyplot(fig_h)