import streamlit as st
import pandas as pd
from io import BytesIO

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    layout="wide",
    page_title="Sabana Profs – Directorio Académico",
    page_icon="🎓",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@300;400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    background-color: #070c12 !important;
    color: #c9d1db !important;
}
.stApp {
    background-color: #070c12;
    background-image:
        radial-gradient(ellipse 80% 400px at 50% -60px, rgba(14,165,233,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 60% 300px at 85% 80%, rgba(99,102,241,0.05) 0%, transparent 60%);
    background-attachment: fixed;
    min-height: 100vh;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
#MainMenu, footer, header { visibility: hidden !important; }

/* Ocultar sidebar nativo completamente */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ── Header ── */
.sabana-header {
    width: 100%;
    padding: 0 40px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(7,12,18,0.92);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 200;
}
.logo-group { display: flex; align-items: center; gap: 16px; }
.univ-badge { display: flex; flex-direction: column; line-height: 1.15; }
.univ-badge .sup { font-size: 8px; letter-spacing: .22em; color: #4b5563; font-weight: 600; text-transform: uppercase; }
.univ-badge .main { font-size: 17px; font-weight: 300; color: #f1f5f9; letter-spacing: .01em; }
.vdiv { width: 1px; height: 26px; background: rgba(255,255,255,0.07); }
.sys-label { font-size: 11px; font-weight: 500; letter-spacing: .14em; color: #475569; text-transform: uppercase; }
.nav-links { display: flex; gap: 32px; align-items: center; font-size: 12px; font-weight: 400; }
.nav-links a { color: #4b5563; text-decoration: none; transition: color .2s; letter-spacing: .03em; }
.nav-links a:hover { color: #e2e8f0; }
.nav-links a.active { color: #e2e8f0; border-bottom: 1px solid rgba(14,165,233,0.7); padding-bottom: 1px; }

/* ── Main wrapper ── */
.main-wrap { max-width: 1300px; margin: 0 auto; padding: 40px 28px 72px; }

/* ── Panel izquierdo de filtros ── */
.filter-panel {
    background: #0a1018;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 22px 18px;
    position: sticky;
    top: 74px;
}
.filter-panel-title {
    font-size: 10px; font-weight: 700; letter-spacing: .2em;
    text-transform: uppercase; color: #334155;
    margin-bottom: 18px; padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.filter-label {
    font-size: 10px; font-weight: 600; letter-spacing: .12em;
    text-transform: uppercase; color: #475569;
    margin-bottom: 6px; margin-top: 14px; display: block;
}
.filter-divider { height: 1px; background: rgba(255,255,255,0.05); margin: 14px 0; }

/* Ocultar labels de widgets dentro del panel */
.stSelectbox label, .stTextInput label, .stSlider label { display: none !important; }

/* Inputs */
[data-baseweb="input"] input, [data-baseweb="select"] div {
    background: rgba(255,255,255,0.03) !important;
    border-color: rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important; border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important; font-size: 13px !important;
}
[data-baseweb="input"] input:focus {
    border-color: rgba(14,165,233,0.5) !important;
    box-shadow: 0 0 0 2px rgba(14,165,233,0.1) !important;
}

/* ── LANDING ── */
.landing-hero { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 64px 0 48px; animation: fadeUp .7s ease both; }
.landing-eyebrow { font-size: 10px; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: #0ea5e9; margin-bottom: 20px; opacity: .85; }
.landing-title { font-size: clamp(32px, 5vw, 52px); font-weight: 200; color: #f8fafc; line-height: 1.12; letter-spacing: -.02em; margin-bottom: 16px; }
.landing-title strong { font-weight: 600; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.landing-sub { font-size: 15px; font-weight: 300; color: #475569; max-width: 520px; line-height: 1.7; margin-bottom: 48px; }
.upload-card { background: rgba(14,20,30,0.7); border: 1px solid rgba(14,165,233,0.2); border-radius: 20px; padding: 36px 48px; text-align: center; max-width: 440px; width: 100%; margin: 0 auto 20px; animation: glowPulse 4s ease-in-out infinite; }
.upload-icon { width: 52px; height: 52px; background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.2); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin: 0 auto 16px; }
.upload-card h3 { font-size: 15px; font-weight: 500; color: #e2e8f0; margin-bottom: 6px; }
.upload-card p { font-size: 11px; color: #334155; line-height: 1.6; }
.section-divider { width: 40px; height: 1px; background: rgba(14,165,233,0.4); margin: 48px auto; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 56px; animation: fadeUp .9s ease .2s both; }
.feature-item { background: rgba(10,16,24,0.6); border: 1px solid rgba(255,255,255,0.045); border-radius: 14px; padding: 24px 22px; transition: border-color .25s, transform .25s; }
.feature-item:hover { border-color: rgba(14,165,233,0.25); transform: translateY(-2px); }
.feature-icon { font-size: 20px; margin-bottom: 12px; display: block; }
.feature-title { font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 8px; }
.feature-desc { font-size: 12px; font-weight: 300; color: #334155; line-height: 1.65; }

/* ── DASHBOARD ── */
.add-zone { display: flex; align-items: center; gap: 16px; background: rgba(10,16,24,0.5); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px 20px; margin-bottom: 6px; transition: border-color .2s; }
.add-zone:hover { border-color: rgba(14,165,233,0.25); }
.add-zone-icon { font-size: 16px; color: #38bdf8; opacity: .8; flex-shrink: 0; }
.add-zone-text span { font-size: 12px; font-weight: 500; color: #64748b; letter-spacing: .04em; }
.chips-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; margin-top: 8px; }
.chip { display: inline-flex; align-items: center; gap: 5px; background: rgba(14,165,233,0.07); border: 1px solid rgba(14,165,233,0.2); color: #7dd3fc; font-size: 10px; font-weight: 500; letter-spacing: .06em; padding: 3px 10px; border-radius: 99px; }
.chip .dot { width: 5px; height: 5px; border-radius: 50%; background: #0ea5e9; }

/* Stats strip */
.stats-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; overflow: hidden; margin-bottom: 28px; animation: fadeUp .5s ease both; }
.stat-cell { background: #0a1018; padding: 20px 22px; display: flex; flex-direction: column; gap: 4px; transition: background .2s; }
.stat-cell:hover { background: rgba(14,165,233,0.04); }
.stat-num { font-size: 24px; font-weight: 300; color: #f1f5f9; letter-spacing: -.02em; font-family: 'JetBrains Mono', monospace !important; }
.stat-label { font-size: 9px; font-weight: 600; color: #334155; text-transform: uppercase; letter-spacing: .16em; }
.stat-accent { color: #38bdf8; }

/* Dir card */
.dir-card { background: #090f17; border: 1px solid rgba(255,255,255,0.055); border-radius: 16px; overflow: hidden; margin-bottom: 16px; animation: fadeUp .55s ease both; }
.dir-card-header { padding: 16px 22px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: space-between; }
.dir-card-header .prof-name { font-size: 15px; font-weight: 500; color: #e2e8f0; display: flex; align-items: center; gap: 10px; }
.prof-initial { width: 32px; height: 32px; background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.25); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; color: #38bdf8; flex-shrink: 0; font-family: 'JetBrains Mono', monospace; }
.dir-card-header .meta { font-size: 10px; font-weight: 500; color: #1e3a5f; letter-spacing: .08em; text-transform: uppercase; }

/* DataFrame */
[data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] table { border-collapse: collapse !important; }
[data-testid="stDataFrame"] table thead th { background: rgba(7,12,18,0.9) !important; color: #334155 !important; font-size: 9px !important; text-transform: uppercase !important; letter-spacing: .14em !important; font-weight: 700 !important; border-bottom: 1px solid rgba(255,255,255,0.05) !important; padding: 10px 14px !important; font-family: 'JetBrains Mono', monospace !important; }
[data-testid="stDataFrame"] table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.03) !important; }
[data-testid="stDataFrame"] table tbody tr:hover td { background: rgba(14,165,233,0.04) !important; }
[data-testid="stDataFrame"] table tbody td { color: #94a3b8 !important; font-size: 12px !important; background: #090f17 !important; padding: 10px 14px !important; font-family: 'Sora', sans-serif !important; }

/* Prof stats */
.prof-stats { display: flex; flex-direction: column; gap: 10px; }
.prof-stat { background: rgba(7,12,18,0.8); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 14px 16px; transition: border-color .2s; }
.prof-stat:hover { border-color: rgba(14,165,233,0.2); }
.prof-stat .val { font-size: 22px; font-weight: 300; color: #f1f5f9; font-family: 'JetBrains Mono', monospace !important; letter-spacing: -.01em; line-height: 1; margin-bottom: 5px; }
.prof-stat .val .unit { font-size: 12px; color: #38bdf8; margin-left: 3px; }
.prof-stat .lbl { font-size: 9px; font-weight: 600; color: #1e293b; text-transform: uppercase; letter-spacing: .14em; }

/* Buttons */
.stDownloadButton button { background: rgba(14,165,233,0.07) !important; border: 1px solid rgba(14,165,233,0.25) !important; color: #7dd3fc !important; border-radius: 8px !important; font-size: 12px !important; font-weight: 500 !important; font-family: 'Sora', sans-serif !important; letter-spacing: .04em !important; transition: all .2s !important; }
.stDownloadButton button:hover { background: rgba(14,165,233,0.15) !important; border-color: rgba(14,165,233,0.5) !important; }
.stButton button { background: rgba(239,68,68,0.06) !important; border: 1px solid rgba(239,68,68,0.2) !important; color: #fca5a5 !important; border-radius: 8px !important; font-size: 11px !important; font-family: 'Sora', sans-serif !important; letter-spacing: .04em !important; transition: all .2s !important; }
.stButton button:hover { background: rgba(239,68,68,0.12) !important; }

/* File uploader */
[data-testid="stFileUploader"] > label { display: none !important; }
[data-testid="stFileUploader"] section { background: transparent !important; border: none !important; padding: 0 !important; }
[data-testid="stFileUploaderDropzone"] { background: rgba(10,16,24,0.6) !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: rgba(14,165,233,0.4) !important; }

hr { border-color: rgba(255,255,255,0.05) !important; margin: 20px 0 !important; }

/* Footer */
.sabana-footer { border-top: 1px solid rgba(255,255,255,0.05); margin-top: 64px; padding: 22px 40px; display: flex; justify-content: space-between; align-items: center; font-size: 10px; color: #1e293b; letter-spacing: .06em; }
.sabana-footer nav { display: flex; gap: 24px; }
.sabana-footer nav a { color: #1e293b; text-decoration: none; transition: color .2s; text-transform: uppercase; }
.sabana-footer nav a:hover { color: #64748b; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes glowPulse { 0%, 100% { box-shadow: 0 0 40px rgba(14,165,233,0.05); } 50% { box-shadow: 0 0 60px rgba(14,165,233,0.12); } }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE PROCESAMIENTO
# ══════════════════════════════════════════════════════════════════════════════

def parsear_hora(serie: pd.Series) -> pd.Series:
    limpia = serie.astype(str).str.strip()
    limpia = limpia.str.replace(r':([AP]M)$', r' \1', regex=True)
    return pd.to_datetime(limpia, format='%I:%M %p', errors='coerce')


def procesar_excel(file, nombre_semestre: str) -> pd.DataFrame:
    df = pd.read_excel(file, header=0)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    alias = {
        'Nombre profesor':     ['Nombre profesor', 'Nombre Profesor', 'Profesor', 'DOCENTE'],
        'Nombre del curso':    ['Nombre del curso', 'Nombre Curso', 'Materia', 'MATERIA', 'ASIGNATURA'],
        'Ciclo Lectivo':       ['Ciclo Lectivo', 'Ciclo', 'Semestre', 'SEMESTRE', 'PERIODO'],
        'Descripción Materia': ['Descripción Materia', 'Descripcion Materia', 'Departamento', 'DEPARTAMENTO', 'Depto'],
        'Componente':          ['Componente', 'COMPONENTE'],
        'F Inicial':           ['F Inicial', 'Fecha Inicio', 'F_Inicial', 'FECHA INICIO'],
        'Fecha Final':         ['Fecha Final', 'Fecha_Final', 'F Final', 'FECHA FIN'],
        'Hora Inicio':         ['Hora Inicio', 'HORA INICIO', 'H_Inicio'],
        'Hora Final':          ['Hora Final',  'HORA FINAL',  'H_Final'],
        'ID Sección Combinada':['ID Sección Combinada', 'ID Seccion Combinada', 'ID_Seccion_Combinada'],
        'Día':                 ['Día', 'Dia', 'DIA', 'DAY'],
        'ID Instalación':      ['ID Instalación', 'ID Instalacion', 'Salón', 'Salon', 'SALON'],
    }
    rename = {}
    for canonical, opciones in alias.items():
        for op in opciones:
            if op in df.columns and canonical not in df.columns:
                rename[op] = canonical
    df = df.rename(columns=rename)

    col_prof = 'Nombre profesor'
    col_mat  = 'Nombre del curso'
    if col_prof not in df.columns or col_mat not in df.columns:
        st.error(f"❌ No se encontraron las columnas necesarias en **{nombre_semestre}**. "
                 f"Columnas disponibles: {list(df.columns)}")
        return pd.DataFrame()

    df = df.dropna(subset=[col_prof])
    df[col_prof] = df[col_prof].astype(str).str.strip().str.title()
    df[col_mat]  = df[col_mat].astype(str).str.strip().str.title()

    if 'Ciclo Lectivo' not in df.columns:
        df['Ciclo Lectivo'] = nombre_semestre

    if 'Hora Inicio' in df.columns and 'Hora Final' in df.columns:
        h_ini = parsear_hora(df['Hora Inicio'])
        h_fin = parsear_hora(df['Hora Final'])
        df['Hrs_Sesion'] = (h_fin - h_ini).dt.total_seconds() / 3600
        df['Hrs_Sesion'] = df['Hrs_Sesion'].clip(lower=0)
    else:
        df['Hrs_Sesion'] = 1.0

    if 'ID Sección Combinada' in df.columns:
        mask_comb = (
            df['ID Sección Combinada'].notna() &
            (df['ID Sección Combinada'].astype(str).str.strip() != '')
        )
        cols_esp = [c for c in ['Nombre profesor','Día','Hora Inicio','Hora Final','ID Instalación']
                    if c in df.columns]
        df_comb   = df[mask_comb].drop_duplicates(subset=cols_esp, keep='first')
        df_normal = df[~mask_comb]
        df = pd.concat([df_normal, df_comb], ignore_index=True)

    grupo = [c for c in ['Ciclo Lectivo','Componente','Nombre profesor',
                          'Nombre del curso','Descripción Materia'] if c in df.columns]

    agg_dict = {'Hrs_Sesion': lambda x: round(x.sum() * 16, 1)}
    if 'F Inicial'   in df.columns: agg_dict['F Inicial']   = 'min'
    if 'Fecha Final' in df.columns: agg_dict['Fecha Final'] = 'max'

    reporte = df.groupby(grupo, as_index=False).agg(agg_dict)
    reporte = reporte.rename(columns={
        'Ciclo Lectivo':       'Semestre',
        'Nombre profesor':     'Profesor',
        'Nombre del curso':    'Materia',
        'Descripción Materia': 'Departamento',
        'Hrs_Sesion':          'Horas_Totales',
        'F Inicial':           'Fecha_Inicio',
        'Fecha Final':         'Fecha_Fin',
    })
    reporte['Semestre'] = reporte['Semestre'].astype(str).str.strip()
    return reporte


# ══════════════════════════════════════════════════════════════════════════════
# ESTADO DE SESIÓN
# ══════════════════════════════════════════════════════════════════════════════
if 'df_master' not in st.session_state: st.session_state.df_master = pd.DataFrame()
if 'cargados'  not in st.session_state: st.session_state.cargados  = []

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
tiene_datos = not st.session_state.df_master.empty

st.markdown(f"""
<div class="sabana-header">
  <div class="logo-group">
    <div class="univ-badge">
      <span class="sup">Universidad de</span>
      <span class="main">La Sabana</span>
    </div>
    <div class="vdiv"></div>
    <span class="sys-label">Sabana Profs</span>
    <div class="vdiv"></div>
    <span class="sys-label">Directorio Académico</span>
  </div>
  <nav class="nav-links">
    <a href="#" {"class='active'" if not tiene_datos else ""}>Inicio</a>
    <a href="#" {"class='active'" if tiene_datos else ""}>Buscar</a>
    <a href="#">Ayuda</a>
  </nav>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════════
if not tiene_datos:
    st.markdown("""
    <div class="landing-hero">
      <span class="landing-eyebrow">Sistema de Gestión Académica</span>
      <h1 class="landing-title">Consulta la carga<br>docente de <strong>La Sabana</strong></h1>
      <p class="landing-sub">
        Procesa los archivos de programación académica para obtener
        el historial de horas por profesor, semestre y departamento
        de forma rápida y precisa.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        st.markdown("""
        <div class="upload-card">
          <div class="upload-icon">📊</div>
          <h3>Cargar base de datos</h3>
          <p>Arrastra tu archivo Excel o haz clic para seleccionar</p>
        </div>
        """, unsafe_allow_html=True)
        archivo = st.file_uploader("xlsx", type=["xlsx","xls"],
                                   label_visibility="collapsed",
                                   accept_multiple_files=False)
        if archivo and archivo.name not in st.session_state.cargados:
            with st.spinner("Procesando datos…"):
                df_nuevo = procesar_excel(
                    archivo,
                    archivo.name.replace(".xlsx","").replace(".xls","")
                )
            if not df_nuevo.empty:
                st.session_state.df_master = df_nuevo
                st.session_state.cargados.append(archivo.name)
                st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
      <div class="feature-item">
        <span class="feature-icon">🗂️</span>
        <div class="feature-title">Multi-semestre</div>
        <div class="feature-desc">Carga y acumula archivos de distintos semestres. El sistema consolida todo en un único directorio navegable.</div>
      </div>
      <div class="feature-item">
        <span class="feature-icon">⏱️</span>
        <div class="feature-title">Cálculo automático</div>
        <div class="feature-desc">Calcula las horas totales por materia a partir de los horarios de sesión multiplicados por las 16 semanas del período.</div>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🔍</span>
        <div class="feature-title">Búsqueda y filtros</div>
        <div class="feature-desc">Filtra por profesor, departamento, componente o rango de semestres para encontrar exactamente lo que necesitas.</div>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🪞</span>
        <div class="feature-title">Limpieza de duplicados</div>
        <div class="feature-desc">Detecta y elimina automáticamente secciones espejo y registros combinados para evitar doble conteo de horas.</div>
      </div>
      <div class="feature-item">
        <span class="feature-icon">📥</span>
        <div class="feature-title">Exportación</div>
        <div class="feature-desc">Descarga los datos de cada docente en formato CSV o Excel con un solo clic.</div>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🏛️</span>
        <div class="feature-title">Datos institucionales</div>
        <div class="feature-desc">Compatible con los archivos de programación estándar de La Sabana, incluyendo variantes de columnas y formatos históricos.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# DASHBOARD (con datos)
# ════════════════════════════════════════════════════════════
else:
    df = st.session_state.df_master.copy()

    # Layout: columna filtros (izq) | contenido (der)
    col_filtros, col_contenido = st.columns([1, 3.2], gap="large")

    # ════════════ PANEL DE FILTROS ════════════
    with col_filtros:
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        st.markdown('<div class="filter-panel-title">Filtros</div>', unsafe_allow_html=True)

        # Rango de semestres
        semestres = sorted(df['Semestre'].dropna().unique())
        st.markdown('<span class="filter-label">Rango de semestres</span>', unsafe_allow_html=True)
        if len(semestres) > 1:
            sem_rango = st.select_slider(
                "sem",
                options=semestres,
                value=(semestres[0], semestres[-1]),
                label_visibility="collapsed",
            )
        else:
            sem_rango = (semestres[0], semestres[0])
            st.markdown(
                f'<div style="font-size:12px;color:#475569;padding:6px 0 10px;">{semestres[0]}</div>',
                unsafe_allow_html=True
            )

        df_f = df[
            (df['Semestre'] >= sem_rango[0]) &
            (df['Semestre'] <= sem_rango[1])
        ]

        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)

        # Buscar profesor
        st.markdown('<span class="filter-label">Buscar profesor</span>', unsafe_allow_html=True)
        buscar_prof = st.text_input("buscar", placeholder="Nombre…", label_visibility="collapsed")
        if buscar_prof:
            df_f = df_f[df_f['Profesor'].str.contains(buscar_prof, case=False, na=False)]

        # Selectbox de docente
        st.markdown('<span class="filter-label">Docente</span>', unsafe_allow_html=True)
        profesores = sorted(df_f['Profesor'].dropna().unique())
        if not profesores:
            st.markdown('<div style="font-size:11px;color:#ef4444;padding:6px 0;">Sin resultados</div>', unsafe_allow_html=True)
            st.stop()
        prof_sel = st.selectbox("prof", profesores, label_visibility="collapsed")

        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)

        # Departamento
        if 'Departamento' in df_f.columns:
            st.markdown('<span class="filter-label">Departamento</span>', unsafe_allow_html=True)
            deptos = ["Todos"] + sorted(df_f['Departamento'].dropna().unique())
            depto_sel = st.selectbox("depto", deptos, label_visibility="collapsed")
        else:
            depto_sel = "Todos"

        # Componente
        if 'Componente' in df_f.columns:
            st.markdown('<span class="filter-label">Componente</span>', unsafe_allow_html=True)
            comps = ["Todos"] + sorted(df_f['Componente'].dropna().unique())
            comp_sel = st.selectbox("comp", comps, label_visibility="collapsed")
        else:
            comp_sel = "Todos"

        st.markdown('</div>', unsafe_allow_html=True)

        # Botón limpiar
        st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
        if st.button("Limpiar datos", use_container_width=True):
            st.session_state.df_master = pd.DataFrame()
            st.session_state.cargados  = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ════════════ CONTENIDO PRINCIPAL ════════════
    with col_contenido:

        # Zona agregar semestre
        st.markdown("""
        <div class="add-zone">
          <span class="add-zone-icon">＋</span>
          <div class="add-zone-text"><span>Agregar otro semestre</span></div>
        </div>
        """, unsafe_allow_html=True)
        archivo_nuevo = st.file_uploader(
            "xlsx2", type=["xlsx","xls"],
            label_visibility="collapsed",
            accept_multiple_files=False,
            key="uploader_adicional"
        )
        if archivo_nuevo and archivo_nuevo.name not in st.session_state.cargados:
            with st.spinner(f"Procesando {archivo_nuevo.name}…"):
                df_nuevo = procesar_excel(
                    archivo_nuevo,
                    archivo_nuevo.name.replace(".xlsx","").replace(".xls","")
                )
            if not df_nuevo.empty:
                st.session_state.df_master = pd.concat(
                    [st.session_state.df_master, df_nuevo], ignore_index=True
                ).drop_duplicates()
                st.session_state.cargados.append(archivo_nuevo.name)
                st.success(f"✅ {archivo_nuevo.name} agregado.")
                st.rerun()

        # Chips
        chips_html = '<div class="chips-row">'
        for nombre in st.session_state.cargados:
            chips_html += f'<span class="chip"><span class="dot"></span>{nombre}</span>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

        # Stats strip
        n_profs    = df['Profesor'].nunique()
        n_materias = df['Materia'].nunique()
        n_sems     = df['Semestre'].nunique()
        total_hrs  = int(df['Horas_Totales'].sum())

        st.markdown(f"""
        <div class="stats-strip">
          <div class="stat-cell">
            <span class="stat-num">{n_profs:,}</span>
            <span class="stat-label">Profesores</span>
          </div>
          <div class="stat-cell">
            <span class="stat-num">{n_materias:,}</span>
            <span class="stat-label">Materias</span>
          </div>
          <div class="stat-cell">
            <span class="stat-num">{n_sems}</span>
            <span class="stat-label">Semestres</span>
          </div>
          <div class="stat-cell">
            <span class="stat-num stat-accent">{total_hrs:,}</span>
            <span class="stat-label">Horas totales</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Aplicar filtros
        resultado = df_f[df_f['Profesor'] == prof_sel].copy()
        if depto_sel != "Todos" and 'Departamento' in resultado.columns:
            resultado = resultado[resultado['Departamento'] == depto_sel]
        if comp_sel != "Todos" and 'Componente' in resultado.columns:
            resultado = resultado[resultado['Componente'] == comp_sel]

        inicial = prof_sel[0].upper() if prof_sel else "?"

        # Dir card
        st.markdown(f"""
        <div class="dir-card">
          <div class="dir-card-header">
            <div class="prof-name">
              <div class="prof-initial">{inicial}</div>
              {prof_sel}
            </div>
            <span class="meta">{len(resultado)} registros &nbsp;·&nbsp; {sem_rango[0]} → {sem_rango[1]}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        cols_mostrar = [c for c in ['Semestre','Componente','Materia','Departamento',
                                    'Horas_Totales','Fecha_Inicio','Fecha_Fin']
                        if c in resultado.columns]

        col_tabla, col_stats = st.columns([3, 1], gap="medium")

        with col_tabla:
            col_config = {}
            if 'Horas_Totales' in resultado.columns:
                col_config['Horas_Totales'] = st.column_config.NumberColumn("Horas / Semestre", format="%.1f h")
            if 'Fecha_Inicio' in resultado.columns:
                col_config['Fecha_Inicio'] = st.column_config.DateColumn("Fecha Inicio", format="DD/MM/YYYY")
            if 'Fecha_Fin' in resultado.columns:
                col_config['Fecha_Fin'] = st.column_config.DateColumn("Fecha Fin", format="DD/MM/YYYY")
            st.dataframe(
                resultado[cols_mostrar],
                use_container_width=True,
                hide_index=True,
                height=380,
                column_config=col_config,
            )

        with col_stats:
            total_prof = resultado['Horas_Totales'].sum() if 'Horas_Totales' in resultado.columns else 0
            n_mat_prof = resultado['Materia'].nunique()
            n_sem_prof = resultado['Semestre'].nunique()

            st.markdown(f"""
            <div class="prof-stats">
              <div class="prof-stat">
                <div class="val">{total_prof:.0f}<span class="unit">h</span></div>
                <div class="lbl">Total en el período</div>
              </div>
              <div class="prof-stat">
                <div class="val">{n_mat_prof}</div>
                <div class="lbl">Materias distintas</div>
              </div>
              <div class="prof-stat">
                <div class="val">{n_sem_prof}</div>
                <div class="lbl">Semestres activos</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Descarga
        if not resultado.empty:
            nombre_archivo = prof_sel.replace(' ','_')
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                st.download_button(
                    "↓ Descargar datos (CSV)",
                    data=resultado.to_csv(index=False).encode('utf-8-sig'),
                    file_name=f"Datos_{nombre_archivo}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with c2:
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Datos Profesor')
                buf.seek(0)
                st.download_button(
                    "↓ Descargar datos (Excel)",
                    data=buf,
                    file_name=f"Datos_{nombre_archivo}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

# Footer
st.markdown("""
<div class="sabana-footer">
  <span>© 2026 Universidad de La Sabana — Sabana Profs</span>
  <nav>
    <a href="#">Privacidad</a>
    <a href="#">Contacto</a>
    <a href="#">Soporte</a>
  </nav>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)