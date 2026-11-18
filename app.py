# -*- coding: utf-8 -*-
"""ALETEO - Sitio en Streamlit (versión oscura / neón)
Autoras: Laura Natalia Garcia y Sara Londoño

Estructura de carpetas:
    app.py
    requirements.txt
    videos/   -> archivos .mp4 (sección "ALETEO en acción", en orden alfabético)
    fotos/    -> .jpg .jpeg .png .webp .gif (galería)
    media/    -> TUS imágenes o videos para reemplazar los visuales hechos con código.
                 Nómbralos exactamente así (la extensión puede ser mp4, webm, gif, png, jpg, jpeg o webp):
                     hero.*    -> portada (reemplaza la mariposa grande)
                     intro.*   -> sección "No somos visitantes de la naturaleza"
                     demo.*    -> simulación (si es video, el control deslizante cambia su velocidad)
                     park.*    -> sección "Una nueva forma de acercarnos a la conservación"
                 Si un archivo no existe, se muestra el visual original hecho con código.
                 Recomendación: videos cortos (idealmente < 15 MB) en loop, sin audio.
"""
import base64
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent
MEDIA = BASE / "media"
VIDEOS = sorted((BASE / "videos").glob("*.mp4"))
FOTOS = sorted(
    p for p in (BASE / "fotos").glob("*")
    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
)
EXT_VIDEO = {".mp4", ".webm"}
EXT_IMG = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

st.set_page_config(
    page_title="ALETEO — La naturaleza siente nuestra presencia",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Estilos de la página Streamlit (quita márgenes y menús) ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"]{display:none!important}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#05050a!important}
.block-container{padding:0!important;max-width:100%!important}
div[data-testid="stVerticalBlock"]{gap:0!important}
iframe{display:block;border:0;background:#05050a}
.al-wrap{background:#05050a}
.al-tag{font:700 .7rem 'DM Sans',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#22e6ff;text-shadow:0 0 12px #22e6ff99;margin:0 0 20px}
.al-h{font:700 clamp(2.7rem,6vw,5.5rem)/.96 'Outfit',sans-serif;letter-spacing:-.065em;color:#f4f5ff;margin:0 0 23px}
.al-h em{font-style:normal;color:#ff2fd1;text-shadow:0 0 28px #ff2fd1aa}
.al-lead{font:400 1.03rem/1.8 'DM Sans',sans-serif;color:#a3a8c3;max-width:700px;margin:0 0 30px}
.al-cap{font:700 1.15rem 'Outfit',sans-serif;color:#c8ff3d;text-shadow:0 0 14px #c8ff3d66;margin:12px 4px 0}
.al-cap2{font:400 .86rem 'DM Sans',sans-serif;color:#8a90ad;margin:0 4px 28px}
div[data-testid="stVideo"] video, div[data-testid="stImage"] img{
  border-radius:18px;border:1px solid #22e6ff66;box-shadow:0 0 22px #22e6ff33,0 0 60px #9d6bff22}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Medios propios (hero / intro / demo / park) ----------
@st.cache_data(show_spinner=False)
def _leer_medio(ruta: str, mtime: float) -> str:
    """Devuelve la etiqueta HTML (img o video) con el archivo embebido en base64."""
    p = Path(ruta)
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    datos = base64.b64encode(p.read_bytes()).decode()
    src = f"data:{mime};base64,{datos}"
    if p.suffix.lower() in EXT_VIDEO:
        return (f'<video class="mediaslot" src="{src}" autoplay muted loop playsinline '
                f'disablepictureinpicture></video>')
    return f'<img class="mediaslot" src="{src}" alt="">'


def slot(nombre: str):
    """Busca media/<nombre>.<ext>. Devuelve HTML o None si no existe."""
    if not MEDIA.exists():
        return None
    for p in sorted(MEDIA.glob(f"{nombre}.*")):
        if p.suffix.lower() in EXT_VIDEO | EXT_IMG:
            return _leer_medio(str(p), p.stat().st_mtime)
    return None


# ---------- Estilos y scripts de las partes en HTML ----------
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
:root{--bg:#05050a;--bg2:#0a0a14;--panel:#0e0e1a;--lime:#c8ff3d;--pink:#ff2fd1;--cyan:#22e6ff;--violet:#9d6bff;--yellow:#ffe14d;--coral:#ff5c8a;--text:#f2f4ff;--muted:#a3a8c3}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;overflow-x:hidden}a{color:inherit;text-decoration:none}button{font:inherit;cursor:pointer}
.glow{position:fixed;z-index:20;pointer-events:none;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,#22e6ff22,#ff2fd114 45%,transparent 70%);transform:translate(-50%,-50%)}
.mediaslot{width:100%;height:100%;object-fit:cover;display:block}

nav{height:78px;padding:0 7vw;display:flex;align-items:center;justify-content:space-between;position:absolute;z-index:5;width:100%;color:white}
.brand,.footer-logo{font:800 1.6rem Outfit;letter-spacing:-.07em;text-shadow:0 0 18px #ffffff55}.brand span,.footer-logo span{color:var(--lime);text-shadow:0 0 18px var(--lime)}
.navlinks{display:flex;gap:25px;font-size:.8rem}.navlinks a{color:#c9cde6;transition:.2s}.navlinks a:hover{color:var(--lime);text-shadow:0 0 12px var(--lime)}
.navbutton{border:1px solid var(--cyan);color:var(--cyan);border-radius:30px;padding:10px 16px;font-size:.78rem;box-shadow:0 0 14px #22e6ff55,inset 0 0 12px #22e6ff22}

.hero{min-height:820px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 78% 38%,#2a0f4d 0,#10092a 38%,#05050a 75%);color:white;padding:155px 8vw 90px;display:flex;align-items:center}
.hero:before{content:"";position:absolute;width:650px;height:650px;border:1px solid #9d6bff55;border-radius:50%;right:-100px;top:10%;box-shadow:0 0 0 65px #9d6bff10,0 0 0 130px #22e6ff08,0 0 60px #9d6bff44}
.copy{position:relative;z-index:2;max-width:650px}
.eyebrow,.tag{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:var(--cyan);text-shadow:0 0 12px #22e6ff99}
.hero .eyebrow{color:var(--lime);text-shadow:0 0 12px #c8ff3d99}
h1{font:800 clamp(5rem,12vw,10rem)/.78 Outfit;letter-spacing:-.09em;margin:36px 0 27px;text-shadow:0 0 40px #ffffff44}
h1 span{display:block;margin-left:9vw;color:var(--lime);text-shadow:0 0 22px var(--lime),0 0 70px #c8ff3d88}
.subtitle{font:500 clamp(1.1rem,2vw,1.45rem) Outfit;color:#ffd0f5;text-shadow:0 0 18px #ff2fd188}
.desc{line-height:1.75;color:#b9bdd8;max-width:450px;margin:20px 0 28px}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.btn{padding:14px 21px;border-radius:40px;font-size:.85rem;font-weight:700;display:inline-block;transition:.25s}.btn:hover{transform:translateY(-3px)}
.lime{background:var(--lime);color:#050508;box-shadow:0 0 22px #c8ff3d88,0 0 60px #c8ff3d33}
.ghost{border:1px solid var(--pink);color:#ffb8ee;box-shadow:0 0 16px #ff2fd155,inset 0 0 14px #ff2fd122}
.hero-note{margin-top:45px;color:#8a90ad;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase}

.art{position:absolute;right:4%;top:15%;width:min(54vw,660px);height:75%;display:grid;place-items:center}
.heromedia{width:min(100%,520px);aspect-ratio:1;border-radius:36px;overflow:hidden;border:1px solid var(--pink);box-shadow:0 0 30px #ff2fd188,0 0 100px #22e6ff44,inset 0 0 30px #ff2fd133;animation:float 5s ease-in-out infinite}
.orbit{position:absolute;width:82%;aspect-ratio:1;border:1px solid #22e6ff55;border-radius:50%;animation:spin 45s linear infinite;box-shadow:0 0 30px #22e6ff22}
.orbit:before,.orbit:after{content:"";position:absolute;width:10px;height:10px;background:var(--pink);border-radius:50%;top:15%;left:15%;box-shadow:0 0 22px 4px var(--pink)}
.orbit:after{top:auto;left:auto;bottom:13%;right:14%;background:var(--lime);box-shadow:0 0 22px 4px var(--lime)}
@keyframes spin{to{transform:rotate(360deg)}}

.butterfly{position:relative;width:70%;max-width:520px;aspect-ratio:1;filter:drop-shadow(0 0 30px #9d6bffaa) drop-shadow(0 0 70px #22e6ff55);animation:float 5s ease-in-out infinite}
.wing{position:absolute;width:47%;height:55%;top:12%;background:linear-gradient(145deg,var(--cyan),#5a6dff 55%,var(--violet));border:2px solid #ffffffcc;box-shadow:inset 0 0 30px #ffffff77,0 0 28px #22e6ff99;transform-origin:100% 85%;border-radius:80% 15% 75% 25%;transition:transform .5s}
.wing.l{left:4%;transform:rotate(-24deg)}.wing.r{right:4%;transform:scaleX(-1) rotate(-24deg)}
.wing.lower{top:48%;height:36%;width:39%;background:linear-gradient(145deg,var(--pink),var(--yellow));border-radius:30% 70% 65% 35%;box-shadow:inset 0 0 30px #ffffff77,0 0 28px #ff2fd199}
.wing.lower.l{left:12%;transform:rotate(25deg)}.wing.lower.r{right:12%;transform:scaleX(-1) rotate(25deg)}
.butterfly.open .wing.l{transform:rotate(-48deg)}.butterfly.open .wing.r{transform:scaleX(-1) rotate(-48deg)}
.butterfly.open .wing.lower.l{transform:rotate(48deg)}.butterfly.open .wing.lower.r{transform:scaleX(-1) rotate(48deg)}
.body{position:absolute;z-index:2;width:5%;height:60%;left:47.5%;top:18%;border-radius:50%;background:linear-gradient(90deg,#1b1b33,#8a90c0,#12121f);box-shadow:0 0 14px #ffffff66}
.antenna{position:absolute;z-index:3;top:13%;left:49%;height:15%;width:2px;background:var(--lime);box-shadow:0 0 10px var(--lime);transform:rotate(-20deg)}.antenna.a2{left:51%;transform:rotate(20deg)}
.floatlabel{position:absolute;padding:11px 15px;border-radius:40px;background:#0b0b1acc;backdrop-filter:blur(12px);border:1px solid var(--cyan);color:#d8fbff;box-shadow:0 0 18px #22e6ff55;font-size:.7rem;animation:float 6s infinite;z-index:3}
.fl1{top:20%;right:2%}.fl2{bottom:20%;left:0;animation-delay:-2s;border-color:var(--pink);color:#ffd9f6;box-shadow:0 0 18px #ff2fd155}
@keyframes float{50%{translate:0 -16px}}
.scroll{position:absolute;bottom:28px;left:8vw;font-size:.67rem;letter-spacing:.16em;color:#8a90ad}

section{padding:110px 8vw;position:relative;background:var(--bg)}
.tag{margin-bottom:20px}
.heading{font:700 clamp(2.7rem,6vw,5.5rem)/.96 Outfit;letter-spacing:-.065em;margin:0 0 23px;max-width:850px;color:#f4f5ff}
.heading em{font-style:normal;color:var(--lime);text-shadow:0 0 26px #c8ff3daa,0 0 70px #c8ff3d44}
.lead{font-size:1.03rem;line-height:1.8;color:var(--muted);max-width:700px}.lead strong{color:var(--lime)}

.intro{display:grid;grid-template-columns:1fr .8fr;gap:8vw;align-items:center;background:radial-gradient(ellipse at 85% 50%,#1a0d33 0,transparent 60%),var(--bg)}
.introart,.parkart{height:390px;border-radius:48%;display:grid;place-items:center;position:relative;overflow:hidden}
.introart{background:radial-gradient(circle at 50% 40%,#ff2fd1aa,#7a2bff77 45%,#0a0a14 85%);border:1px solid var(--pink);box-shadow:0 0 40px #ff2fd166,0 0 120px #9d6bff33,inset 0 0 40px #ff2fd133}
.introart:before,.parkart:before{content:"";position:absolute;width:80%;aspect-ratio:1;border:1px solid #ffffff55;border-radius:50%;box-shadow:0 0 0 40px #ffffff10,0 0 0 80px #ffffff08}
.introart span,.parkart span{font-size:9rem;filter:drop-shadow(0 0 30px #ffffff88);animation:float 4s infinite;z-index:1}
.introart small{position:absolute;bottom:28px;background:#05050acc;color:#fff;padding:9px 14px;border-radius:30px;font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;border:1px solid #ffffff55;z-index:2}
.has-media:before{display:none}.has-media .mediaslot{position:absolute;inset:0}

.manifesto{background:linear-gradient(120deg,#0b0420,#1b0536 50%,#05161c);overflow:hidden;border-top:1px solid #ff2fd155;border-bottom:1px solid #22e6ff55}
.manifesto .tag{color:var(--yellow);text-shadow:0 0 12px #ffe14d99}
.manifesto blockquote{font:700 clamp(2.8rem,6.7vw,6.5rem)/.98 Outfit;letter-spacing:-.07em;margin:0;max-width:1100px;color:#fff}
.manifesto blockquote span{color:var(--pink);text-shadow:0 0 26px #ff2fd1,0 0 80px #ff2fd177}
.manifesto p{max-width:540px;line-height:1.7;color:#c0c4de;margin-top:30px}
.flower{position:absolute;right:8%;bottom:0;font-size:9rem;opacity:.35;color:var(--cyan);text-shadow:0 0 40px var(--cyan)}

.experience{background:var(--bg2)}
.headrow{display:flex;justify-content:space-between;align-items:end;gap:35px;margin-bottom:50px}.headrow .lead{max-width:390px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:17px}
.step{border-radius:26px;padding:27px;min-height:320px;background:#0e0e1a;border:1px solid var(--yellow);box-shadow:0 0 24px #ffe14d33,inset 0 0 30px #ffe14d0d;transition:.3s}
.step:hover{transform:translateY(-8px);box-shadow:0 0 40px #ffe14d66,inset 0 0 30px #ffe14d14}
.step:nth-child(2){border-color:var(--violet);box-shadow:0 0 24px #9d6bff44,inset 0 0 30px #9d6bff12}.step:nth-child(2):hover{box-shadow:0 0 40px #9d6bff88}
.step:nth-child(3){border-color:var(--cyan);box-shadow:0 0 24px #22e6ff44,inset 0 0 30px #22e6ff10}.step:nth-child(3):hover{box-shadow:0 0 40px #22e6ff88}
.step .emoji{font-size:4.4rem;height:100px;display:grid;place-items:center;filter:drop-shadow(0 0 18px #ffffff66)}
.num{font:700 3.6rem Outfit;color:transparent;-webkit-text-stroke:1px #ffffff66}
.step h3,.techitem h3,.futurecard h3{font:700 1.4rem Outfit;margin:15px 0 8px;color:#fff}
.step p,.futurecard p{font-size:.88rem;line-height:1.65;color:var(--muted)}

.demo{background:radial-gradient(ellipse at 20% 20%,#0d1f3a 0,transparent 55%),#03030a;color:white}
.demo .tag{color:var(--lime);text-shadow:0 0 12px #c8ff3d99}.demo .heading{color:white}.demo .lead{color:var(--muted)}
.demogrid{display:grid;grid-template-columns:1fr 1fr;gap:7vw;align-items:center}
.stage{min-height:400px;border:1px solid var(--cyan);border-radius:30px;background:radial-gradient(circle,#1b2a66,#0a0a1e 70%);position:relative;display:grid;place-items:center;overflow:hidden;box-shadow:0 0 36px #22e6ff55,0 0 100px #9d6bff33,inset 0 0 40px #22e6ff22}
.stage .butterfly{width:70%;max-width:350px}.stage .orbit{width:76%}
.stage.has-media:before{display:none}
.stage.has-media:after{content:"";position:absolute;inset:auto 0 0 0;height:90px;background:linear-gradient(transparent,#000000cc);z-index:1}
.stagefoot{position:absolute;bottom:18px;left:18px;right:18px;display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:.7rem;color:#e6f8ff;z-index:2}
.stagefoot button{border:1px solid var(--lime);background:#c8ff3d18;color:var(--lime);border-radius:30px;padding:9px 13px;box-shadow:0 0 12px #c8ff3d44}
.rangebox{margin-top:35px}.rangebox label{display:flex;justify-content:space-between;font-size:.75rem;color:#c9cde6;margin-bottom:12px}
.range{width:100%;accent-color:var(--lime)}
.meter{height:7px;background:#ffffff1a;border-radius:20px;margin-top:13px;overflow:hidden}
.meter div{height:100%;width:25%;background:linear-gradient(90deg,var(--cyan),var(--pink),var(--lime));box-shadow:0 0 14px var(--pink);transition:width .2s}
.tiny{font-size:.72rem;color:#7d83a1;line-height:1.6;margin-top:18px}

.techgrid{display:grid;grid-template-columns:.8fr 1.2fr;gap:8vw;align-items:start}
.flow{background:#0c0c18;color:white;border-radius:28px;padding:28px;position:sticky;top:30px;border:1px solid var(--violet);box-shadow:0 0 34px #9d6bff55,inset 0 0 30px #9d6bff1a}
.flow h3{font:700 1.5rem Outfit}
.node{padding:15px;text-align:center;border:1px solid #22e6ff77;border-radius:13px;background:#22e6ff0d;font-size:.8rem;margin:10px 0;box-shadow:0 0 12px #22e6ff22}
.arrow{text-align:center;color:var(--lime);text-shadow:0 0 10px var(--lime)}
.techlist{display:grid;gap:15px}
.techitem{padding:22px 0;border-bottom:1px solid #ffffff1c;display:grid;grid-template-columns:48px 1fr;gap:15px}
.icon{height:45px;width:45px;border-radius:14px;background:#c8ff3d15;border:1px solid var(--lime);box-shadow:0 0 14px #c8ff3d55;display:grid;place-items:center;font-size:1.3rem}
.techitem h3{margin:0 0 7px}.techitem p{margin:0;color:var(--muted);font-size:.88rem;line-height:1.7}

.park{background:radial-gradient(ellipse at 15% 60%,#2b2205 0,transparent 55%),var(--bg2);display:grid;grid-template-columns:1fr .8fr;gap:7vw;align-items:center}
.park .tag{color:var(--yellow);text-shadow:0 0 12px #ffe14d99}
.parkart{height:370px;border-radius:48% 48% 20px 20px;background:linear-gradient(160deg,#7dff6a66,#0f6b5a99 60%,#05050a);border:1px solid var(--lime);box-shadow:0 0 40px #c8ff3d55,0 0 110px #22e6ff22,inset 0 0 40px #c8ff3d22}

.video{background:var(--bg)}
.reflection{background:var(--bg2)}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:40px}
.card{background:#0e0e1a;border-radius:22px;padding:26px;min-height:190px;border:1px solid #ffffff22;transition:.3s}
.card:nth-child(1){border-color:var(--pink);box-shadow:0 0 20px #ff2fd144}.card:nth-child(2){border-color:var(--cyan);box-shadow:0 0 20px #22e6ff44}
.card:nth-child(3){border-color:var(--yellow);box-shadow:0 0 20px #ffe14d33}.card:nth-child(4){border-color:var(--lime);box-shadow:0 0 20px #c8ff3d44}
.card:hover{transform:translateY(-5px)}
.card h3{font:700 1.15rem Outfit;margin:0 0 12px;color:#fff}.card p{font-size:.86rem;color:var(--muted);line-height:1.7;margin:0}
.card small{display:block;margin-top:14px;color:var(--violet);text-shadow:0 0 10px #9d6bff88;text-transform:uppercase;letter-spacing:.1em;font-size:.64rem;font-weight:700}

.future{background:linear-gradient(180deg,#05050a,#10052a);color:white}
.future .tag{color:var(--pink);text-shadow:0 0 12px #ff2fd199}.future .lead{color:var(--muted)}
.futuregrid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:40px}
.futurecard{border:1px solid #9d6bff88;border-radius:22px;padding:23px;background:#9d6bff0d;box-shadow:0 0 22px #9d6bff33}
.futurecard .emoji{font-size:2rem;filter:drop-shadow(0 0 12px #ffffff88)}.futurecard h3{margin:16px 0 8px}.futurecard p{color:var(--muted)}
.futurecard small{color:var(--lime);text-shadow:0 0 8px var(--lime);text-transform:uppercase;font-size:.65rem;letter-spacing:.1em}

.team{text-align:center;background:var(--bg)}.team .heading,.team .lead{margin-left:auto;margin-right:auto}
.teambox{margin:35px auto 0;max-width:650px;border:1px dashed var(--cyan);border-radius:22px;padding:30px;color:var(--muted);background:#22e6ff0a;box-shadow:0 0 24px #22e6ff33}
.teambox strong{display:block;font:700 1.2rem Outfit;color:var(--lime);text-shadow:0 0 14px #c8ff3d77;margin-bottom:8px}

footer{background:#020205;color:white;padding:55px 8vw 25px;border-top:1px solid #ff2fd155}
.footrow{display:flex;justify-content:space-between;gap:30px;padding-bottom:45px}
.footer-logo{font-size:5rem}.footrow p{color:#8a90ad;line-height:1.7;max-width:330px;font-size:.84rem}
.footbottom{border-top:1px solid #ffffff22;padding-top:20px;display:flex;justify-content:space-between;color:#7d83a1;font-size:.7rem}

.reveal{opacity:0;transform:translateY(25px);transition:.8s}.reveal.visible{opacity:1;transform:none}
.top{display:none}

@media(max-width:850px){.navlinks{display:none}.hero{min-height:850px;padding:140px 7vw 80px;align-items:flex-start}.art{width:90vw;height:420px;right:5%;top:auto;bottom:15px}.intro,.park,.demogrid,.techgrid{grid-template-columns:1fr}.introart{min-height:300px}.headrow{display:block}.steps{grid-template-columns:1fr}.step{min-height:250px}.flow{position:relative;top:auto;order:2}.techlist{order:1}.futuregrid{grid-template-columns:1fr 1fr}.footrow{display:block}.parkart{height:300px}}
@media(max-width:560px){nav{padding:0 6vw;height:68px}.hero{min-height:790px;padding:125px 6vw 40px}.hero h1{font-size:5.2rem}.hero .desc{font-size:.9rem}.art{height:360px;width:100vw;right:0}.floatlabel{font-size:.6rem;padding:8px 10px}.fl1{right:2%}.fl2{left:2%}.hero-note{font-size:.58rem}section{padding:78px 6vw}.heading{font-size:3.05rem}.introart{height:280px}.stage{min-height:330px}.cards,.futuregrid{grid-template-columns:1fr}.card{min-height:unset}.parkart{height:270px}.footer-logo{font-size:4rem}.footbottom{display:block;line-height:2}.footbottom span{display:block}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}.reveal{opacity:1;transform:none}}
"""

EXTRA_CSS = """
.hero{height:auto!important;min-height:820px!important;max-height:none!important}
"""

FIT_RESPALDO = """
function fit(){var f=window.frameElement;if(f){f.style.height=document.documentElement.scrollHeight+'px';}}
window.addEventListener('load',fit);window.addEventListener('resize',fit);
if(window.ResizeObserver){new ResizeObserver(fit).observe(document.body);}
setTimeout(fit,300);setTimeout(fit,1200);
"""

ENLACES = """
function findTarget(id){
  var t=document.getElementById(id);if(t)return t;
  try{
    var pd=window.parent.document;t=pd.getElementById(id);if(t)return t;
    var fr=pd.querySelectorAll('iframe');
    for(var i=0;i<fr.length;i++){try{t=fr[i].contentDocument.getElementById(id);if(t)return t;}catch(e){}}
  }catch(e){}
  return null;
}
document.addEventListener('click',function(e){
  var a=e.target.closest('a[href^="#"]');if(!a)return;
  var id=a.getAttribute('href').slice(1);
  if(!id){e.preventDefault();return;}
  var t=findTarget(id);
  if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}
});
"""

BUTTERFLY = ('<div class="wing l"></div><div class="wing r"></div><div class="wing lower l"></div>'
             '<div class="wing lower r"></div><div class="body"></div><div class="antenna"></div>'
             '<div class="antenna a2"></div>')

# ---------- Bloques con espacio para tus medios ----------
def bloque_hero() -> str:
    m = slot("hero")
    centro = (f'<div class="heromedia">{m}</div>' if m else
              f'<div class="orbit"></div><div class="butterfly" id="heroButterfly">{BUTTERFLY}</div>')
    return (f'<div class="art">{centro}<div class="floatlabel fl1">✦ Un encuentro con la naturaleza</div>'
            '<div class="floatlabel fl2">Tu presencia transforma el vuelo</div></div>')


def bloque_intro() -> str:
    m = slot("intro")
    inner = m if m else "<span>🦋</span>"
    cls = " has-media" if m else ""
    return (f'<div class="introart reveal{cls}">{inner}'
            '<small>Curiosidad que se convierte en conexión</small></div>')


def bloque_park() -> str:
    m = slot("park")
    inner = m if m else "<span>🦋</span>"
    cls = " has-media" if m else ""
    return f'<div class="parkart reveal{cls}">{inner}</div>'


def bloque_demo() -> str:
    m = slot("demo")
    if m:
        centro = m
        boton = ""
        cls = " has-media"
    else:
        centro = f'<div class="orbit"></div><div class="butterfly" id="demoButterfly">{BUTTERFLY}</div>'
        boton = '<button id="flap">Abrir / cerrar alas ✨</button>'
        cls = ""
    return (f'<div class="stage reveal{cls}" id="demoStage">{centro}'
            f'<div class="stagefoot"><span id="distanceText">Distancia: lejos</span>{boton}</div></div>')


PARTE_1 = r"""<nav><a class="brand" href="#inicio">ALETEO<span>.</span></a><div class="navlinks"><a href="#concepto">El concepto</a><a href="#equilibrio">Equilibrio</a><a href="#experiencia">La experiencia</a><a href="#tecnologia">Tecnología</a><a href="#registro">Registro</a><a href="#reflexion">Reflexiones</a></div><a class="navbutton" href="#experiencia">Explorar ↓</a></nav>
<header class="hero" id="inicio"><div class="copy"><div class="eyebrow">Experiencia interactiva · Parque de la Conservación</div><h1>ALE<span>TEO.</span></h1><div class="subtitle">La naturaleza siente nuestra presencia.</div><p class="desc">¿Y si una mariposa pudiera responder a tus movimientos? Descubre una experiencia donde el cuerpo, la curiosidad y la tecnología se encuentran para acercarnos al mundo natural.</p><div class="actions"><a class="btn lime" href="#concepto">Descubrir el proyecto ↗</a><a class="btn ghost" href="#experiencia">Cómo funciona ↓</a></div><div class="hero-note">Acércate · Explora · Descubre</div></div>%%HERO%%<div class="scroll">DESLIZA PARA DESCUBRIR ↓</div></header>

<section class="intro" id="concepto"><div class="reveal"><div class="tag">01 / De dónde nace</div><h2 class="heading">No somos visitantes de la naturaleza. <em>Somos parte de ella.</em></h2><p class="lead">ALETEO nace de una pregunta: ¿cómo podemos acercar a los niños al mundo natural de una manera diferente? La propuesta transforma la observación en participación: una mariposa digital que responde a la presencia de quienes se acercan a ella.</p><p class="lead">A través del juego y la exploración corporal, ALETEO invita a los niños a reconocer sus ritmos y explorar la autorregulación emocional. La mariposa propone una metáfora sencilla: no siempre necesitamos correr ni permanecer inmóviles; podemos encontrar un ritmo propio, entre la calma y la energía, según lo que sentimos y necesitamos.</p></div>%%INTRO%%</section>
<section class="manifesto"><div class="tag">Una idea para sentir</div><blockquote class="reveal">A veces, basta con <span>encontrar nuestro ritmo</span> para descubrir el equilibrio.</blockquote><p class="reveal">La mariposa es el puente entre dos mundos: el humano y el natural. Su vuelo cambia con nuestra presencia y nos recuerda que cada movimiento tiene su momento. Cuando nos acercamos, su aleteo se acelera; cuando tomamos distancia, se calma. Así, los niños pueden explorar —sin instrucciones rígidas ni respuestas correctas— cómo se siente moverse rápido, hacer una pausa y encontrar un equilibrio propio.</p><div class="flower">✿</div></section>

<section class="experience" id="equilibrio"><div class="headrow reveal"><div><div class="tag">Una invitación a encontrar el ritmo propio</div><h2 class="heading">Ni correr todo el tiempo,<br>ni quedarse <em>quietos.</em></h2></div><p class="lead">ALETEO convierte el movimiento de la mariposa en una metáfora cercana para hablar con los niños sobre emociones, pausas y equilibrio.</p></div><div class="cards"><article class="card reveal"><h3>⚡ La energía también tiene su lugar</h3><p>Acercarse hace que la mariposa vuele más rápido. Podemos reconocer la emoción, la curiosidad y las ganas de explorar, sin pensar que sentir mucha energía está mal.</p></article><article class="card reveal"><h3>🌿 La pausa también importa</h3><p>Al tomar distancia, el aleteo se vuelve más lento. Hacer una pausa, respirar y observar también son formas valiosas de participar.</p></article></div><p class="lead reveal" style="margin-top:28px"><strong>El mensaje:</strong> no se trata de estar siempre acelerados ni de permanecer quietos. Se trata de reconocer cómo nos sentimos y encontrar, a nuestra manera, un ritmo que nos haga sentir bien, como la mariposa que acompasa su vuelo.</p></section>
<section class="experience" id="experiencia"><div class="headrow reveal"><div><div class="tag">02 / La experiencia</div><h2 class="heading">Tú te mueves.<br><em>Ella responde.</em></h2></div><p class="lead">La interacción sucede sin controles complicados: el visitante explora con su cuerpo y descubre cómo cambia el vuelo de la mariposa.</p></div><div class="steps"><article class="step reveal"><div class="emoji">🧍‍♀️</div><div class="num">01</div><h3>Te acercas</h3><p>Los sensores detectan el cambio de distancia y el sistema interpreta tu presencia.</p></article><article class="step reveal"><div class="emoji">🦋</div><div class="num">02</div><h3>La mariposa responde</h3><p>Al acercarte, su vuelo aumenta la velocidad. El movimiento digital reacciona a tu proximidad y te permite explorar cómo cambia el ritmo.</p></article><article class="step reveal"><div class="emoji">🌿</div><div class="num">03</div><h3>Encuentras tu ritmo</h3><p>Cuando tomas distancia, el vuelo se vuelve más lento. La experiencia invita a probar, hacer pausas y descubrir que la calma y la energía pueden convivir en equilibrio.</p></article></div></section>
<section class="demo" id="demo"><div class="demogrid"><div class="reveal"><div class="tag">03 / Prueba la idea</div><h2 class="heading">¿Qué pasa cuando <em>te acercas?</em></h2><p class="lead">Explora una pequeña simulación conceptual. Desliza el control para cambiar la proximidad y observa cómo varía el ritmo del aleteo.</p><p class="tiny">Esta demostración es una simulación web inspirada en el proyecto; no está conectada a los sensores físicos.</p></div>%%DEMO%%</div><div class="rangebox reveal"><label><span>LEJOS · VUELO TRANQUILO</span><span>CERCA · VUELO RÁPIDO</span></label><input class="range" type="range" min="0" max="100" value="25" id="proximity"><div class="meter"><div id="meterFill"></div></div></div></section>
<section id="tecnologia"><div class="techgrid"><div class="reveal"><div class="tag">04 / Cómo lo hicimos</div><h2 class="heading">Del movimiento a <em>la magia.</em></h2><p class="lead">La tecnología funciona como un puente invisible: capta información del espacio físico, la procesa y la convierte en cambios visuales que el visitante puede percibir.</p><p class="lead">El prototipo integra sensores ultrasónicos y TouchDesigner para traducir los datos de proximidad y posición en respuestas de la animación.</p></div><div class="flow reveal"><h3>Flujo de interacción</h3><div class="node">① Sensores ultrasónicos<br><small>Detección de distancia y posición</small></div><div class="arrow">↓</div><div class="node">② Procesamiento de datos<br><small>Lectura y adaptación de valores</small></div><div class="arrow">↓</div><div class="node">③ TouchDesigner<br><small>Control de la animación</small></div><div class="arrow">↓</div><div class="node" style="border-color:#c8ff3d;color:#c8ff3d;box-shadow:0 0 16px #c8ff3d55">④ Respuesta visual<br><small>La mariposa cambia su vuelo</small></div></div></div><div class="techlist"><article class="techitem reveal"><div class="icon">📡</div><div><h3>Sensores ultrasónicos</h3><p>Se utilizan dos sensores para obtener información de distancia y posición en los ejes de interacción definidos para el montaje.</p></div></article><article class="techitem reveal"><div class="icon">🧩</div><div><h3>TouchDesigner</h3><p>El entorno de programación visual recibe y procesa los datos para vincularlos con los parámetros de la animación.</p></div></article><article class="techitem reveal"><div class="icon">🎞️</div><div><h3>Animación audiovisual</h3><p>La mariposa digital es el centro visual de la experiencia. Su velocidad de vuelo responde a la proximidad detectada.</p></div></article></div></section>
<section class="park"><div class="reveal"><div class="tag">05 / Un espacio para aprender</div><h2 class="heading">Una nueva forma de acercarnos a la <em>conservación.</em></h2><p class="lead">En el contexto del Parque de la Conservación, ALETEO propone complementar la experiencia de aprendizaje ambiental con una interacción lúdica y sensible.</p><p class="lead">No busca reemplazar el encuentro con la biodiversidad, sino despertar preguntas, curiosidad y ganas de conocer y respetar a los seres vivos. También abre una conversación sencilla sobre el cuidado de nuestras emociones: reconocer cuándo queremos movernos, cuándo necesitamos parar y cómo encontrar un equilibrio propio.</p></div>%%PARK%%</section>

"""

PARTE_2 = r"""<section class="reflection" id="reflexion"><div class="tag">07 / Lo que aprendimos</div><h2 class="heading reveal">Diseñar también es <em>observar.</em></h2><p class="lead reveal">Completen estas notas con lo observado durante la grabación y las pruebas reales.</p><div class="cards"><article class="card reveal"><h3>👀 Comportamientos inesperados</h3><p>¿Qué hicieron los niños que el equipo no había previsto? ¿Intentaron tocar, seguir o perseguir la mariposa? ¿Descubrieron otras formas de interactuar?</p><small>Completar con observaciones reales</small></article><article class="card reveal"><h3>↔️ Ergonomía y acceso</h3><p>¿La altura y la ubicación de los sensores facilitaron la participación de niños de diferentes estaturas? ¿La interacción fue intuitiva?</p><small>Completar con observaciones reales</small></article><article class="card reveal"><h3>⚙️ Materiales y funcionamiento</h3><p>¿Cómo respondieron los sensores? ¿Hubo retrasos, fallas o condiciones del espacio que afectaran la proyección?</p><small>Completar con observaciones reales</small></article><article class="card reveal"><h3>💡 Aprendizajes del equipo</h3><p>¿Qué funcionó mejor de lo esperado? ¿Qué cambiarían después de observar a los visitantes interactuar?</p><small>Completar con observaciones reales</small></article></div></section>
<section class="future"><div class="tag">08 / Lo que sigue</div><h2 class="heading reveal">Una experiencia que puede <em>seguir creciendo.</em></h2><p class="lead reveal">ALETEO abre posibilidades para ampliar la interacción y enriquecer el vínculo entre cuerpo, tecnología y naturaleza.</p><div class="futuregrid"><article class="futurecard reveal"><div class="emoji">🪽</div><h3>Alas que responden</h3><p>Explorar el control de la apertura y el cierre de las alas mediante el movimiento vertical de las manos.</p><small>POSIBLE VERSIÓN 2.0</small></article><article class="futurecard reveal"><div class="emoji">🎵</div><h3>Un paisaje sonoro</h3><p>Incorporar sonidos ambientales y respuestas auditivas que acompañen la interacción.</p><small>POSIBLE VERSIÓN 2.0</small></article><article class="futurecard reveal"><div class="emoji">🌺</div><h3>Un ecosistema expandido</h3><p>Sumar flores, hojas, partículas u otras especies digitales para ampliar el universo visual.</p><small>POSIBLE VERSIÓN 2.0</small></article></div></section>
<section class="team"><div class="tag">09 / Quiénes lo hicieron posible</div><h2 class="heading reveal">Diseñado para <em>sentir y descubrir.</em></h2><p class="lead reveal">Un proyecto de diseño interactivo desarrollado para el Parque de la Conservación.</p><div class="teambox reveal"><strong>Equipo ALETEO</strong>Laura Natalia Garcia<br>Sara Londoño</div></section>
<footer><div class="footrow"><div><div class="footer-logo">ALE<span>TEO.</span></div><p>La naturaleza siente nuestra presencia. Una experiencia interactiva para acercarnos al mundo natural a través del juego y la tecnología.</p></div><div><div class="eyebrow">Parque de la Conservación</div><p>Proyecto de diseño interactivo<br>Equipo: ALETEO<br>Integrantes: Laura Natalia Garcia y Sara Londoño</p></div></div><div class="footbottom"><span>© ALETEO · Proyecto académico · Laura Natalia Garcia y Sara Londoño</span><span>Acercarse · Explorar · Descubrir 🦋</span></div></footer>"""

JS_1 = r"""
const glow=document.getElementById('glow');window.addEventListener('pointermove',e=>{glow.style.left=e.clientX+'px';glow.style.top=e.clientY+'px';const b=document.getElementById('heroButterfly');if(!b)return;const r=b.getBoundingClientRect(),dx=(e.clientX-r.left-r.width/2)/r.width,dy=(e.clientY-r.top-r.height/2)/r.height;b.style.translate=`${dx*12}px ${dy*12}px`});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(x=>io.observe(x));
const range=document.getElementById('proximity'),butterfly=document.getElementById('demoButterfly'),demoVideo=document.querySelector('#demoStage video'),label=document.getElementById('distanceText'),fill=document.getElementById('meterFill'),flap=document.getElementById('flap');
const anim=document.createElement('style');anim.textContent='@keyframes wingbeat{from{filter:brightness(1);transform:rotate(-8deg)}to{filter:brightness(1.3);transform:rotate(18deg)}}@keyframes demoFloat{50%{translate:0 -12px}}';document.head.appendChild(anim);
function update(){let v=+range.value;label.textContent=v<34?'Distancia: lejos':v<68?'Distancia: media':'Distancia: cerca';fill.style.width=v+'%';
if(butterfly){butterfly.style.animation=`demoFloat ${Math.max(.35,2.2-v*.017)}s ease-in-out infinite`;butterfly.querySelectorAll('.wing').forEach(w=>w.style.animation=`wingbeat ${Math.max(.22,1.1-v*.008)}s ease-in-out infinite alternate`)}
if(demoVideo){try{demoVideo.playbackRate=Math.min(4,.4+v*.036)}catch(e){}}}
range.addEventListener('input',update);update();
if(flap&&butterfly){flap.addEventListener('click',()=>{butterfly.classList.toggle('open');flap.textContent=butterfly.classList.contains('open')?'Cerrar alas ↻':'Abrir / cerrar alas ✨'})}
"""

JS_2 = r"""const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(x=>io.observe(x));"""


def pagina(html: str, js: str, fit: bool = False) -> str:
    return (
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{CSS}{EXTRA_CSS}</style></head><body>"
        f"<div class='glow' id='glow'></div>{html}"
        f"<script>{js}\n{ENLACES}{FIT_RESPALDO if fit else ''}</script></body></html>"
    )


def mostrar_html(html: str, js: str, alto_respaldo: int) -> None:
    """Muestra una parte del diseño HTML con altura automática."""
    if hasattr(st, "iframe"):  # Streamlit reciente: ajusta la altura solo
        st.iframe(pagina(html, js), height="content")
    else:  # Streamlit antiguo
        components.html(pagina(html, js, fit=True), height=alto_respaldo, scrolling=False)


def imagen(ruta: str) -> None:
    try:
        st.image(ruta, width="stretch")
    except TypeError:  # versiones antiguas
        st.image(ruta, use_container_width=True)


# ---------- 1) Portada, concepto, experiencia, demo, tecnología, parque ----------
parte1 = (PARTE_1
          .replace("%%HERO%%", bloque_hero())
          .replace("%%INTRO%%", bloque_intro())
          .replace("%%DEMO%%", bloque_demo())
          .replace("%%PARK%%", bloque_park()))
mostrar_html(parte1, JS_1, 6000)

# ---------- 2) Videos y fotos ----------
st.markdown('<div id="registro"></div>', unsafe_allow_html=True)
_, centro, _ = st.columns([1, 14, 1])
with centro:
    st.markdown(
        """
<div style="padding:90px 0 30px">
<div class="al-tag">06 / La experiencia en el espacio</div>
<h2 class="al-h">ALETEO <em>en acción.</em></h2>
<p class="al-lead">Registros del montaje y de las pruebas de interacción. Los videos muestran distintos momentos del prototipo en funcionamiento.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # Videos: 3 por fila
    for inicio in range(0, len(VIDEOS), 3):
        cols = st.columns(3, gap="medium")
        for col, (i, video) in zip(cols, enumerate(VIDEOS[inicio:inicio + 3], start=inicio + 1)):
            with col:
                st.video(str(video))
                st.markdown(
                    f'<div class="al-cap">Registro {i:02d}</div>'
                    '<div class="al-cap2">Video de documentación del proyecto ALETEO.</div>',
                    unsafe_allow_html=True,
                )

    # Fotos: solo aparece la galería si hay imágenes en la carpeta fotos/
    if FOTOS:
        st.markdown(
            """
<div style="padding:50px 0 25px">
<div class="al-tag">Galería</div>
<h2 class="al-h">Momentos del <em>proyecto.</em></h2>
</div>
""",
            unsafe_allow_html=True,
        )
        for inicio in range(0, len(FOTOS), 3):
            cols = st.columns(3, gap="medium")
            for col, foto in zip(cols, FOTOS[inicio:inicio + 3]):
                with col:
                    imagen(str(foto))
                    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

# ---------- 3) Reflexiones, futuro, equipo y pie de página ----------
mostrar_html(PARTE_2, JS_2, 3000)
